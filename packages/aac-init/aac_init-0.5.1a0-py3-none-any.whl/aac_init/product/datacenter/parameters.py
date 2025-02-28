from aac_init.control_engine.controller import controller



@controller.parameters("datacenter", "aci", "clear_configuration")
def clear_configuration_parameters():
    return [
        {
            "name": "data_path",
            "type": "str",
            "required": True,
            "description": "A folder path that contains needed data files: 00-global_policy.yml and nac_data/01-fabric_mgmt.yml",
        }
    ]


@controller.parameters("datacenter", "aci", "wipe_reimage")
def fabric_bootstrap_parameters():
    return [
        {
            "name": "data_path",
            "type": "str",
            "required": True,
            "description": "A folder path that contains needed data files: 00-global_policy.yml and nac_data/01-fabric_mgmt.yml",
        },
        {
            "name": "max_switch_concurrent",
            "type": "int",
            "required": False,
            "description": "Max number of switch install at a time.",
        }
    ]


@controller.parameters("datacenter", "aci", "apic_init_setup")
def apic_init_setup_parameters():
    return [
        {
            "name": "data_path",
            "type": "str",
            "required": True,
            "description": "A folder path that contains needed data files: 00-global_policy.yml",
        }
    ]


@controller.parameters("datacenter", "aci", "apic_nac_config")
def apic_nac_config_parameters():
    return [
        {
            "name": "data_path",
            "type": "str",
            "required": True,
            "description": "A folder path that contains needed data files: 00-global_policy.yml",
        }
    ]
