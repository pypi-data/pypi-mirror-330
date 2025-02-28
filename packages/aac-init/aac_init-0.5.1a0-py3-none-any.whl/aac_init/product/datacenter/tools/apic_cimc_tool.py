# -*- coding: utf-8 -*-

# Copyright: (c) 2024, Rudy Lei <shlei@cisco.com>, Yang Bian <yabian@cisco.com>

import re
import urllib3
import requests
import xml.etree.ElementTree as ET
import time
import traceback

from aac_init.log_utils import LazyLogger, netmiko_session_logger
from aac_init.control_engine.global_cache import context_cache
from aac_init.control_engine.metadata_loader import metadata
from netmiko import ConnectHandler

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class ApicCimcTool:
    """APIC CIMC Toolkits, include API and SSH."""

    def __init__(self, global_policies: dict, apic_cimc_connection: dict, apics: list):
        for k, v in global_policies.items():
            v = str(v) if isinstance(v, int) else v
            setattr(self, k, v)
        for k, v in apic_cimc_connection.items():
            v = str(v) if isinstance(v, int) else v
            setattr(self, k, v)
        self.apics = apics
        self.logger = LazyLogger(f"apiccimctool_{self.hostname}.log")
        self.device_ssh = {
            "host": self.cimc_address,
            "username": self.apic_cimc_username,
            "password": self.apic_cimc_password,
            "fast_cli": False,  # Disable fast CLI to mimic human-like sending
            "session_log": netmiko_session_logger(
                f"ssh_session_{self.hostname}_cimc.log"
            ),
            "session_log_file_mode": "append",
            "global_delay_factor": 5,
            "auth_timeout": 120,
        }
        self.token = None
        self.ssh_connection = None
        self.apic_workflow = (
            0  # APIC validate, api_install, ssh_install workflow protection
        )
        self.apic_config_dict = {
            "Enter the fabric name": self.fabric_name,
            "Enter the fabric ID": self.fabric_id,
            "Enter the number of active controllers in the fabric": self.fabric_active_controllers,
            "Enter the POD ID": self.pod,
            "Is this a standby controller": self.standby_controller,
            "Enter the controller ID": self.id,
            "Enter the controller name": self.hostname,
            "Enter address pool for TEP addresses": self.tep_pool,
            "Enter the VLAN ID for infra network": self.infra_vlan,
            "Enter address pool for BD multicast addresses": self.gipo,
            "Enable IPv6 for Out of Band Mgmt": "N\n",  # Don't support IPv6 at this moment
            "Enter the IPv4 address of the default gateway": self.apic_gateway,
            "Enter the IPv4 address": f"{self.apic_address}/{self.apic_netmask}",
            "Enter the interface speed": "\n",  # Don't support to change speed at this moment
            "Enable strong passwords": self.strong_password,
            "Enter the password for admin": self.aci_local_password,
            "Reenter the password for admin": self.aci_local_password,
            "Standalone APIC Cluster": "no\n",  # Don't support standalone controller at this moment
            "Welcome to APIC Setup Utility": "\n",
            "Enter the IP Address of default gateway": self.apic_gateway,
            "Enter the IP Address": f"{self.apic_address}/{self.apic_netmask}",
        }

        self.logger.debug("APIC CIMC tool initialized successfully.")

    def _api_base_request(self, data):
        """Send POST request to the CIMC API."""

        try:
            cimc_url = f"https://{self.cimc_address}/nuova"
            headers = {
                "accept": "*/*",
                "Content-Type": "text/html",
            }

            response = requests.post(
                url=cimc_url, headers=headers, data=data, verify=False
            )

            if response.status_code == 200:
                self.logger.debug(
                    f"CIMC API request successfully with status code '{response.status_code}'. Data sent: {data}"
                )
                return response
            else:
                self.logger.error(
                    f"CIMC API request failed with status code '{response.status_code}'. Data sent: {data}"
                )
                return False

        except Exception as e:
            self.logger.error(
                f"Exception occurred during CIMC API request. Error: {str(e)}, Data: {data}"
            )
            self.logger.error(traceback.format_exc())
            return False

    def _api_login(self):
        """Login CIMC API and retrieve authentication token."""
        try:
            data = (
                f"<aaaLogin inName='{self.apic_cimc_username}' "
                f"inPassword='{self.apic_cimc_password}'>"
                f"</aaaLogin>"
            )

            for i in range(1, 4):
                response = self._api_base_request(data)
                if response:
                    self.token = ET.fromstring(response.text).attrib.get("outCookie")

                    if self.token:
                        self.logger.debug(
                            f"Login successfully to CIMC '{self.cimc_address}' via API. Token: '{self.token}'"
                        )
                        return self.token
                    else:
                        self.logger.debug(
                            f"Login failed to CIMC '{self.cimc_address}' via API: No token received. Retry = {i}"
                        )
                else:
                    self.logger.debug(
                        f"Login request to CIMC '{self.cimc_address}' failed: No response. Retry = {i}"
                    )
                time.sleep(3)

        except Exception as e:
            self.logger.error(
                f"Exception occurred during CIMC login for '{self.cimc_address}': {str(e)}"
            )
            self.logger.error(traceback.format_exc())

        self.logger.error(
            f"Failed to connect to '{self.cimc_address}' with both API methods after 3 attempts!"
        )
        return None

    def _api_logout(self):
        try:
            data = (
                f"<aaaLogout cookie='{self.token}' inCookie='{self.token}'></aaaLogout>"
            )
            response = self._api_base_request(data)
            if response:
                self.logger.debug(
                    f"Successfully logged out from CIMC '{self.cimc_address}' with token '{self.token}'."
                )
                return True
            else:
                self.logger.error(
                    f"Logout request to CIMC '{self.cimc_address}' failed!"
                )
        except Exception as e:
            self.logger.error(
                f"Exception occurred during CIMC logout for '{self.cimc_address}': {str(e)}"
            )
            self.logger.error(traceback.format_exc())

        return False

    def _api_health_check(self):
        """
        Perform health check on the CIMC by retrieving and logging key system information.
        """
        try:
            # Retrieve firmware information
            firmware_data = f"""
            <!-- Request firmware version -->
            <configResolveDn cookie="{self.token}" inHierarchical='false'
            dn="sys/rack-unit-1/mgmt/fw-system"/>
            """
            firmware_response = self._api_base_request(firmware_data)

            if firmware_response:
                firmware_version = (
                    ET.fromstring(firmware_response.text)
                    .find(".//firmwareRunning")
                    .attrib["version"]
                )
                self.logger.debug(f"Current Firmware version: {firmware_version}")
            else:
                self.logger.error(
                    f"Failed to retrieve firmware version from CIMC {self.cimc_address}."
                )
                return False

            # Retrieve fault information
            fault_data = f"""
            <!-- Request fault information -->
            <configResolveClass cookie="{self.token}" inHierarchical='false' classId='faultInst'/>
            """
            self.logger.debug(
                f"Retrieving fault information for CIMC {self.cimc_address}:"
            )
            fault_response = self._api_base_request(fault_data)

            if fault_response:
                self.logger.debug(f"Fault information: {fault_response.text}")
            else:
                self.logger.error(
                    f"Failed to retrieve fault information from CIMC {self.cimc_address}."
                )
                return False

            # Retrieve TPM status
            tpm_data = f"""
            <!-- Request TPM status -->
            <configResolveClass cookie="{self.token}" inHierarchical='false' classId='equipmentTpm'/>
            """
            tpm_response = self._api_base_request(tpm_data)

            if tpm_response:
                tpm_status = (
                    ET.fromstring(tpm_response.text)
                    .find(".//equipmentTpm")
                    .attrib["enabledStatus"]
                )
                self.logger.debug(f"Current TPM status: {tpm_status}")
            else:
                self.logger.error(
                    f"Failed to retrieve TPM status from CIMC {self.cimc_address}."
                )
                return False

            # Check if TPM is enabled
            if "enable" not in tpm_status:
                self.logger.error(f"CIMC {self.cimc_address}: TPM is not enabled!")
                return False

            self.logger.debug(f"CIMC: '{self.cimc_address}' passed CIMC health check.")
            return True

        except Exception as e:
            # Log any exceptions that occur during the health check
            self.logger.error(
                f"Exception occurred during CIMC health check for {self.cimc_address}: {str(e)}"
            )
            self.logger.error(traceback.format_exc())
            return False

    def _api_clear_mapping(self):
        """Clear existing CIMC virtual media mappings and boot order."""

        try:
            # Retrieve current CIMC media mappings
            cimc_mapping_data = f"""
            <!-- Request CIMC media mappings -->
            <configResolveClass cookie="{self.token}" inHierarchical='false' classId='commVMediaMap'/>
            """
            cimc_mapping_response = self._api_base_request(cimc_mapping_data)

            # Check if a virtual media mapping exists and remove it
            if cimc_mapping_response and re.search(
                r"commVMediaMap volumeName", cimc_mapping_response.text
            ):
                existing_mapping = (
                    ET.fromstring(cimc_mapping_response.text)
                    .find(".//commVMediaMap")
                    .attrib["volumeName"]
                )
                self.logger.debug(
                    f"Found existing virtual media mapping: {existing_mapping}. Removing it."
                )

                # Clear the existing virtual media mapping
                cimc_mapping_clear_data = f"""
                <!-- Clear CIMC media mapping -->
                <configConfMo cookie="{self.token}">
                    <inConfig>
                        <commVMediaMap
                        dn="sys/svc-ext/vmedia-svc/vmmap-{existing_mapping}"
                        volumeName="{existing_mapping}" status='removed'/>
                    </inConfig>
                </configConfMo>
                """
                cimc_mapping_clear_response = self._api_base_request(
                    cimc_mapping_clear_data
                )

                if cimc_mapping_clear_response:
                    self.logger.debug(
                        f"Successfully removed virtual media mapping: '{existing_mapping}'."
                    )
                else:
                    self.logger.error(
                        f"Failed to remove virtual media mapping: '{existing_mapping}'!"
                    )
                    return False
            else:
                self.logger.debug("No existing virtual media mapping found.")

            # Retrieve current CIMC boot order
            cimc_boot_data = f"""
            <!-- Request CIMC boot order -->
            <configResolveClass cookie="{self.token}" inHierarchical='false' classId='lsbootVMedia'/>
            """
            cimc_boot_data_response = self._api_base_request(cimc_boot_data)

            # Check if a boot order exists and remove it
            if cimc_boot_data_response and re.search(
                r"lsbootVMedia name", cimc_boot_data_response.text
            ):
                existing_bootorder = (
                    ET.fromstring(cimc_boot_data_response.text)
                    .find(".//lsbootVMedia")
                    .attrib["name"]
                )
                self.logger.debug(
                    f"Found existing boot order: '{existing_bootorder}'. Removing it."
                )

                # Clear the existing boot order
                cimc_bootorder_clear_data = f"""
                <!-- Clear CIMC boot order -->
                <configConfMo cookie="{self.token}">
                    <inConfig>
                        <lsbootVMedia
                        dn="sys/rack-unit-1/boot-precision/vm-{existing_bootorder}"
                        name="{existing_bootorder}" status='removed'/>
                    </inConfig>
                </configConfMo>
                """
                cimc_bootorder_clear_response = self._api_base_request(
                    cimc_bootorder_clear_data
                )

                if cimc_bootorder_clear_response:
                    self.logger.debug(
                        f"Successfully removed boot order: {existing_bootorder}."
                    )
                else:
                    self.logger.error(
                        f"Failed to remove boot order: {existing_bootorder}!"
                    )
                    return False
            else:
                self.logger.debug("No existing boot order found.")

            return True

        except Exception as e:
            # Log any exceptions that occur during the clearing process
            self.logger.error(
                f"Exception occurred during CIMC mapping/boot order clear for {self.cimc_address}: {str(e)}"
            )
            self.logger.error(traceback.format_exc())
            return False

    def _api_power_on_cimc(self):
        """Power on CIMC."""
        try:
            cimc_power_on_data = f"""
            <!-- Request to power on CIMC -->
            <configConfMo cookie="{self.token}">
                <inConfig>
                    <computeRackUnit dn="sys/rack-unit-1" adminPower="up"/>
                </inConfig>
            </configConfMo>
            """

            cimc_power_on_response = self._api_base_request(cimc_power_on_data)

            if cimc_power_on_response:
                self.logger.debug(
                    f"CIMC '{self.cimc_address}' has been successfully powered on."
                )
                return True
            else:
                self.logger.error(f"Failed to power on CIMC '{self.cimc_address}'!")

        except Exception as e:
            # Log any exceptions that occur during the power on process
            self.logger.error(
                f"Exception occurred while powering on CIMC '{self.cimc_address}': {str(e)}"
            )
            self.logger.error(traceback.format_exc())

        return False

    def _api_power_down_cimc(self):
        """Power down CIMC."""
        try:
            cimc_power_down_data = f"""
            <!-- Request to power down CIMC -->
            <configConfMo cookie="{self.token}">
                <inConfig>
                    <computeRackUnit dn="sys/rack-unit-1" adminPower="down" />
                </inConfig>
            </configConfMo>
            """

            cimc_power_down_response = self._api_base_request(cimc_power_down_data)

            if cimc_power_down_response:
                self.logger.debug(
                    f"CIMC '{self.cimc_address}' has been successfully powered down."
                )
                return True
            else:
                self.logger.error(f"Failed to power down CIMC: '{self.cimc_address}'!")

        except Exception as e:
            # Log any exceptions that occur during the power down process
            self.logger.error(
                f"Exception occurred while powering on CIMC '{self.cimc_address}': {str(e)}"
            )
            self.logger.error(traceback.format_exc())

        return False

    def _api_bootstrap_6x(self):
        """API bootstrap method for 6.x"""

        login_url = f"https://{self.apic_address}/api/workflows/v1/login"
        login_data = {
            "username": self.aci_local_username,
            "password": self.aci_local_password,
            "domain": "DefaultAuth",
        }
        jwt_token = ""
        for i in range(1, 4):
            try:
                login_res = requests.post(login_url, json=login_data, verify=False)
                if login_res.status_code == 200:
                    jwt_token = login_res.json()["jwttoken"]
                    self.logger.debug(
                        f"Login APIC bootstrap API successfully, jwt_token: {jwt_token}"
                    )
                    break
                else:
                    time.sleep(5)
                    self.logger.debug(
                        f"Login APIC bootstrap API failed: '{self.apic_address}' , Retry = {i}"
                    )
                    self.logger.debug(login_res.text)
            except Exception as e:
                self.logger.debug(
                    f"Login APIC bootstrap API failed: '{self.apic_address}' , Retry = {i}"
                )
                self.logger.debug(
                    f"Exception occurred during CIMC health check for {self.cimc_address}: {str(e)}"
                )
                self.logger.debug(traceback.format_exc())
                time.sleep(5)

        if not jwt_token:
            self.logger.error(
                f"Bootstrap API login failed after 3 attempts: {self.apic_address}"
            )
            return False

        bootstrap_headers = {"Cookie": f"APIC-cookie={jwt_token}"}
        bootstrap_url = (
            f"https://{self.apic_address}/api/workflows/v1/cluster/bootstrap"
        )

        bootstrap_data = {
            "cluster": {
                "fabricName": self.fabric_name,
                "fabricId": int(self.fabric_id),
                "clusterSize": int(self.fabric_active_controllers),
                "layer3": False,
                "gipoPool": self.gipo,
                "adminPassword": self.aci_local_password,
                "infraVlan": int(self.infra_vlan),
            },
            "nodes": [],
            "pods": [{"podId": 1, "tepPool": self.tep_pool}],
        }
        for item in self.apics:
            node = {
                "nodeName": item.get("hostname"),
                "controllerType": "physical",
                "serialNumber": item.get("serial_number"),
                "nodeId": int(item.get("id")),
                "podId": int(item.get("pod")),
                "cimc": {
                    "address4": item.get("cimc_address"),
                    "username": self.apic_cimc_username,
                    "password": self.apic_cimc_password,
                },
                "oobNetwork": {
                    "address4": f"{item.get('apic_address')}/{self.apic_netmask}",
                    "gateway4": self.apic_gateway,
                    "enableIPv4": True,
                    "enableIPv6": False,
                    "address6": "",
                    "gateway6": "",
                },
            }

            bootstrap_data["nodes"].append(node)

        self.logger.debug(f"Bootstrap API data: {bootstrap_data}")

        bootstrap_res = requests.post(
            bootstrap_url, headers=bootstrap_headers, json=bootstrap_data, verify=False
        )
        if bootstrap_res.status_code != 200:
            self.logger.error(
                f"Bootstrap config failed due to api error: {bootstrap_url} || {bootstrap_res.text}"
            )
            return False

        wait_time = 600
        start_time = time.time()
        time.sleep(5)

        while time.time() - start_time <= wait_time:
            try:
                check_res = requests.get(
                    bootstrap_url,
                    headers=bootstrap_headers,
                    json=bootstrap_data,
                    verify=False,
                )
            except Exception as e:
                self.logger.error(f"Getting bootstrap failed duo to api error: {e}")
                self.logger.error(traceback.format_exc())
                return False

            if check_res.status_code != 200:
                self.logger.error(
                    f"API error when getting bootstrap status: {bootstrap_url}"
                )
                return False

            check_result = check_res.json()
            status = check_result["status"]
            progress = status.get("progress")
            state = status.get("state")

            if progress == 0 and state == "Pending":
                self.logger.error("No bootstrap config found!")
                return False

            if progress == 100 and state == "Completed":
                self.logger.debug(f"APIC: {self.hostname} API bootstrap successfully.")
                metadata.datacenter.APIC_DISCOVER_SKIP_FLAG = True
                return True

            self.logger.debug(
                f"API bootstrap check info - progress: {progress} || state: {state}"
            )

            time.sleep(30)

        self.logger.error(f"Bootstrap not finished in {wait_time} seconds! Failed.")
        return False

    def _validate_apic_image(self):
        """Validate APIC image"""
        self.logger.debug("Validating APIC image...")

        pattern = r"(?:aci-apic-dk9\.)(\d+\.\d+\.\d+[a-z])\.iso"
        version_match = re.search(pattern, self.apic_image)

        if version_match:
            self.logger.debug(
                f"Validate version: '{version_match.group(1)}' successfully."
            )
            return True
        else:
            self.logger.error(f"Invalid APIC image: {self.apic_image}")
            return False

    def api_validate_apic(self):
        """
        Validate CIMC for APIC installation by performing the following steps:
        1. Validate APIC image.
        2. Login CIMC via SSH.
        3. Login CIMC via API.
        4. Perform CIMC health check.
        5. Clear any existing virtual media mappings.
        6. Power down CIMC.
        """

        self.logger.debug("Validating APIC Image for APIC installation...")

        if not self._validate_apic_image():
            self.logger.error("Validate APIC Image failed!")
            return False

        self.logger.debug("Validating CIMC for APIC installation...")

        if not self._ssh_connect():
            self.logger.error("Validating CIMC failed due to SSH login failed@")
            return False
        else:
            self._ssh_disconnect()

        if not self._api_login():
            self.logger.error("Validating CIMC failed due to API login failed!")
            return False

        try:
            if not self._api_health_check():
                self.logger.error("CIMC health check failed!")
                return False
            self.logger.debug("CIMC health check passed.")

            if not self._api_clear_mapping():
                self.logger.error("CIMC mapping cleanup failed!")
                return False
            self.logger.debug("CIMC mapping cleanup successfully.")

            self.logger.debug("Powering down CIMC...")
            if not self._api_power_down_cimc():
                self.logger.error("Failed to power down CIMC.")
                return False

            self.apic_workflow = 1
            self.logger.debug("Validated CIMC for APIC installation successfully.")
            return True

        except Exception as e:
            # Log any exceptions that occur during the validation process
            self.logger.error(
                f"Exception occurred during CIMC validation for APIC: {str(e)}"
            )
            self.logger.error(traceback.format_exc())

        finally:
            self._api_logout()

        return False

    def api_install_apic(self):
        """
        Configure installation parameters by performing the following steps:
        1. Login CIMC via API.
        2. Configure following configurations on CIMC:
            - hostname
            - description
            - timezone
            - NTP
            - Serial Over LAN(SOL)
            - CIMC mapping
            - boot order
            - Disable CIMC LLDP
            - Update CIMC power restore policy
        3. Power on CIMC.
        """

        # APIC validation is required before api installation
        if self.apic_workflow != 1:
            self.logger.error("APIC Validation is not performed, aborting...")
            return False

        self.logger.debug("Configure APIC installation via CIMC-MAP.")

        # Step 1: Login CIMC via api
        if not self._api_login():
            self.logger.error(
                "Configure APIC installation failed due to API login failed!"
            )
            return False
        try:
            # Define CIMC installation steps
            cimc_install_data = {
                "Configure hostname": f"""
                    <configConfMo cookie="{self.token}"><inConfig>
                        <mgmtIf dn="sys/rack-unit-1/mgmt/if-1" hostname="{self.hostname}"/>
                    </inConfig></configConfMo>
                """,
                "Configure description": f"""
                    <configConfMo cookie="{self.token}"><inConfig>
                        <computeRackUnit dn="sys/rack-unit-1" usrLbl="{self.description}"/>
                    </inConfig></configConfMo>
                """,
                "Configure timeZone": f"""
                    <configConfMo cookie="{self.token}"><inConfig>
                        <topSystem dn="sys" timeZone="{self.timezone}"/>
                    </inConfig></configConfMo>
                """,
                "Configure NTP": f"""
                    <configConfMo cookie="{self.token}"><inConfig>
                        <commNtpProvider dn="sys/svc-ext/ntp-svc" ntpServer1="{self.ntp_server}"/>
                    </inConfig></configConfMo>
                """,
                "Configure SOL (Serial Over LAN)": f"""
                    <configConfMo cookie="{self.token}"><inConfig>
                        <solIf dn="sys/rack-unit-1/sol-if" adminState="enable" speed="115200"
                            comport="com0" sshPort="2400"/>
                    </inConfig></configConfMo>
                """,
                "Configure CIMC mapping for APIC image": f"""
                    <configConfMo cookie="{self.token}"><inConfig>
                        <commVMediaMap volumeName="aci-automation" map="www"
                                    remoteShare="{self.aci_image_path}" remoteFile="{self.apic_image}"
                                    dn="sys/svc-ext/vmedia-svc/vmmap-aci-automation"/>
                    </inConfig></configConfMo>
                """,
                "Set CIMC boot order to CIMC-map": f"""
                    <configConfMo cookie="{self.token}"><inConfig>
                        <lsbootVMedia dn="sys/rack-unit-1/boot-precision/vm-cimc-map"
                                    name="cimc-map" type="VMEDIA" subtype="cimc-mapped-dvd"
                                    order="1" state="Enabled"/>
                    </inConfig></configConfMo>
                """,
                "Disable LLDP": f"""
                    <configConfMo cookie="{self.token}"><inConfig>
                        <adaptorGenProfile dn="sys/rack-unit-1/adaptor-1/general" lldp="disabled"/>
                    </inConfig></configConfMo>
                """,
                "Update power restore policy": f"""
                    <configConfMo cookie="{self.token}"><inConfig>
                        <biosVfResumeOnACPowerLoss dn="sys/rack-unit-1/board/Resume-on-AC-power-loss" vpResumeOnACPowerLoss="reset"/>
                    </inConfig></configConfMo>
                """,
            }

            # Step 2: Execute each configuration step in the CIMC installation process
            for step_name, config_data in cimc_install_data.items():
                cimc_install_response = self._api_base_request(config_data)
                if cimc_install_response:
                    self.logger.debug(f"{step_name} completed successfully.")
                else:
                    self.logger.error(f"{step_name} failed!")
                    return False  # Exit if any step fails

            # Step 3: All steps succeeded, power on CIMC
            self.logger.debug("Powering on CIMC...")
            if not self._api_power_on_cimc():
                self.logger.error("Failed to power on CIMC.")
                return False

            self.apic_workflow = 2
            self.logger.debug(
                "CIMC-MAP configured successfully, ready to install APIC via SSH speed up..."
            )
            return True

        except Exception as e:
            # Log any exceptions that occur during the installation process
            self.logger.error(
                f"Exception occurred during configure CIMC-MAP for {self.cimc_address}: {str(e)}"
            )
            self.logger.error(traceback.format_exc())

        finally:
            self._api_logout()

        return False

    def _ssh_connect(self):
        """SSH Connector"""

        DEVICE_TYPES = [
            "linux",
            "generic",
        ]
        for i in range(1, 4):
            for device_type in DEVICE_TYPES:
                try:
                    self.logger.debug(
                        f"Attempting to connect '{self.cimc_address}' with '{device_type}'..."
                    )
                    self.device_ssh["device_type"] = device_type
                    self.ssh_connection = ConnectHandler(**self.device_ssh)
                    self.logger.debug(
                        f"Connected to '{self.cimc_address}': with '{device_type}' successfully."
                    )
                    return True
                except Exception as e:
                    self.logger.debug(
                        f"Failed to connect to '{self.cimc_address}' with '{device_type}': {e}"
                    )
                    self.logger.debug(traceback.format_exc())
                    time.sleep(3)

            self.logger.debug(
                f"Failed to connect to '{self.cimc_address}' with both methods! Retry = {i}"
            )

        self.logger.error(
            f"Failed to connect to '{self.cimc_address}' with both SSH methods after 3 attempts!"
        )
        return False

    def _ssh_disconnect(self):
        if self.ssh_connection:
            self.ssh_connection.disconnect()
            self.logger.debug(f"Disconnected SSH connection for: {self.cimc_address}")
            return True
        else:
            self.logger.error(f"No ssh connection found: {self.cimc_address}")
            return False

    def ssh_install_apic(self):
        """Monitor and accelerate APIC installation via CIMC SSH"""

        # API installation is required before ssh installation
        if self.apic_workflow != 2:
            self.logger.error("APIC API installation is not performed, aborting...")
            return False

        self.logger.debug(
            "Start APIC installation monitoring and acceleration via CIMC SSH..."
        )

        if not self._ssh_connect():
            self.logger.error(
                "APIC installation monitoring and acceleration failed due to SSH login failed."
            )
            return False

        iso_url = f"{self.aci_image_path}{self.apic_image}"

        step_chain = [
            {
                "command": "connect host",
                "expect": "To speed up the install, enter iso url",
                "read_timeout": 900,
            },
            {
                "command": iso_url,  # http://10.124.145.88/Images/ACI/4/4.2/aci-apic-dk9.4.2.7f.iso
                "expect": "type static, dhcp, bash for a shell to configure networking",
                "read_timeout": 90,
            },
            {
                "command": "bash",
                "expect": r"bash-4.2#|root@\(none\):/#",
                "read_timeout": 90,
            },
        ]

        try:
            for item in step_chain:
                cmd = item.get("command")
                self.ssh_connection.send_command(
                    cmd, item.get("expect"), read_timeout=item.get("read_timeout")
                )
                self.logger.debug(f"Successfully execute command: {cmd}")

            interfaces = self.ssh_connection.send_command_timing(
                "ls -l /sys/class/net",
                read_timeout=30,
            )
            oob_interface = "eno1" if "/net/eno1" in interfaces else "enp1s0f0"
            self.logger.debug(f"Configure interface: {oob_interface}")

            bash_cmd = [
                f"ip addr add {self.apic_address}/{self.apic_netmask} dev {oob_interface}",
                f"ip link set {oob_interface} up",
                f"ip route add default via {self.apic_gateway}",
            ]

            self.ssh_connection.send_multiline_timing(bash_cmd)
            self.logger.debug("Interface configured, waiting for APIC installation...")

            output = self.ssh_connection.send_command(
                "exit",
                r"Enter the artifact URL \(empty if done\):|atomix installation complete|atomix-installer returned 0",
                read_timeout=3600,
                strip_prompt=False,
            )

            # version 5.x: Enter the artifact URL (empty if done):
            if "Enter the artifact URL (empty if done):" in output:
                self.ssh_connection.send_multiline_timing("\n")

                self.ssh_connection.read_until_pattern(
                    pattern="atomix installation complete", read_timeout=3600
                )

            self.ssh_connection.read_until_pattern(
                pattern="reboot: Power down", read_timeout=120
            )

            if not self._api_login():
                self.logger.error(
                    "CIMC mapping cleanup failed due to API login failed!"
                )
                return False

            if not self._api_clear_mapping():
                self.logger.error("CIMC mapping cleanup failed!")
                return False

            self.logger.debug("APIC installation successfully.")

            return True

        except Exception as e:
            # Log any exceptions that occur during the installation process
            self.logger.error(
                f"Exception occurred during APIC install acceleration for {self.cimc_address}: {str(e)}"
            )
            self.logger.error(traceback.format_exc())

        finally:
            self._ssh_disconnect()

        return False

    def _execute_init_command(self, out_msg, exist_old_config=False):
        for i in range(2):
            max_loop = 3 * len(self.apic_config_dict)
            while max_loop:
                max_loop -= 1
                if max_loop <= 0:
                    self.logger.error("Max loop reached, unknown failure!")
                    return False
                if "Would you like to edit the configuration?" in out_msg:
                    cmd = "\n"
                    if exist_old_config and i == 1:
                        cmd = "N"
                    self.ssh_connection.send_command_timing(cmd, read_timeout=15)
                    self.logger.debug("Complete APIC initial setup configuration.")
                    break
                if "Password is not strong enough" in out_msg:
                    self.logger.error(
                        "APIC required a strong password, but simple password provided in '00-global_policy!'"
                    )
                    return False
                else:
                    matched = False
                    self.logger.debug(f"out_msg_loop: {out_msg}")
                    for key, value in self.apic_config_dict.items():
                        if key in out_msg:
                            out_msg = self.ssh_connection.send_command_timing(
                                value, last_read=5, read_timeout=15, strip_prompt=False
                            )
                            matched = True
                            break
                    if not matched:
                        self.logger.error(
                            f"APIC setup key/value match error, output msg: {out_msg}"
                        )
                        return False


    def ssh_init_apic(self):
        """Configure APIC initial setup parameters via CIMC SSH"""
        # TBD: Enhance more ACI fabric scenarios...

        self.logger.debug("Starting to initial setup APIC via CIMC SSH...")



        if not self._api_login():
            self.logger.error("APIC initial setup failed due to API login failed!")
            return False

        try:
            self.logger.debug("Powering on CIMC...")
            if not self._api_power_on_cimc():
                self.logger.error("Failed to power on CIMC!")
                return False
        except Exception as e:
            # Log any exceptions that occur during the CIMC power on process
            self.logger.error(
                f"Exception occurred during powering on CIMC for {self.cimc_address}: {str(e)}"
            )
            self.logger.error(traceback.format_exc())
            return False
        finally:
            self._api_logout()

        if not self._ssh_connect():
            self.logger.error("APIC initial setup failed due to SSH login failed!")
            return False

        exist_old_config = False
        try:
            # key = ("datacenter", "aci", "clear_configuration")
            # connect_host_expect_pattern = "|".join(self.apic_config_dict.keys()) + "|Press any key to continue..."
            apic_config_list = list(self.apic_config_dict.keys())
            apic_config_list.remove("Enter the fabric name")
            connect_host_expect_pattern = "|".join(apic_config_list)
            output = self.ssh_connection.send_command_timing(
                "connect host",
                last_read=60,
                read_timeout=900
            )

            if re.search(connect_host_expect_pattern, output):
                exist_old_config = True

            # if key not in context_cache.tasks:
            #     output = self.ssh_connection.send_command(
            #         "connect host",
            #         connect_host_expect_pattern,
            #         read_timeout=900,
            #     )
            #     if re.search("|".join(self.apic_config_dict.keys())):
            #         exist_old_config = True
            # else:
            #     self.ssh_connection.send_command("connect host", read_timeout=900)
            ###### Loop method

            if not exist_old_config:
                out_pattern = "Enter the fabric name|Press Enter Or Input JSON string"
                out_msg = self.ssh_connection.send_command_timing("\n", read_timeout=10, strip_prompt=False)
                if not re.search(out_pattern, out_msg):
                    self.logger.debug("Did not match the target pattern after send_command_timing.")
                    out_msg += self.ssh_connection.read_until_pattern(
                        out_pattern,
                        read_timeout=300,
                    )
                else:
                    self.logger.debug("Matched the target pattern after send_command_timing.")

                self.logger.debug(f"Init output message phase1: {out_msg}")
                # For version 6.x
                if "Press Enter Or Input JSON string" in out_msg:
                    out_msg = self.ssh_connection.send_command(
                        "\n",
                        "Enter the password for admin",
                        read_timeout=60,
                        strip_prompt=False,
                    )
                    self.logger.debug(f"Init output message phase2: {out_msg}")

            self._execute_init_command(exist_old_config=exist_old_config, out_msg=out_msg)
            # Post Check
            pattern = f"{self.hostname} login|System pre-configured successfully"
            result = self.ssh_connection.read_until_pattern(
                pattern=pattern, read_timeout=180
            )
            self.logger.debug(f"APIC init result: {result}")

            # For version 6.x
            if "System pre-configured successfully" in result:
                self.logger.debug(
                    f"APIC System pre-configured successfully for ACI 6.x, go to 'https://{self.apic_address}' to complete the bootstrapping!"
                )
                if not self._api_bootstrap_6x():
                    self.logger.error("APIC initial setup failed!")
                    return False
                self.ssh_connection.read_until_pattern(
                    pattern=f"{self.hostname} login", read_timeout=300
                )

            self.logger.debug("APIC initial setup successfully.")

            return True

        except Exception as e:
            # Log any exceptions that occur during the APIC initial setup process
            self.logger.error(
                f"Exception occurred during APIC initial setup for '{self.cimc_address}': {str(e)}"
            )
            self.logger.error(traceback.format_exc())

        finally:
            self._ssh_disconnect()

        return False

    def gen_install_apic(self):
        """
        Complete APIC installation workflow:
        1. Configure installation parameters via CIMC API
        2. Monitor and accelerate APIC installation via CIMC SSH
        """
        self.logger.debug("Start to run APIC installation workflow...")

        if not self.api_install_apic():
            self.logger.error(f"APIC {self.hostname} API installation phase failed!")
            return False

        self.logger.debug(
            f"APIC '{self.hostname}' API installation phase completed successfully."
        )

        if not self.ssh_install_apic():
            self.logger.error(f"APIC {self.hostname} SSH installation phase failed!")
            return False

        self.logger.debug(
            f"APIC '{self.hostname}' SSH installation phase completed successfully."
        )

        self.logger.debug(
            f"APIC '{self.hostname}' had been successfully installed to '{self.apic_image}'."
        )

        return True

    def ssh_clear_config(self):
        self.logger.debug("Start clear cimc config.")
        if not self.ssh_connection:
            if not self._ssh_connect():
                self.logger.error(f"Connect failed, clear config failed.")
                return False

        if not self._api_login():
            self.logger.error("Clear configuration failed due to API login failed!")
            return False

        try:
            self.logger.debug("Powering on CIMC...")
            if not self._api_power_on_cimc():
                self.logger.error("Failed to power on CIMC!")
                return False
        except Exception as e:
            # Log any exceptions that occur during the CIMC power on process
            self.logger.error(
                f"Exception occurred during powering on CIMC for {self.cimc_address}: {str(e)}"
            )
            self.logger.error(traceback.format_exc())
            return False
        finally:
            self._api_logout()

        try:
            output = self.ssh_connection.send_command(
                "connect host",
                "#|login|to Exit the session",
                read_timeout=900,
            )

            if "to Exit the session" in output:
                output = self.ssh_connection.send_command_timing(
                    "\n",
                    strip_prompt=False,
                    read_timeout=30,
                    delay_factor=30
                )

            for config_str in self.apic_config_dict:
                if config_str in output:
                    self.logger.warning("The device may have already been cleared of its configuration.")
                    return True

            if "login" in output:
                output = self.ssh_connection.send_command_timing(
                    self.aci_local_username,
                    strip_prompt=False,
                    read_timeout=30,
                    delay_factor=30
                )

                if "Password" in output:
                    output = self.ssh_connection.send_command_timing(
                        self.aci_local_password,
                        strip_prompt=False,
                        read_timeout=30,
                        delay_factor=30
                    )

            command_list = [
                ("acidiag touch clean", "This command will wipe out this device, Proceed?"),
                ("acidiag touch setup", "This command will reset the device configuration, Proceed?"),
                ("acidiag reboot", "This command will restart this device, Proceed?")
            ]
            for command, expect_str in command_list:
                output = self.ssh_connection.send_command_timing(
                    command,
                    strip_prompt=False,
                    delay_factor=30
                )
                if expect_str in output:
                    self.ssh_connection.send_command_timing('y', read_timeout=30)

            self.logger.info("command executed successfully.")
            self.ssh_connection.read_until_pattern(
                pattern=r"Press any key to continue", read_timeout=300
            )

            # key = ("datacenter", "aci", "apic_init_setup")
            # if key not in context_cache.tasks:
            #     self.logger.info("Matched expect: Press any key to continue, start power down cimc.")
            #     if not self._api_power_down_cimc():
            #         self.logger.error("Failed to power down CIMC.")
            #         return False
            # else:
            self.logger.info("Matched expect: Press any key to continue, Finished.")
            return True
        except Exception as e:
            self.logger.error(
                f"Exception occurred during clearing config for '{self.cimc_address}'"
            )
            self.logger.error(traceback.format_exc())
        finally:
            self._ssh_disconnect()

        return False
