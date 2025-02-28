# -*- coding: utf-8 -*-

# Copyright: (c) 2024, Wang Xiao <xiawang3@cisco.com>

import os.path
from pathlib import Path
from datetime import datetime

# BASE_DIR = Path(__file__).resolve().parent.parent
#
# current_datetime = datetime.now().strftime("%Y%m%d-%H%M%S")
# base_dir = f"aac_init_working_dir_{current_datetime}"
#
# OUTPUT_BASE_DIR = os.path.join(os.getcwd(), base_dir)

# base_dir_template = "aac_init_{fabric_name}_" + f"working_dir_{current_datetime}"
# OUTPUT_BASE_DIR_TEMPLATE = os.path.join(os.getcwd(), base_dir_template)

# DEFAULT_USER_SELECTIONS = [
#     "Wipe and boot APIC/switch to particular version",
#     "APIC initial setup (Single Pod)",
#     "Init ACI Fabric via NaC (Network as Code)"
# ]

# DEFAULT_DATA_PATH = ["00-global_policy.yml", "00-global_policy.yaml"]
# DEFAULT_GLOBAL_POLICY_PATH = "00-global_policy.y*ml"
# DEFAULT_FABRIC_MGMT_PATH = ["01-fabric_mgmt.yml", "01-fabric_mgmt.yaml"]
# FABRIC_MGMT_PATH = "01-fabric_mgmt.y*ml"
# DATA_PATH = "nac_data"

# SCHEMA_DIR = os.path.join(BASE_DIR, "schemas")

# TEMPLATE_DIR = {
#     "nac_tasks": os.path.join(BASE_DIR, "templates", "03-nac_tasks"),
# }

# DEFAULT_LOG_LEVEL = 'info'

# APIC_DISCOVER_SKIP_FLAG = False  # Not skip APIC discovery by default, set to True for APIC2/3 on version 6.x

# OUTPUT_BASE_DIR = OUTPUT_BASE_DIR_TEMPLATE.format(fabric_name="work")
