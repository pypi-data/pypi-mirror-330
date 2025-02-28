# -*- coding: utf-8 -*-

# Copyright: (c) 2024, Rudy Lei <shlei@cisco.com>, Yang Bian <yabian@cisco.com>, Wang Xiao <xiawang3@cisco.com>

import re
import ipaddress
import traceback
import threading

from collections import Counter
from time import sleep
from netmiko import ConnectHandler

from aac_init.log_utils import LazyLogger, netmiko_session_logger
from aac_init.control_engine.global_cache import context_cache


class AciSwitchTool:
    """ACI Switch Toolkits, include Telnet and SSH."""

    def __init__(
        self, global_policies: dict, switch_connection: dict, fabric_mgmt_node: dict, semaphore: threading.Semaphore = None
    ):
        for k, v in global_policies.items():
            setattr(self, k, v)
        for k, v in switch_connection.items():
            setattr(self, k, v)
        for k, v in fabric_mgmt_node.items():
            setattr(self, k, v)

        self.logger = LazyLogger(f"aciswitchtool_{self.hostname}.log")
        self.switch_telnet = {
            "host": self.console_address,
            "port": self.console_port,
            "username": self.aci_local_username,
            "password": self.aci_local_password,
            "session_log": netmiko_session_logger(
                f"telnet_session_{self.hostname}.log"
            ),
            "session_log_file_mode": "append",
            "fast_cli": False
        }
        self.telnet_connection = None

        self.switch_standby_telnet = {}
        if hasattr(self, "console_address_secondary") and hasattr(
            self, "console_port_secondary"
        ):
            self.switch_standby_telnet = {
                "host": self.console_address_secondary,
                "port": self.console_port_secondary,
                "username": self.aci_local_username,
                "password": self.aci_local_password,
                "session_log": netmiko_session_logger(
                    f"telnet_session_{self.hostname}_standby.log"
                ),
                "session_log_file_mode": "append",
                "global_delay_factor": 5,
                "fast_cli": False
            }
        self.telnet_connection_standby = None

        self.aci_version = None
        self.aci_switch_workflow = (
            0  # ACI switch validation, installation workflow protection
        )
        self.semaphore = semaphore

        self.logger.debug("ACI switch tool initialized successfully.")

    def _telnet_connect(self):
        """Telnet Connector"""

        DEVICE_TYPES = [
            "cisco_ios_telnet",
            "generic_telnet",
        ]

        for i in range(1, 4):
            for device_type in DEVICE_TYPES:
                try:
                    self.logger.debug(
                        f"Attempting to connect '{self.hostname}' via telnet '{self.console_address}:{self.console_port}' with '{device_type}'..."
                    )
                    self.switch_telnet["device_type"] = device_type
                    self.telnet_connection = ConnectHandler(**self.switch_telnet)
                    self.logger.debug(
                        f"Connected to '{self.console_address}:{self.console_port}' with '{device_type}' successfully!"
                    )
                    return True
                except Exception as e:
                    self.logger.debug(
                        f"Failed to connect to '{self.console_address}:{self.console_port}' with '{device_type}': {e}"
                    )
                    self.logger.debug(traceback.format_exc())
                    sleep(3)

            self.logger.debug(
                f"Failed to connect to '{self.console_address}:{self.console_port}' with both telnet methods! Retry = {i}"
            )

        self.logger.error(
            f"Failed to connect to '{self.console_address}:{self.console_port}' with both telnet methods after 3 attempts!"
        )
        return False

    def _telnet_connect_standby(self):
        """Telnet Connector for standby"""

        DEVICE_TYPES = [
            "cisco_ios_telnet",
            "generic_telnet",
        ]

        for i in range(1, 4):
            for device_type in DEVICE_TYPES:
                try:
                    self.logger.debug(
                        f"Attempting to connect {self.hostname}_standby via telnet {self.console_address_secondary}:{self.console_port_secondary} with {device_type}..."
                    )
                    self.switch_standby_telnet["device_type"] = device_type
                    self.telnet_connection_standby = ConnectHandler(
                        **self.switch_standby_telnet
                    )
                    self.logger.debug(
                        f"Connected to '{self.console_address_secondary}:{self.console_port_secondary}' with '{device_type}' successfully!"
                    )
                    return True
                except Exception as e:
                    self.logger.debug(
                        f"Failed to connect to '{self.console_address_secondary}:{self.console_port_secondary}' with '{device_type}': {e}"
                    )
                    self.logger.debug(traceback.format_exc())
                    sleep(3)

            self.logger.debug(
                f"Failed to connect to '{self.console_address_secondary}:{self.console_port_secondary}' with both telnet methods! Retry = {i}"
            )

        self.logger.error(
            f"Failed to connect to '{self.console_address_secondary}:{self.console_port_secondary}' with both telnet methods after 3 attempts!"
        )
        return False

    def _telnet_disconnect(self):
        if self.telnet_connection:
            self.telnet_connection.disconnect()
            sleep(3)  # Safely release console
            self.logger.debug(f"Disconnected telnet connection for: {self.hostname}")
            return True
        else:
            self.logger.error(f"No telnet connection found: {self.hostname}")
            return False

    def _telnet_disconnect_standby(self):
        if self.telnet_connection_standby:
            self.telnet_connection_standby.disconnect()
            sleep(3)  # Safely release console
            self.logger.debug(
                f"Disconnected standby telnet connection for: {self.hostname}"
            )
            return True
        else:
            self.logger.error(f"No standby telnet connection found: {self.hostname}")
            return False

    def _validate_aci_switch_image(self):
        """Validate ACI switch image"""

        self.logger.debug("Validating ACI switch image...")
        pattern = r"(?:aci-n9000-dk9\.)(\d+\.\d+\.\d+[a-z])\.bin"
        version_match = re.search(pattern, self.switch_image)

        if version_match:
            self.logger.debug(
                f"Validate version: '{version_match.group(1)}' successfully."
            )
            version_part = re.match(
                r"(\d+)\.(\d+)\.(\d+)([a-z])", version_match.group(1)
            )

            if version_part:
                major, minor, patch, _ = version_part.groups()
                self.aci_version = [int(major), int(minor), int(patch)]
                self.logger.debug(f"ACI version: {self.aci_version}")
                return True
            else:
                self.logger.error("Failed to parse the version components!")
        else:
            self.logger.error("Invalid ACI switch image format!")

        return False

    def _find_valid_prompt(self, telnet_connection, delay_factor=60, max_attempts=3):
        # invalid_pattern = r"^\[\s*\d+\.\d+\]"
        valid_pattern = r"loader >|\(none\)#|\(none\) login:|^[^#]*#\s*$"
        attempts = 0
        attempt_prompt_lst = []

        while attempts < max_attempts:
            prompt = telnet_connection.find_prompt(delay_factor=delay_factor)
            self.logger.debug(f"Attempt {attempts + 1}: Prompt received: {prompt}")
            attempt_prompt_lst.append(prompt)
            if re.search(valid_pattern, prompt):
                return prompt
            attempts += 1

        most_common_prompt, count = Counter(attempt_prompt_lst).most_common(1)[0]
        self.logger.warning(
            f"No valid prompt found after {max_attempts} attempts. "
            f"Returning most common prompt: {most_common_prompt} (Count: {count})"
        )
        return most_common_prompt


    def _telnet_validate_aci_switch(self, telnet_connection):
        """
        1. Validate ACI switch image.
        2. Validate ACI switch based on switch prompt:
            - loader: not supported for version 16.0.2 and later, warning if no 'keyinfo'
            - nxos/aci with N9K PID: pass
        """

        self.logger.debug(f"Validating ACI switch: {self.hostname}")

        self._validate_aci_switch_image()
        if not self.aci_version:
            self.logger.error(
                "Validate ACI switch failed due to image validation failed!"
            )
            return False

        try:
            switch_prompt = self._find_valid_prompt(telnet_connection)
            self.logger.debug(f"switch prompt: {switch_prompt}")

            if "(none) login" in switch_prompt:
                telnet_connection.send_command_timing("admin")
                switch_prompt = self._find_valid_prompt(telnet_connection)
            elif "login:" in switch_prompt:
                output = telnet_connection.send_command_timing(self.aci_local_username, read_timeout=20)
                if "Password" in output:
                    telnet_connection.send_command_timing(self.aci_local_password, read_timeout=20)
                switch_prompt = self._find_valid_prompt(telnet_connection)

            if "loader >" in switch_prompt:
                loader_output = telnet_connection.send_command_timing("keyinfo")
                if self.aci_version >= [16, 0, 2]:
                    self.logger.error(
                        f"Selected ACI version is {self.aci_version}, cannot determine memory and hardware information under loader mode! Manual intervention required."
                    )
                    return False

                if "Nexus9k" in loader_output:
                    self.aci_switch_workflow = 2
                    self.logger.debug(
                        "Nexus9k identified in loader output. Loader validated successfully."
                    )
                    return True

                else:
                    self.logger.warning(
                        "N9K not found in loader output or 'keyinfo' not supported in this loader version. Manual intervention required."
                    )
                    self.logger.warning(
                        "Beta behavior: aac-init will keep installing ACI image, but it might be failed..."
                    )
                    self.aci_switch_workflow = 2
                    return True

            elif "#" in switch_prompt:
                version_output = telnet_connection.send_command(
                    "show version | grep kickstart", read_timeout=15
                )
                version_output += telnet_connection.send_command(
                    "cat /mnt/cfg/0/boot/grub/menu.lst.local", read_timeout=15
                )

                if "aci" in version_output:
                    self.aci_switch_workflow = 1
                    self.logger.debug(
                        "ACI image identified. Switch validated successfully."
                    )
                    return True

                elif "nxos" in version_output:
                    self.aci_switch_workflow = 2
                    self.logger.debug(
                        "NXOS image identified. Switch validated successfully."
                    )
                    return True
                else:
                    self.logger.error(
                        "Switch validation failed! ACI/NXOS or N9K not detected!"
                    )

            else:
                self.logger.error(
                    "Unrecognized device prompt. Unable to validate the switch!"
                )

        except Exception as e:
            # Log any exceptions that occur during the validation process
            self.logger.error(
                f"Exception occurred during validation for aci switch: {str(e)}"
            )
            self.logger.error(traceback.format_exc())

        finally:
            if telnet_connection == self.telnet_connection:
                self._telnet_disconnect()
            elif telnet_connection == self.telnet_connection_standby:
                self._telnet_disconnect_standby()
            else:
                self.logger.error(
                    f"Unknown telnet connection: {str(telnet_connection)}"
                )

        return False

    def _telnet_set_loader(self, telnet_connection, delay_factor=60):
        """Set N9K switch to loader mode"""

        # ACI switch validation is required before set loader
        if self.aci_switch_workflow not in [1, 2]:
            self.logger.error("ACI switch validation is not performed, aborting...")
            return False

        self.logger.debug(f"Setting '{self.hostname}' to loader...")

        try:
            switch_prompt = telnet_connection.find_prompt(delay_factor=delay_factor)
            if "loader >" in switch_prompt:
                self.logger.debug("Already in loader.")
                return True
            else:
                switch_prompt += telnet_connection.send_command_timing(
                    "\n",
                    last_read=300,
                    read_timeout=1200,
                    strip_prompt=False,
                    strip_command=False
                )
            self.logger.debug(f"switch prompt: {switch_prompt}")

            if "login:" in switch_prompt:
                if "(none) login:" in switch_prompt:
                    telnet_connection.send_command_timing(
                        "admin"
                    )
                else:
                    telnet_connection.send_command_timing(self.aci_local_username)
                    telnet_connection.send_command_timing(self.aci_local_password)

            current_os_running = telnet_connection.send_command(
                "show version | grep kickstart", read_timeout=20
            )
            current_os_running += telnet_connection.send_command(
                "cat /mnt/cfg/0/boot/grub/menu.lst.local", read_timeout=40
            )

            pid_raw = telnet_connection.send_command(
                "show inventory | grep -A1 Chassis", read_timeout=40
            )
            pid_pattern = re.compile(r"PID: (N9K-[A-Z0-9\-]+)")

            if pid_raw:
                if not pid_pattern.findall(pid_raw):
                    self.logger.error(
                        f"Unable to determine chassis PID! PID raw output:\n {pid_raw}"
                    )
                    return False
            else:
                if not self.switch_image:
                    self.logger.error(
                        "Unable to determine ACI version!"
                    )
                    return False

            # Version 16.0.2, determine image by hardware PID
            if self.aci_version == [16, 0, 2]:
                SWITCH_602_64BIT = [
                    "N9K-C9408",
                    "N9K-C9504",
                    "N9K-C9508",
                    "N9K-C9516",
                    "N9K-C9364D-GX2A",
                    "N9K-C9348D-GX2A",
                    "N9K-C9332D-GX2B",
                    "N9K-C93600CD-GX",
                    "N9K-C9316D-GX",
                    "N9K-C9364C",
                ]

                if pid_pattern.findall(pid_raw)[0] in SWITCH_602_64BIT:
                    self.switch_image = self.switch_image.replace(".bin", "-cs_64.bin")
                    self.logger.debug(f"Update target image to: '{self.switch_image}'")

            # Version above 16.0.2, determine image by memory, 32G memory will install 64bits, lower than 32G will install 32bits
            # Installation guidelines for software versions 6.0.3 and later:
            # - By default, the installation type is determined based on memory size:
            #   - Install the 32-bit version if memory is less than 32G.
            #   - Install the 64-bit version if memory is 32G or more.
            # - Exceptions apply for specific supervisor module models (as shown in "show module" output):
            #   - For sup-a (16G) or sup-a+ (16G), versions 6.0.3, 6.0.4, and 6.0.5 cannot be installed.
            #   - For sup-a, sup-a+, or sup-b (24G), always install the 32-bit version.
            #   - For sup-b+ (32G), always install the 64-bit version.

            if self.aci_version >= [16, 0, 3]:
                show_module_content = telnet_connection.send_command("show module", read_timeout=20)
                supervisor_pattern = r"Supervisor Module\s+(\S+)"
                supervisor_version_matches = re.findall(supervisor_pattern, show_module_content)
                if [16, 0, 3] <= self.aci_version <= [16, 0, 5]:
                    for match in supervisor_version_matches:
                        if match.lower() in ["sup-a", "sup-a+"]:
                            self.logger.error(f"Installation Blocked: The detected Supervisor Module version is '{match.lower}'. "
                                              f"Installation of the {'.'.join(self.aci_version)} image is not supported on this hardware. "
                                              f"Please verify the system requirements and choose a compatible image version.")
                            return False

                replace_flag = False
                if self.aci_version >= [16, 0, 6]:
                    for match in supervisor_version_matches:
                        if match.lower in ["sup-b+"]:
                            self.switch_image = self.switch_image.replace(".bin", "-cs_64.bin")
                            replace_flag = True
                            self.logger.debug(f"Update target image to: '{self.switch_image}'")
                            break

                if not replace_flag:
                    mem_raw = telnet_connection.send_command(
                        "cat /proc/meminfo | grep MemTotal", read_timeout=20
                    )
                    mem_match = re.search(r"\bMemTotal:\s+(\d+)", mem_raw)
                    if not mem_match:
                        self.logger.error(
                            f"Unable to determine ACI version per memory check! Memory raw data: '{mem_raw}'"
                        )
                        return False

                    mem_result = mem_match.group(1)

                    if int(mem_result) > 30000000:  # 32G system
                        self.switch_image = self.switch_image.replace(
                            ".bin", "-cs_64.bin"
                        )
                        self.logger.debug(
                            f"Update target image to: '{self.switch_image}' per memory check, memory result: '{mem_result}'"
                        )

            # ACI handler
            if "aci" in current_os_running:
                self.logger.debug("ACI OS handling...")
                telnet_connection.send_command("rm -f bootflash/*.bin", read_timeout=30)
                telnet_connection.send_command(
                    "setup-clean-config.sh", "Done", read_timeout=180
                )
                telnet_connection.send_command(
                    "clear-bootvars.sh", "Done", read_timeout=180
                )

                grub0_output = telnet_connection.send_command(
                    "ls /mnt/cfg/0/boot/grub/"
                )
                grub1_output = telnet_connection.send_command(
                    "ls /mnt/cfg/1/boot/grub/"
                )
                # match file/folder
                file_pattern = re.compile(
                    r"^[\w\-\.\s\u4e00-\u9fff\u3040-\u30ff\u00a1-\uffff]+$"
                )
                grub0_files = [
                    line
                    for line in grub0_output.splitlines()
                    if file_pattern.match(line)
                ]
                grub1_files = [
                    line
                    for line in grub1_output.splitlines()
                    if file_pattern.match(line)
                ]
                if grub0_files or grub1_files:
                    self.logger.error("Clear grub failed!")
                    self.logger.error(f"Grab0: {grub0_files}")
                    self.logger.error(f"Grab1: {grub1_files}")
                    return False

                self.logger.debug("GRUB cleared, entering loader...")
                telnet_connection.send_command(
                    "reload", "This command will reload the chassis", read_timeout=60
                )
                telnet_connection.send_command_timing("y")

                telnet_connection.read_until_pattern(
                    pattern="loader >", read_timeout=300
                )

            # Nexus handler
            else:
                self.logger.debug("NXOS handling...")
                telnet_connection.send_command(
                    "configure terminal", "config", read_timeout=20
                )
                telnet_connection.send_command(
                    "delete bootflash:*.bin no-prompt", read_timeout=20
                )
                telnet_connection.send_command("no boot nxos", read_timeout=20)
                telnet_connection.send_command(
                    "copy running-config startup-config",
                    "Copy complete.",
                    read_timeout=60,
                )
                telnet_connection.send_command(
                    "reload", "This command will reboot the system", read_timeout=30
                )
                telnet_connection.send_command_timing("y")
                telnet_connection.read_until_pattern(
                    pattern="loader >", read_timeout=300
                )

            self.aci_switch_workflow = 2
            self.logger.debug("Entered to loader.")
            return True

        except Exception as e:
            # Log any exceptions that occur during the set loader process
            self.logger.error(
                f"Exception occurred during set loader for aci switch: {str(e)}"
            )
            self.logger.error(traceback.format_exc())

        finally:
            if telnet_connection == self.telnet_connection:
                self._telnet_disconnect()
            elif telnet_connection == self.telnet_connection_standby:
                self._telnet_disconnect_standby()
            else:
                self.logger.error(
                    f"Unknown telnet connection: {str(telnet_connection)}"
                )

        return False

    def _telnet_loader_install_aci_switch(self, telnet_connection):
        """Install aci switch from loader mode"""

        # loader is required to install aci switch
        if self.aci_switch_workflow != 2:
            self.logger.error(
                "ACI switch validation or set loader is required before installation, aborting..."
            )
            return False

        self.logger.debug(f"Installing '{self.hostname}' from loader...")

        aci_switch_image_http = self.aci_image_path + self.switch_image
        aci_switch_image_tftp = aci_switch_image_http.replace("http", "tftp")
        self.logger.debug(f"ACI switch image tftp path: {aci_switch_image_tftp}")

        device_oob_trad = ipaddress.IPv4Interface(self.oob_address)
        set_tftp_ip = f"set ip {device_oob_trad.ip} {device_oob_trad.netmask}"
        set_tftp_gw = f"set gw {self.oob_gateway}"
        tftp_boot_cmd = f"boot {aci_switch_image_tftp}"

        try:
            telnet_connection.send_command_timing("\n")
            telnet_connection.send_command_timing(set_tftp_ip)
            set_gw_result = telnet_connection.send_command_timing(set_tftp_gw)

            self.logger.debug(f"set gw result content: {set_gw_result}")

            address_check = f"Address: {device_oob_trad.ip}" in set_gw_result
            netmask_check = f"Netmask: {device_oob_trad.netmask}" in set_gw_result
            gateway_check = f"Gateway: {self.oob_gateway}" in set_gw_result

            if all([address_check, netmask_check, gateway_check]):
                if self.semaphore:
                    with self.semaphore:
                        telnet_connection.send_command_timing(tftp_boot_cmd)
                else:
                    telnet_connection.send_command_timing(tftp_boot_cmd)
                self.logger.debug(
                    (
                        f"Node '{self.hostname}': Starting to install '{self.switch_image}'"
                    )
                )
                telnet_connection.read_until_pattern(
                    pattern="User Access Verification", read_timeout=900
                )

                # loader post-installation check
                sleep(180)
                post_check_result = telnet_connection.send_command_timing("\n")
                version_post_check = re.search(
                    r"aci-n9000-dk9\.\d+\.\d+\.\d+[a-z]", self.switch_image
                ).group(0)

                for i in range(1, 31):
                    self.logger.debug(f"Post check retry: {i}")
                    self.logger.debug(post_check_result)
                    if "(none) login:" in self._find_valid_prompt(telnet_connection):
                        post_check_result = telnet_connection.send_command_timing(
                            "admin"
                        )

                    elif "(none)#" in self._find_valid_prompt(telnet_connection):
                        post_check_result = telnet_connection.send_command(
                            "cat /mnt/cfg/0/boot/grub/menu.lst.local",
                            expect_string=version_post_check,
                            read_timeout=60,
                        )
                        self.logger.debug(
                            f"ACI switch successfully installed {self.switch_image}"
                        )

                        return True

                    else:
                        post_check_result = telnet_connection.send_command_timing("\n")
                        sleep(1)

                self.logger.error("ACI switch installation post-check timeout!")
            else:
                self.logger.error("set_gw_result check failed!")

        except Exception as e:
            # Log any exceptions that occur during the set loader process
            self.logger.error(
                f"Exception occurred during set loader for aci switch: {str(e)}"
            )
            self.logger.error(traceback.format_exc())

        finally:
            if telnet_connection == self.telnet_connection:
                self._telnet_disconnect()
            elif telnet_connection == self.telnet_connection_standby:
                self._telnet_disconnect_standby()
            else:
                self.logger.error(
                    f"Unknown telnet connection: {str(telnet_connection)}"
                )

        return False

    def validate_aci_switch(self):
        """
        Validate ACI switch by performing the following steps:
        1. Validate switch active console
        2. Validate switch standby console if modular spine(Opt)
        """

        self.logger.debug(f"Validating ACI switch: {self.hostname}")

        if not self._telnet_connect():
            self.logger.error(
                f"Validating ACI switch '{self.hostname}' failed due to console login failed!"
            )
            return False

        if self._telnet_validate_aci_switch(self.telnet_connection):
            self.logger.debug(f"ACI switch '{self.hostname}' validated successfully.")
        else:
            self.logger.error(f"Failed to validate ACI switch '{self.hostname}'!")
            return False

        # Validate Standby sup for modular spine if have
        if self.switch_standby_telnet:
            if not self._telnet_connect_standby():
                self.logger.error(
                    f"Validating ACI switch '{self.hostname}_standby' failed due to console login failed!"
                )
                return False

            if self._telnet_validate_aci_switch(self.telnet_connection_standby):
                self.logger.debug(
                    f"ACI switch '{self.hostname}_standby' validated successfully."
                )
            else:
                self.logger.error(
                    f"Failed to validate ACI switch '{self.hostname}_standby'!"
                )
                return False

        return True

    def detect_active_and_standby(self, ori_active_connection, ori_standby_connection):
        """
        # 1. If both active and standby connections are in loader mode, return (ori_active_connection, ori_standby_connection).
        # 2. If only one connection is in loader, it is the active connection. Return (loader connection, other connection).
        # 3. If neither connection is in loader, determine the active and standby roles. Return (new active, new standby) if roles are correctly identified.
        # 4. If both connections are either active or standby due to incorrect input, log an error.
        """

        ori_active_prompt = self._find_valid_prompt(ori_active_connection)
        self.logger.debug(f"Original active prompt: {ori_active_prompt}")

        ori_standby_prompt = self._find_valid_prompt(ori_standby_connection)
        self.logger.debug(f"Original standby prompt: {ori_standby_prompt}")

        if "loader >" in ori_active_prompt and "loader >" in ori_standby_prompt:
            self.logger.debug("Both active and standby are in loader mode.")
            return ori_active_connection, ori_standby_connection

        if "loader >" in ori_active_prompt:
            self.logger.debug("Original active is in loader mode.")
            return ori_standby_connection, ori_active_connection

        if "loader >" in ori_standby_prompt:
            self.logger.debug("Original standby is in loader mode.")
            return ori_active_connection, ori_standby_connection

        self.logger.debug("Neither the original active nor the original standby is in loader mode, starting to attempt identification.")

        # If neither is in loader, determine which is active and which is standby
        ori_active_is_standby = False
        ori_standby_is_standby = False

        ori_active_output = ""
        ori_standby_output = ""
        max_retries = 3
        retries = 0
        current_timeout = 15
        while retries < max_retries:
            try:
                if not ori_active_output:
                    ori_active_output = ori_active_connection.send_command("show module", read_timeout=current_timeout)
                if not ori_standby_output:
                    ori_standby_output = ori_standby_connection.send_command("show module", read_timeout=current_timeout)
                break
            except Exception as e:
                self.logger.debug(f"Attempt {retries + 1} failed with error: {e}. Retrying...")
                retries += 1
                current_timeout += 5
        if not (ori_active_output or ori_standby_output):
            if not ori_active_output:
                self.logger.error(
                    f"Failed to execute command in original active connection after {max_retries} retires.")
            if not ori_standby_output:
                self.logger.error(
                    f"Failed to execute command in original standby connection after {max_retries} retires.")
            return False, False

        if "Module information could not be retrieved" in ori_active_output:
            self.logger.debug("Original active is standby based on module output.")
            ori_active_is_standby = True

        if "Module information could not be retrieved" in ori_standby_output:
            self.logger.debug("Original standby is standby based on module output")
            ori_standby_is_standby = True

        if ori_active_is_standby and not ori_standby_is_standby:
            return ori_standby_connection, ori_active_connection
        elif ori_standby_is_standby and not ori_active_is_standby:
            return ori_active_connection, ori_standby_connection

        self.logger.error(f"Both connections are either active or standby due to user input error")
        self.logger.debug(ori_active_connection)
        self.logger.debug(ori_standby_connection)

        return False, False

    def set_loader(self, telnet_connection, connection_name, delay_factor=60):
        if self._telnet_set_loader(telnet_connection, delay_factor):
            self.logger.debug(f"Setting ACI switch '{connection_name}' to loader successfully.")
            return True
        else:
            self.logger.error(f"Failed to set ACI switch '{connection_name}' to loader!")
            return False

    def install_aci_switch(self):
        """
        Install ACI switch by performing the following steps:
        1. if console_address_secondary && console_port_secondary, check active/standby sup via "show module"
        2. Set switch active console to loader
        3. Set switch standby console to loader if modular spine(Opt)
        4. Install switch active console
        5. Install switch standby console if modular spine(Opt)
        """

        self.logger.debug(f"Installing ACI switch: '{self.hostname}'...")

        if not self._telnet_connect():
            self.logger.error(
                f"Install ACI switch '{self.hostname}' failed due to console login failed!"
            )
            return False

        if self.switch_standby_telnet:
            if not self._telnet_connect_standby():
                self.logger.error(
                    f"Install ACI switch '{self.hostname}_standby' failed due to console login failed!"
                )
                return False

            active_connection, standby_connection = self.detect_active_and_standby(
                self.telnet_connection,
                self.telnet_connection_standby
            )
            if not (active_connection or standby_connection):
                self.logger.debug("There is an error when detect connection active and standby.")
                return False

            active_hostname = self.hostname if active_connection == self.telnet_connection else f"{self.hostname}_standby"
            standby_hostname = f"{self.hostname}_standby" if standby_connection == self.telnet_connection_standby else self.hostname

            if not self.set_loader(active_connection, active_hostname):
                return False

            if not self.set_loader(standby_connection, standby_hostname, delay_factor=600):
                return False
        else:
            if not self.set_loader(self.telnet_connection, self.hostname):
                return False

        # Set Standby sup to loader for modular spine if have
        if not self._telnet_connect():
            self.logger.error(
                f"Install ACI switch '{self.hostname}' failed due to console login failed!"
            )
            return False

        if self._telnet_loader_install_aci_switch(self.telnet_connection):
            self.logger.info(
                f"Install ACI switch '{self.hostname}' to '{self.switch_image}' successfully."
            )
        else:
            self.logger.error(
                f"Failed to install ACI switch '{self.hostname}' to '{self.switch_image}'!"
            )
            return False

        # Install Standby sup for modular spine if have
        if self.switch_standby_telnet:
            if not self._telnet_connect_standby():
                self.logger.error(
                    f"Install ACI switch '{self.hostname}_standby' failed due to console login failed!"
                )
                return False

            if self._telnet_loader_install_aci_switch(self.telnet_connection_standby):
                self.logger.info(
                    f"Install ACI switch '{self.hostname}_standby' to '{self.switch_image}' successfully."
                )
            else:
                self.logger.error(
                    f"Failed to install ACI switch '{self.hostname}_standby' to '{self.switch_image}'!"
                )
                return False

        return True

    def _telnet_clear_configuration(self, telnet_connection, host_name, delay_factor=60):
        # ACI switch validation is required
        if self.aci_switch_workflow != 1:
            self.logger.error("ACI switch validation failed, aborting...")
            return False

        self.logger.debug(f"Clearing configuration '{host_name}'")

        try:
            switch_prompt = telnet_connection.find_prompt(delay_factor=delay_factor)

            switch_prompt += telnet_connection.send_command_timing(
                "\n",
                last_read=300,
                read_timeout=1200,
                strip_prompt=False,
                strip_command=False
            )
            self.logger.debug(f"switch prompt: {switch_prompt}")
            if "login:" in switch_prompt:
                if "(none) login:" in switch_prompt:
                    # exit, already no config
                    return True
                else:
                    telnet_connection.send_command_timing(self.aci_local_username)
                    telnet_connection.send_command_timing(self.aci_local_password)

            telnet_connection.send_command(
                "setup-clean-config.sh", "Done", read_timeout=180
            )

            telnet_connection.send_command(
                "reload", "This command will reload the chassis", read_timeout=60
            )
            telnet_connection.send_command_timing("y")

            telnet_connection.read_until_pattern(
                pattern=r"\(none\) login:", read_timeout=300
            )
            return True
        except Exception as e:
            # Log any exceptions that occur during clearing configuration for aci switch
            self.logger.error(
                f"Exception occurred during clearing configuration for aci switch: {str(e)}"
            )
            self.logger.error(traceback.format_exc())
        finally:
            if telnet_connection == self.telnet_connection:
                self._telnet_disconnect()
            elif telnet_connection == self.telnet_connection_standby:
                self._telnet_disconnect_standby()
            else:
                self.logger.error(
                    f"Unknown telnet connection: {str(telnet_connection)}"
                )

        return False

    def clear_configuration(self):
        # find active, and execute command on active. no need in standby
        self.logger.debug(f"Clearing ACI switch configuration: '{self.hostname}'...")
        if not self._telnet_connect():
            self.logger.error(
                f"Clear ACI switch '{self.hostname}' configuration failed due to console login failed!"
            )
            return False

        if not self.switch_standby_telnet:
            active_connection = self.telnet_connection
            active_hostname = self.hostname
        else:
            if not self._telnet_connect_standby():
                self.logger.error(
                    f"Install ACI switch '{self.hostname}_standby' failed due to console login failed!"
                )
                return False

            active_connection, standby_connection = self.detect_active_and_standby(
                self.telnet_connection,
                self.telnet_connection_standby
            )
            if not (active_connection or standby_connection):
                self.logger.debug("There is an error when detect connection active and standby.")
                return False
            active_hostname = self.hostname if active_connection == self.telnet_connection else f"{self.hostname}_standby"

        if not self._telnet_clear_configuration(active_connection, active_hostname):
            self.logger.error(f"Clear ACI switch '{active_hostname}' configuration failed")
            return False

        return True

        # if self.switch_standby_telnet:
        #     if not self._telnet_connect_standby():
        #         self.logger.error(
        #             f"Install ACI switch '{self.hostname}_standby' failed due to console login failed!"
        #         )
        #         return False
        #
        #     if not self._telnet_clear_configuration(self.telnet_connection_standby, f"{self.hostname}_standby"):
        #         self.logger.error(
        #             f"Install ACI switch '{self.hostname}_standby' failed due to console login failed!"
        #         )
        #         return False

        #     active_connection, standby_connection = self.detect_active_and_standby(
        #         self.telnet_connection,
        #         self.telnet_connection_standby
        #     )
        #     if not (active_connection or standby_connection):
        #         self.logger.debug("There is an error when detect connection active and standby.")
        #         return False
        #
        #     active_hostname = self.hostname if active_connection == self.telnet_connection else f"{self.hostname}_standby"
        #     standby_hostname = f"{self.hostname}_standby" if standby_connection == self.telnet_connection_standby else self.hostname
        #
        #     if not self._telnet_clear_configuration(active_connection, active_hostname):
        #         return False
        #
        #     if not self._telnet_clear_configuration(standby_connection, standby_hostname):
        #         return False
        # else:
        #     if not self._telnet_clear_configuration(self.telnet_connection, self.hostname):
        #         return False

        # return True
