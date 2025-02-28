import os
import traceback
from fnmatch import fnmatch
from ruamel import yaml
from pathlib import Path

from aac_init.tools.file_tools.yaml_tool import YamlTool
from aac_init.control_engine.global_cache import context_cache


def load_global_policy(data_path, logger, global_policy_path_pattern="00-global_policy.y*ml"):
    """Load global policy"""
    yaml_tool = YamlTool(data_path)
    logger.debug("Loading global policy...")
    for dir, _, files in os.walk(data_path):
        for filename in files:
            if fnmatch(filename, global_policy_path_pattern):
                context_cache.global_policy_path = os.path.join(dir, filename)
    if context_cache.global_policy_path:
        context_cache.global_policy = yaml_tool.load_yaml_file(context_cache.global_policy_path)
        logger.debug("'00-global_policy' loaded successfully.")
        return True
    else:
        logger.error("'00-global_policy' is missing!")
        return False


def load_fabric_mgmt(data_path, logger, fabric_mgmt_path="01-fabric_mgmt.y*ml"):
    """Load fabric mgmt"""
    yaml_tool = YamlTool(data_path)
    logger.debug("Loading fabric mgmt...")
    for dir, _, files in os.walk(data_path):
        for filename in files:
            if fnmatch(filename, fabric_mgmt_path):
                context_cache.fabric_mgmt_path = os.path.join(dir, filename)
    if context_cache.fabric_mgmt_path:
        context_cache.fabric_mgmt = yaml_tool.load_yaml_file(context_cache.fabric_mgmt_path)
        if not context_cache.fabric_mgmt:
            logger.error("Failed to load fabric mgmt!")
            return False
        logger.debug("'01-fabric-mgmt' loaded successfully.")
        return True
    else:
        logger.error("'01-fabric-mgmt' is missing!")
        return False


def load_aac_data(logger, data_path, output_path, nac_templates_dir=None):
    """Load global policy and AAC data"""

    logger.debug("Loading global policy and AAC data...")
    yaml_tool = YamlTool(data_path)
    if not nac_templates_dir:
        nac_templates_dir = os.path.join(Path(__file__).resolve().parent, "templates", "03-nac_tasks")

    try:
        if yaml_tool.render_j2_templates(
                nac_templates_dir, output_path
        ):
            logger.debug(
                f"Generate AAC working directory: '{output_path}' successfully."
            )

        nac_data_path = os.path.join(data_path, "nac_data")
        nac_data = yaml_tool.load_yaml_files(nac_data_path)

        aac_path = os.path.join(
            output_path,
            os.path.basename(nac_templates_dir),
            "host_vars",
            "apic1",
        )
        aac_data_path = os.path.join(aac_path, "data.yaml")

        with open(aac_data_path, "w") as aac:
            y = yaml.YAML()
            y.default_flow_style = False
            y.dump(nac_data, aac)

        logger.debug(
            f"Copy NAC data to working directory: '{aac_data_path}' successfully."
        )

        # self.aac_inventory_path = os.path.join(
        #     os.getcwd(),
        #     output_path,
        #     os.path.basename(settings.TEMPLATE_DIR.get("nac_tasks")),
        #     "inventory.yaml",
        # )

        logger.debug("Set AAC inventory successfully.")
        return True

    except Exception as e:
        logger.error(f"Exception occurred during loading AAC data: {str(e)}")
        logger.error(traceback.format_exc())

    return False