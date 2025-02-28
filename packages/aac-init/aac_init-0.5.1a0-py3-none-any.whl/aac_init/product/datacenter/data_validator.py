from aac_init.control_engine.controller import controller

import os
import yamale
import traceback
from fnmatch import fnmatch
from pathlib import Path

from aac_init.control_engine.global_cache import context_cache
from aac_init.log_utils import LazyLogger
from aac_init.tools import YamlTool

logger = LazyLogger("datacenter_validator.log")


class DataCenterValidator:
    """
    Validators during CLI input stage.
    """

    def __init__(self, data_path: str, output_path: str):
        self.logger = logger

        self.logger.debug(
            f"CLI Validator initializing with data_path: '{data_path}', "
            f"output_path: '{output_path}'"
        )

        self.data_path = data_path
        self.output_path = output_path
        self.global_policy_path = None
        self.yaml_tool = YamlTool()
        self.selections = []
        self.default_global_policy_path = "00-global_policy.y*ml"
        self.default_fabric_mgmt_path = "01-fabric_mgmt.y*ml"
        self.default_nac_data_path = "nac_data"
        self.default_schemas_path = os.path.join(Path(__file__).resolve().parent, "schemas")

        self.logger.debug("CLI Validator initialized successfully.")

    def _validate_data_path(self):
        """Validate input data path"""

        self.logger.debug("Validating data path...")
        if not os.path.exists(self.data_path):
            msg = f"YAML Directory doesn't exist: {self.data_path}"
            self.logger.error(msg)
            return False, msg

        if not os.path.isdir(self.data_path):
            msg = f"{self.data_path} is not a directory!"
            self.logger.error(msg)
            return False, msg

        current_dir = os.getcwd()
        current_dir = os.path.abspath(current_dir)
        data_path = os.path.abspath(self.data_path)

        if os.path.commonpath([current_dir, data_path]) == data_path:
            msg = f"The current working directory cannot be the data_path or its subdirectory."
            self.logger.error(msg)
            return False, msg

        msg = f"Validate YAML directory: '{self.data_path}' successfully."
        self.logger.debug(msg)
        return True, msg

    def _validate_output_path(self):
        self.logger.debug("Validating data path...")
        current_working_dir = os.getcwd()

        abs_data_path = os.path.abspath(self.data_path)
        abs_output_path = os.path.abspath(self.output_path)

        if os.path.commonpath([abs_data_path, abs_output_path]) == abs_data_path:
            msg = f"The output directory cannot be the data_path or its subdirectory."
            return False, msg
        return True

    def _validate_syntax_file(self, file_path: str):
        """Validate the syntax of a single YAML file."""

        filename = os.path.basename(file_path)
        self.logger.debug(f"Validating file: {filename}")

        if not all([os.path.isfile(file_path), filename.endswith((".yaml", ".yml"))]):
            msg = f"{filename} is not a yaml file!"
            self.logger.error(msg)
            return False, msg

        # YAML syntax validation
        if self.yaml_tool.load_yaml_file(file_path):
            self.logger.debug(
                f"Validate the syntax of file: '{filename}' successfully."
            )
            return True
        else:
            msg = f"Validate the syntax of file: '{filename}' failed due to data error(empty or syntax issue)."
            self.logger.error(msg)
            return False, msg

    def _validate_yaml(self, default_global_policy_path=None):
        """Validate input yaml files"""

        self.logger.debug("Validating input yaml files...")
        if not default_global_policy_path:
            default_global_policy_path = self.default_global_policy_path
        data_path = os.path.abspath(self.data_path)
        global_policy_yaml_file_exist = False
        for dir, _, files in os.walk(data_path):
            for filename in files:
                self._validate_syntax_file(os.path.join(dir, filename))
                if fnmatch(filename, default_global_policy_path):
                    if os.path.abspath(dir) != data_path:
                        msg = "'00-global_policy' file cannot be in subdirectory!"
                        self.logger.error(msg)
                        return False, msg

                    self.global_policy_path = os.path.join(dir, filename)
                    if global_policy_yaml_file_exist:
                        msg = "Duplicated '00-global_policy' found!"
                        self.logger.error(msg)
                        return False, msg

                    global_policy_yaml_file_exist = True

        if self.global_policy_path:
            self.global_policy = self.yaml_tool.load_yaml_file(
                self.global_policy_path
            )
            self.logger.debug("'00-global_policy' loaded successfully.")
        else:
            self.global_policy = []
            msg = "'00-global_policy' is missing!"
            self.logger.error(msg)
            return False, msg

        self.logger.debug(f"Validate YAML files in: '{self.data_path}' successfully.")
        return True

    def _validate_global_policy(self, schemas_path=None):
        """Validate global policy per selection"""

        self.logger.debug("Validating global policy...")
        if not schemas_path:
            schemas_path = self.default_schemas_path

        fabric_policy = self.global_policy.get("fabric", {})
        apic_check = "apic_nodes_connection" in fabric_policy
        aci_switch_check = "switch_nodes_connection" in fabric_policy

        if "wipe_reimage" in self.selections and not any([apic_check, aci_switch_check]):
            msg = "Validate selection wipe_reimage failed: No APIC/Switch configuration provided!"
            self.logger.error(msg)
            return False, msg

        if "apic_init_setup" in self.selections and not apic_check:
            msg = "Validate Selection apic_init_setup failed: No APIC configuration provided!"
            self.logger.error(msg)
            return False, msg

        if "apic_nac_config" in self.selections and not apic_check:
            msg = "Validate Selection apic_nac_config failed: No APIC configuration provided!"
            self.logger.error(msg)
            return False, msg

        data = yamale.make_data(self.global_policy_path, parser="ruamel")
        schema_folder = os.path.join(schemas_path, "00-global_policy")

        # Need to pass at lease one schema
        for _, _, schema_files in os.walk(schema_folder):
            for schema_file in schema_files:
                self.logger.debug(
                    f"Validating schema: '{schema_file}' for global policy..."
                )
                schema_file_path = os.path.join(schema_folder, schema_file)
                try:
                    schema = yamale.make_schema(schema_file_path)
                    yamale.validate(schema, data)
                    self.logger.debug(f"Schema '{schema_file}' validated successfully.")
                    return True
                except ValueError as e:
                    self.logger.warning(f"Schema '{schema_file}' validated failed!")
                    self.logger.warning(e)
                except Exception as e:
                    self.logger.warning(f"Unknown exception: {e}")
                    self.logger.warning(traceback.format_exc())

        msg = """
            '00-global_policy' did not meet the requirements of any validation schema.
            This may be due to incorrect configuration in '00-global_policy',
            or it might be a new configuration scenario that is not supported by the current schema.
            If you confirm that your configuration is correct and represents a new scenario,
            please contact the shlei@cisco.com to update schema.
            """

        self.logger.error(msg)
        return False, msg

    def _validate_fabric_mgmt(self, fabric_mgmt_path=None, nac_data_path=None, schemas_path=None):
        """Validate fabric management for selection wipe_reimage - install ACI switch"""

        if "fabric_bootstrap" not in self.selections:
            self.logger.debug(
                "Skip fabric management validation due to 'wipe_reimage' is not selected."
            )
            return True

        self.logger.debug("Validating fabric management...")

        if not fabric_mgmt_path:
            fabric_mgmt_path = self.default_fabric_mgmt_path

        if not nac_data_path:
            nac_data_path = self.default_nac_data_path

        if not schemas_path:
            schemas_path = self.default_schemas_path
        data_path = os.path.abspath(self.data_path)
        nac_data_path = os.path.join(data_path, nac_data_path)
        fabric_mgmt_file = None

        if not all([os.path.exists(nac_data_path), os.path.isdir(nac_data_path)]):
            msg = "NaC path doesn't exist or not a folder!"
            self.logger.error(msg)
            return False, msg

        for item in os.listdir(nac_data_path):
            item_path = os.path.join(nac_data_path, item)
            if os.path.isfile(item_path) and fnmatch(item, fabric_mgmt_path):
                if fabric_mgmt_file:
                    msg = "Duplicated 01-fabric_mgmt found!"
                    self.logger.error(msg)
                    return False, msg
                fabric_mgmt_file = item_path
                self.logger.debug(f"fabric_mgmt_file path: {fabric_mgmt_file}")

        if not fabric_mgmt_file:
            msg = "01-fabric_mgmt is missing!"
            self.logger.error(msg)
            return False, msg

        data = yamale.make_data(fabric_mgmt_file, parser="ruamel")
        schema_folder = os.path.join(schemas_path, "01-fabric_mgmt")

        for _, _, schema_files in os.walk(schema_folder):
            for schema_file in schema_files:
                self.logger.debug(
                    f"Validating schema: '{schema_file}' for fabric management..."
                )
                schema_file_path = os.path.join(schema_folder, schema_file)
                try:
                    schema = yamale.make_schema(schema_file_path)
                    yamale.validate(schema, data)
                    self.logger.debug(f"Schema '{schema_file}' validated successfully.")
                    return True
                except ValueError as e:
                    self.logger.warning(f"Schema '{schema_file}' validated failed!")
                    self.logger.warning(e)
                except Exception as e:
                    self.logger.warning(f"Unknown exception: {e}")
                    self.logger.warning(traceback.format_exc())

            msg = """
            '01-fabric_mgmt' did not meet the requirements of any validation schema.
            This may be due to incorrect configuration in '01-fabric_mgmt',
            or it might be a new configuration scenario that is not supported by the current schema.
            If you confirm that your configuration is correct and represents a new scenario,
            please contact the shlei@cisco.com to update schema.
            """

            self.logger.error(msg)
            return False, msg

        # Merge global_policy and fabric_mgmt for switches
        fabric_mgmt_policy = self.yaml_tool.load_yaml_file(fabric_mgmt_file)
        self.logger.debug("01-fabric_mgmt loaded successfully.")

        fabric_mgmt_policy_apic = fabric_mgmt_policy.get("apic", {}) or {}
        fabric_mgmt_policy_apic_node_policies = (
            fabric_mgmt_policy_apic.get("node_policies", {}) or {}
        )
        fabric_mgmt_policy_apic_node_policies_nodes = (
            fabric_mgmt_policy_apic_node_policies.get("nodes", []) or []
        )
        fabric_mgmt_node_ids = set(
            i.get("id") for i in fabric_mgmt_policy_apic_node_policies_nodes
        )
        if len(fabric_mgmt_policy_apic_node_policies_nodes) != len(
            fabric_mgmt_node_ids
        ):
            msg = "Duplicated id found in '01-fabric_mgmt'!"
            self.logger.error(msg)
            return False, msg

        global_policy_fabric = self.global_policy.get("fabric", {}) or {}
        global_policy_switch_nodes_connection = (
            global_policy_fabric.get("switch_nodes_connection", []) or []
        )
        global_policy_switch_node_ids = set(
            i.get("id") for i in global_policy_switch_nodes_connection
        )
        if len(global_policy_switch_nodes_connection) != len(
            global_policy_switch_node_ids
        ):
            msg = "Duplicated id found in '00-global_policy'!"
            self.logger.error(msg)
            return False, msg

        if global_policy_switch_node_ids != fabric_mgmt_node_ids:
            msg = "Switch Nodes in '00-global_policy' and '01-fabric_mgmt' are not identical!"
            self.logger.error(msg)
            return False, msg

        self.logger.debug("Validate fabric management successfully.")
        return True

    def _validate_nac_data(self, nac_data_path=None):
        """Validate nac_data for selection apic_nac_config - ACI as Code"""

        if "apic_nac_config" not in self.selections:
            self.logger.debug("Skip NaC Data validation due to 'apic_nac_config' is not selected.")
            return True

        self.logger.debug("Validating NaC Data...")
        if not nac_data_path:
            nac_data_path = self.default_nac_data_path

        nac_data_path = os.path.join(self.data_path, nac_data_path)

        if not all([os.path.exists(nac_data_path), os.path.isdir(nac_data_path)]):
            msg = "NaC path doesn't exist or not a folder!"
            self.logger.error(msg)
            return False, msg

        nac_yaml_files = []
        for dir, _, files in os.walk(nac_data_path):
            for filename in files:
                nac_yaml_path = os.path.join(dir, filename)
                if nac_yaml_path:
                    nac_yaml_files.append(nac_yaml_path)

        if not nac_yaml_files:
            msg = f"No YAML file found in dir: '{nac_data_path}'"
            self.logger.error(msg)
            return False, msg

        self.logger.debug("NaC Data validated successfully.")
        return True

    def validate_cli_input(self):
        """Validate CLI input data files and selections"""

        self.logger.debug("Validating CLI input data files and selections...")
        validate_funcs = [
            self._validate_data_path,
            self._validate_output_path,
            self._validate_yaml,
            self._validate_global_policy,
            self._validate_fabric_mgmt,
            self._validate_nac_data,
        ]
        msg = None
        for validate_func in validate_funcs:
            validate_result = validate_func()
            if isinstance(validate_result, tuple):
                status, msg = validate_result
            else:
                status = validate_result
            if not status:
                self.logger.error("CLI inputs validated failed!")
                return False, msg

        self.logger.debug("CLI inputs validated successfully.")
        return True, msg


@controller.validator(project="datacenter", product="aci")
def validate(data_path, operations):
    output_path = context_cache.output_dir
    validator = DataCenterValidator(data_path, output_path)
    validator.selections = operations
    return validator.validate_cli_input()