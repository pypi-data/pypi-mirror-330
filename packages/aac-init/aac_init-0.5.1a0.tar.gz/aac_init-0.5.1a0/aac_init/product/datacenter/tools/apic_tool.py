# -*- coding: utf-8 -*-

# Copyright: (c) 2024, Rudy Lei <shlei@cisco.com>

import urllib3
import requests
import json
import traceback

from aac_init.log_utils import LazyLogger, netmiko_session_logger
from aac_init.tools import AnsibleTool
from time import sleep

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class ApicTool:
    """APIC Toolkits, include API and SSH."""

    def __init__(self, global_policies: dict, apic_connection: dict):
        for k, v in global_policies.items():
            setattr(self, k, v)
        for k, v in apic_connection.items():
            setattr(self, k, v)
        self.logger = LazyLogger(f"apictool_{self.hostname}.log")
        self.device_ssh = {
            "host": self.apic_address,
            "username": self.aci_local_username,
            "password": self.aci_local_password,
            "fast_cli": False,  # Disable fast CLI to mimic human-like sending
            "session_log": netmiko_session_logger(f"ssh_session_{self.hostname}.log"),
            "session_log_file_mode": "append",
        }
        self.token = None
        self.ssh_connection = None

        self.logger.debug("APIC tool initialized successfully.")

    # TODO: Need to enhance AAA scenario in further release.
    def _api_login(self):
        """Login APIC API and retrieve authentication token."""

        headers = {
            "accept": "application/json",
            "Content-Type": "application/json",
        }

        try:
            apic_login_url = f"https://{self.apic_address}/api/aaaLogin.json"

            data = {
                "aaaUser": {
                    "attributes": {
                        "name": self.aci_local_username,
                        "pwd": self.aci_local_password,
                    }
                }
            }

            for i in range(1, 4):
                response = requests.post(
                    url=apic_login_url,
                    headers=headers,
                    data=json.dumps(data),
                    verify=False,
                )
                if response.status_code == 200:
                    res_json = response.json()
                    self.token = res_json["imdata"][0]["aaaLogin"]["attributes"][
                        "token"
                    ]

                    if self.token:
                        self.logger.debug(
                            f"Login successfully to APIC '{self.apic_address}' via API. Token: {self.token}"
                        )
                        return self.token
                    else:
                        self.logger.debug(
                            f"Login failed to APIC '{self.apic_address}': No token received. Retry = {i}"
                        )
                else:
                    self.logger.debug(
                        f"Login request to APIC '{self.apic_address}' failed: No response. Retry = {i}"
                    )
                    self.logger.debug(f"Login request info: \nstatus code: {response.status_code}\n content: {response.content}")
                sleep(5)

        except Exception as e:
            self.logger.error(
                f"Exception occurred during APIC login for '{self.apic_address}': {str(e)}"
            )
            self.logger.error(traceback.format_exc())

        self.logger.error(
            f"Failed to connect to '{self.apic_address}' after 3 attempts!"
        )
        return None

    def _api_logout(self):
        pass

    def _ansible_run_playbook(self, playbook_path, inventory_path, output_path, stage):
        aac_ansible = AnsibleTool(output_path)
        return aac_ansible.ansible_runner(stage, playbook_path, inventory_path)

    def _api_health_check(self):
        """
        Perform health check on the API by retrieving and logging key system information.
        """

        self.logger.debug("Performing APIC health check...")
        health_status = []

        try:
            headers = {
                "accept": "application/json",
                "Content-Type": "application/json",
                "Cookie": f"APIC-cookie={self.token}",
            }
            apic_health_url = (
                f"https://{self.apic_address}/api/node/class/infraWiNode.json"
            )

            response = requests.get(url=apic_health_url, headers=headers, verify=False)

            if response.status_code == 200:
                return_data = response.json()
                for item in return_data["imdata"]:
                    health_status.append(item["infraWiNode"]["attributes"]["health"])
                for status in health_status:
                    if status != "fully-fit":
                        self.logger.error(
                            f"APIC '{self.hostname}' Health Check failed (Not fully-fit)!"
                        )
                        return False

                self.logger.debug(
                    f"APIC '{self.hostname}' Health Check successfully (Fully-fit)!"
                )
                return True

        except Exception as e:
            # Log any exceptions that occur during the health check
            self.logger.error(
                f"Exception occurred during APIC health check for {self.apic_address}: {str(e)}"
            )
            self.logger.error(traceback.format_exc())
            return False

    def api_validate_apic(self):
        """
        Validate APIC by performing the following steps:
        1. Login APIC via API.
        2. Perform APIC health check.
        """

        self.logger.debug("Validating APIC status...")

        if not self._api_login():
            self.logger.error("Validating APIC failed due to API login failed!")
            return False
        try:
            if not self._api_health_check():
                self.logger.error("APIC health check failed!")
                return False

            self.logger.debug("APIC validated successfully.")
            return True

        except Exception as e:
            # Log any exceptions that occur during the validation process
            self.logger.error(
                f"Exception occurred during APIC health check for {self.apic_address}: {str(e)}"
            )
            self.logger.error(traceback.format_exc())

        finally:
            self._api_logout()

        return False

    def ansible_validate(self, playbook_path, inventory_path, output_path):
        return self._ansible_run_playbook(playbook_path, inventory_path, output_path, "validate")

    def ansible_deploy(self, playbook_path, inventory_path, output_path):
        return self._ansible_run_playbook(playbook_path, inventory_path, output_path, "deploy")

    def ansible_test(self, playbook_path, inventory_path, output_path):
        return self._ansible_run_playbook(playbook_path, inventory_path, output_path, "test")
