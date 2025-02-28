import os
import time
import threading
from typing import Union, Dict
from pathlib import Path

from aac_init.control_engine.metadata_loader import metadata
from aac_init.control_engine.controller import controller
from aac_init.log_utils import LazyLogger
from aac_init.control_engine.global_cache import context_cache

from .tools import (
    ApicCimcTool,
    AciSwitchTool,
    ApicTool,
)
from .data_utils import load_aac_data, load_global_policy, load_fabric_mgmt
from aac_init.tools import ThreadTool, AnsibleTool


logger = LazyLogger("datacenter_operation.log")

controller.register_alias("aac", "datacenter", "aci")


@controller.register(
    project='datacenter', product="aci", operation='clear_configuration',
    description="Clear switch and cimc configuration",
    order=1,
    dependencies=[]
)
def clear_configuration(data_path):
    logger.info("Start to clear configuration")

    if not load_global_policy(data_path, logger):
        return False

    if not load_fabric_mgmt(data_path, logger):
        return False

    fabric_policy = context_cache.global_policy.get("fabric", {})
    global_policies = fabric_policy.get("global_policies", {}) or {}
    apic_check = "apic_nodes_connection" in fabric_policy
    aci_switch_check = "switch_nodes_connection" in fabric_policy

    clear_config_threads = []

    if apic_check:
        apics = fabric_policy.get("apic_nodes_connection", []) or []
        for apic_cimc_connection in apics:
            apic = ApicCimcTool(global_policies, apic_cimc_connection, apics)
            if not apic.api_validate_apic():
                logger.error(f"Validate APIC '{apic.hostname}' failed!")
                return False
            logger.info(f"Validate APIC '{apic.hostname}' successfully.")
            thread = ThreadTool(target=apic.ssh_clear_config)
            clear_config_threads.append((apic.hostname, thread))

    if aci_switch_check:
        aci_switches = fabric_policy.get("switch_nodes_connection", []) or []

        # Load fabric mgmt
        fabric_mgmt_policy_apic = context_cache.fabric_mgmt.get("apic", {}) or {}
        fabric_mgmt_policy_apic_node_policies = (
                fabric_mgmt_policy_apic.get("node_policies", {}) or {}
        )
        aci_switches_mgmt = (
                fabric_mgmt_policy_apic_node_policies.get("nodes", []) or []
        )

        for aci_switch_connection in aci_switches:
            aci_switch_mgmt = next(
                (
                    node
                    for node in aci_switches_mgmt
                    if node["id"] == aci_switch_connection["id"]
                ),
                {},
            )

            aci_switch = AciSwitchTool(
                global_policies, aci_switch_connection, aci_switch_mgmt
            )
            if not aci_switch.validate_aci_switch():
                logger.error(
                    f"Validate ACI switch '{aci_switch.hostname}' failed!"
                )
                return False
            logger.info(
                f"Validate ACI switch '{aci_switch.hostname}' successfully."
            )
            thread = ThreadTool(target=aci_switch.clear_configuration)
            clear_config_threads.append((aci_switch.hostname, thread))

        for _, thread in clear_config_threads:
            thread.start()

        for _, thread in clear_config_threads:
            thread.join()

        excute_errors = []

        for hostname, thread in clear_config_threads:
            if thread.get_result():
                logger.info(f"Clear config '{hostname}' successfully.")
            else:
                logger.error(
                    f"Clear config '{hostname}' failed. Check APIC/switch logs for details."
                )
                excute_errors.append(hostname)

        if excute_errors:
            logger.error(
                "ACI clear config failed, check APIC/switch logs for details."
            )
            return False

        logger.info("ACI Clear config successfully.")
        return True


@controller.register(
    project='datacenter', product="aci", operation='wipe_reimage',
    description="Wipe and boot APIC/switch to particular version",
    order=2,
    dependencies=[])
def fabric_bootstrap(data_path, max_switch_concurrent: int = None):
    logger.info("Start to bootstrap ACI fabric...")
    if not load_global_policy(data_path, logger):
        return False

    if not load_fabric_mgmt(data_path, logger):
        return False

    fabric_policy = context_cache.global_policy.get("fabric", {})
    global_policies = fabric_policy.get("global_policies", {}) or {}
    apic_check = "apic_nodes_connection" in fabric_policy
    aci_switch_check = "switch_nodes_connection" in fabric_policy

    fabric_bootstrap_threads = []

    # Validate APICs if have
    if apic_check:
        apics = fabric_policy.get("apic_nodes_connection", []) or []

        for apic_cimc_connection in apics:
            apic = ApicCimcTool(global_policies, apic_cimc_connection, apics)
            if not apic.api_validate_apic():
                logger.error(f"Validate APIC '{apic.hostname}' failed!")
                return False
            logger.info(f"Validate APIC '{apic.hostname}' successfully.")
            thread = ThreadTool(target=apic.gen_install_apic)
            fabric_bootstrap_threads.append((apic.hostname, thread))
            logger.debug(f"Add APIC '{apic.hostname}' to thread successfully.")

    # Validate ACI switches if have
    if aci_switch_check:
        aci_switches = fabric_policy.get("switch_nodes_connection", []) or []

        # Load fabric mgmt
        fabric_mgmt_policy_apic = context_cache.fabric_mgmt.get("apic", {}) or {}
        fabric_mgmt_policy_apic_node_policies = (
                fabric_mgmt_policy_apic.get("node_policies", {}) or {}
        )
        aci_switches_mgmt = (
                fabric_mgmt_policy_apic_node_policies.get("nodes", []) or []
        )

        semaphore = None
        if max_switch_concurrent:
            semaphore = threading.Semaphore(max_switch_concurrent)

        for aci_switch_connection in aci_switches:
            aci_switch_mgmt = next(
                (
                    node
                    for node in aci_switches_mgmt
                    if node["id"] == aci_switch_connection["id"]
                ),
                {},
            )

            aci_switch = AciSwitchTool(
                global_policies, aci_switch_connection, aci_switch_mgmt, semaphore
            )
            if not aci_switch.validate_aci_switch():
                logger.error(
                    f"Validate ACI switch '{aci_switch.hostname}' failed!"
                )
                return False
            logger.info(
                f"Validate ACI switch '{aci_switch.hostname}' successfully."
            )
            thread = ThreadTool(target=aci_switch.install_aci_switch)
            fabric_bootstrap_threads.append((aci_switch.hostname, thread))
            logger.debug(
                f"Add ACI switch '{aci_switch.hostname}' to thread successfully."
            )

    for _, thread in fabric_bootstrap_threads:
        thread.start()

    for _, thread in fabric_bootstrap_threads:
        thread.join()

    install_errors = []
    for hostname, thread in fabric_bootstrap_threads:
        if thread.get_result():
            logger.info(f"Install '{hostname}' successfully.")
        else:
            logger.error(
                f"Install '{hostname}' failed. Check APIC/switch logs for details."
            )
            install_errors.append(hostname)

    if install_errors:
        logger.error(
            "ACI fabric bootstrap failed, check APIC/switch logs for details."
        )
        return False

    logger.info("ACI fabric bootstrap successfully.")
    return True


@controller.register(
    project='datacenter', product='aci', operation='apic_init_setup',
    description="APIC initial setup",
    order=3,
    dependencies=[])
def apic_init_setup(data_path):
    logger.info("Start to initial setup APIC...")
    if not context_cache.get("global_policy"):
        if not load_global_policy(data_path, logger):
            return False
    fabric_policy = context_cache.global_policy.get("fabric", {})
    global_policies = fabric_policy.get("global_policies", {}) or {}
    apic_check = "apic_nodes_connection" in fabric_policy

    # Validate APIC exists
    if apic_check:
        apics = fabric_policy.get("apic_nodes_connection", []) or []

        for apic_cimc_connection in apics:
            apic = ApicCimcTool(global_policies, apic_cimc_connection, apics)
            if not apic.api_validate_apic():
                logger.error(f"Validate APIC CIMC'{apic.hostname}' failed!")
                return False
            logger.info(f"Validate APIC CIMC {apic.hostname} successfully.")

        for apic_cimc_connection in apics:
            if metadata.datacenter.APIC_DISCOVER_SKIP_FLAG:
                logger.info(f"Skip APIC discovery for {apic.hostname}.")
                break
            apic = ApicCimcTool(global_policies, apic_cimc_connection, apics)
            if not apic.ssh_init_apic():
                logger.error(f"Initial setup APIC '{apic.hostname}' failed!")
                return False
            logger.info(f"Initial setup APIC {apic.hostname} successfully.")

        time.sleep(300)

        max_retry_times = 3
        for apic_cimc_connection in apics:
            if metadata.datacenter.APIC_DISCOVER_SKIP_FLAG:
                logger.info(f"Skip APIC discovery for {apic.hostname}.")
                break
            apic_cnn = ApicTool(global_policies, apic_cimc_connection)
            validate_success = False
            for _ in range(max_retry_times):
                if apic_cnn.api_validate_apic():
                    validate_success = True
                    break
                time.sleep(60)
            if not validate_success:
                logger.error(f"Initial setup APIC '{apic_cimc_connection.hostname}' failed!")
                return False
    else:
        logger.error("No APIC found!")
        return False

    return True


@controller.register(
    project='datacenter', product='aci', operation='apic_nac_config',
    description="Init ACI Fabric via NaC (Network as Code)",
    order=4,
    dependencies=[])
def apic_nac_config(data_path):
    output_path = context_cache.output_dir
    logger.debug("Start to configure ACI Fabric via NaC...")
    if not context_cache.get("global_policy"):
        if not load_global_policy(data_path, logger):
            return False
    fabric_policy = context_cache.global_policy.get("fabric", {})
    global_policies = fabric_policy.get("global_policies", {}) or {}
    apic_check = "apic_nodes_connection" in fabric_policy

    # Validate APIC exists
    if apic_check:
        apics = fabric_policy.get("apic_nodes_connection", []) or []
        apic1 = next((apic for apic in apics if apic.get("id") == 1), None)
        if not apic1:
            logger.error("No APIC1 found!")
    else:
        logger.error("No APIC found!")
        return False

    apic = ApicTool(global_policies, apic1)
    max_retry = 10
    success_flag = False
    for i in range(max_retry):
        if not apic.api_validate_apic():
            logger.debug(f"APIC API validating {i+1} times...")
            time.sleep(30)
            continue
        break
    if not success_flag:
        logger.error(f"Validate APIC '{apic.hostname}' failed!")
        return False

    logger.info(f"Validate APIC {apic.hostname} successfully.")

    if not load_aac_data(logger, data_path, output_path):
        logger.error("Failed to load AAC data!")
        return False

    nac_templates_dir = os.path.join(Path(__file__).resolve().parent, "templates", "03-nac_tasks")

    playbook_dir_validate = os.path.join(
        os.getcwd(),
        output_path,
        os.path.basename(nac_templates_dir),
        "aac_ansible",
        "apic_validate.yaml",
    )

    aac_inventory_path = os.path.join(
        os.getcwd(),
        output_path,
        os.path.basename(nac_templates_dir),
        "inventory.yaml",
    )

    if not apic.ansible_validate(
            playbook_dir_validate, aac_inventory_path, output_path
    ):
        logger.error("ACI as Code validation failed!")
        return False

    playbook_dir_deploy = os.path.join(
        os.getcwd(),
        output_path,
        os.path.basename(nac_templates_dir),
        "aac_ansible",
        "apic_deploy.yaml",
    )

    if not apic.ansible_deploy(
            playbook_dir_deploy, aac_inventory_path, output_path
    ):
        logger.error("ACI as Code deploy failed!")
        return False

    playbook_dir_test = os.path.join(
        os.getcwd(),
        output_path,
        os.path.basename(nac_templates_dir),
        "aac_ansible",
        "apic_test.yaml",
    )

    if not apic.ansible_test(
            playbook_dir_test, aac_inventory_path, output_path
    ):
        logger.error("ACI as Code test failed!")
        return False

    logger.info(f"Configure APIC {apic.hostname} via AAC successfully.")
    return True
