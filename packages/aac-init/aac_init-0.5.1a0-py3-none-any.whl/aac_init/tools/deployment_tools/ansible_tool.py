# -*- coding: utf-8 -*-

# Copyright: (c) 2024, Wang Xiao <xiawang3@cisco.com>, Rudy Lei <shlei@cisco.com>, Yang Bian <yabian@cisco.com>

import re

from aac_init.log_utils import LazyLogger
from ansible_runner import run


class AnsibleTool:
    """Ansible Toolkits"""

    def __init__(self, output_path: str):
        self.logger = LazyLogger("ansible_tool.log")

        self.output_path = output_path
        self.aac_inventory_path = None

        self.logger.debug("Ansible Tool initialized successfully.")

    def ansible_runner(
        self, ansible_phase, playbook_dir, inventory_path=None, quiet=True
    ):
        """Ansible runner"""

        logger = LazyLogger(f"ansible_tool_{ansible_phase}.log")

        def _callback(res):
            if not quiet and "stdout" in res:
                print(res["stdout"])
            output = re.compile(r"\x1b\[\[?(?:\d{1,2}(?:;\d{0,2})*)?[m|K]").sub(
                "", res["stdout"]
            )
            logger.debug(output)

        runner = run(
            playbook=playbook_dir,
            inventory=inventory_path,
            verbosity=5,
            quiet=True,
            event_handler=_callback,
        )

        if runner.status == "successful":
            logger.debug(
                f"Complete Network as Code Ansible phase: '{ansible_phase}' successfully."
            )
            return True

        else:
            logger.error(f"Error on Network as Code Ansible phase: '{ansible_phase}'!")
            return False
