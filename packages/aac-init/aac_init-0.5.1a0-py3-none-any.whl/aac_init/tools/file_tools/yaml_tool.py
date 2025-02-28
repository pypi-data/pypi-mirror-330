# -*- coding: utf-8 -*-

# Copyright: (c) 2024, Wang Xiao <xiawang3@cisco.com>, Rudy Lei <shlei@cisco.com>, Yang Bian <yabian@cisco.com>

import json
import os
import pathlib
import shutil
import importlib.util
import subprocess
import traceback

from typing import Any
from ruamel import yaml
from jinja2 import ChainableUndefined, Environment, FileSystemLoader
from aac_init.log_utils import LazyLogger


class VaultTag(yaml.YAMLObject):
    yaml_tag = "!vault"

    def __init__(self, v: str):
        self.value = v

    def __repr__(self) -> str:
        spec = importlib.util.find_spec("aac_validate.ansible_vault")
        if spec:
            if "ANSIBLE_VAULT_ID" in os.environ:
                vault_id = os.environ["ANSIBLE_VAULT_ID"] + "@" + str(spec.origin)
            else:
                vault_id = str(spec.origin)
            t = subprocess.check_output(
                [
                    "ansible-vault",
                    "decrypt",
                    "--vault-id",
                    vault_id,
                ],
                input=self.value.encode(),
            )
            return t.decode()
        return ""

    @classmethod
    def from_yaml(cls, loader: Any, node: Any) -> str:
        return str(cls(node.value))


class EnvTag(yaml.YAMLObject):
    yaml_tag = "!env"

    def __init__(self, v: str):
        self.value = v

    def __repr__(self) -> str:
        env = os.getenv(self.value)
        if env is None:
            return ""
        return env

    @classmethod
    def from_yaml(cls, loader: Any, node: Any) -> str:
        return str(cls(node.value))


class YamlTool:
    """Yaml Tool to handle Yaml and Jinja2 file actions"""

    def __init__(self, data_path: str = None):
        self.logger = LazyLogger("yaml_tool.log")
        self.data_path = data_path
        self.logger.debug("YAML tool initialized successfully.")

    def load_yaml_file(self, file_path):
        """Load single YAML file from a provided file path."""

        if (".yaml" not in file_path) and (".yml" not in file_path):
            self.logger.error(f"{file_path} is not an YAML file!")
            return False

        self.logger.debug(f"Loading YAML file '{file_path}'...")

        data = {}
        try:
            with open(file_path, "r") as file:
                content = file.read()
                y = yaml.YAML()
                y.preserve_quotes = True  # type: ignore
                y.register_class(VaultTag)
                y.register_class(EnvTag)
                data = y.load(content)
            self.logger.debug(f"Load YAML file '{file_path}' successfully.")
        except yaml.MarkedYAMLError as e:
            line = e.problem_mark.line + 1 if e.problem_mark else 0
            column = e.problem_mark.column + 1 if e.problem_mark else 0
            msg = (
                f"Syntax error in '{file_path}': "
                f"Line {line}, Column {column} - {e.problem}"
            )
            self.logger.error(msg)
            return False
        except Exception as e:
            self.logger.error(f"Unknown exception: {e}")
            self.logger.error(traceback.format_exc())
            return False

        return data

    def load_yaml_files(self, data_folder_path):
        """Load all YAML files from a provided directory."""

        self.logger.debug("Loading all yaml files...")

        result = {}
        for dir, _, files in os.walk(data_folder_path):
            for filename in files:
                if any([".yaml" in filename, ".yml" in filename]):
                    file_path = dir + os.path.sep + filename
                    data = self.load_yaml_file(file_path)
                    if data:
                        self._merge_dict(data, result)
                        self.logger.debug(f"Merge file '{file_path}' successfully.")
                else:
                    self.logger.debug(f"Skip file '{file_path}'...")

        self.logger.debug("Merged all yaml files successfully.")
        return result

    def _merge_dict(self, data, result):
        """Merge two nested dict/list structures."""

        if data:
            for key, value in data.items():
                if isinstance(value, dict):
                    node = result.setdefault(key, {})
                    if node is None:
                        result[key] = value
                    else:
                        self._merge_dict(value, node)
                elif isinstance(value, list):
                    if key not in result:
                        result[key] = value
                    if isinstance(result[key], list):
                        for i in value:
                            self._merge_list_item(i, result[key])
                else:
                    result[key] = value
        else:
            self.logger.warning("Data is empty!")

    def _merge_list_item(self, data, result_list):
        """Merge items into list."""

        if isinstance(data, dict):
            # check if we have an item in destination with matching primitives
            for dest_item in result_list:
                match = True
                comparison = False
                unique_source = False
                unique_dest = False
                for k, v in data.items():
                    if isinstance(v, dict) or isinstance(v, list):
                        continue
                    if k in dest_item and v == dest_item[k]:
                        comparison = True
                        continue
                    if k not in dest_item:
                        unique_source = True
                        continue
                    comparison = True
                    match = False
                for k, v in dest_item.items():
                    if isinstance(v, dict) or isinstance(v, list):
                        continue
                    if k in data and v == data[k]:
                        comparison = True
                        continue
                    if k not in data:
                        unique_dest = True
                        continue
                    comparison = True
                    match = False
                if comparison and match and not (unique_source and unique_dest):
                    self._merge_dict(data, dest_item)
                    return
        elif data in result_list:
            return

        result_list.append(data)

    def render_j2_template(
        self,
        templates_dst: str,
        template_rel_path: str,
        env: Environment,
        **kwargs: Any,
    ):
        """Render single Jinja2 template"""

        if not template_rel_path.endswith(".j2"):
            self.logger.warning(
                f"'{template_rel_path}' is not a Jinja2 template, skipped..."
            )
            return True

        self.logger.debug(f"Rendering Jinja2 template: {template_rel_path}")

        template = env.get_template(template_rel_path)

        yaml_data = self.load_yaml_files(self.data_path)
        json_data = json.loads(json.dumps(yaml_data))
        result = template.render(json_data, **kwargs)

        # remove extra empty lines
        lines = result.splitlines()
        cleaned_lines = []
        for index, line in enumerate(lines):
            if len(line.strip()):
                cleaned_lines.append(line)
            else:
                if index + 1 < len(lines):
                    next_line = lines[index + 1]
                    if len(next_line) and not next_line[0].isspace():
                        cleaned_lines.append(line)
        result = os.linesep.join(cleaned_lines)

        template_path = os.path.join(templates_dst, template_rel_path)
        rendered_template_path = template_path.replace(".j2", "")
        with open(rendered_template_path, "w") as file:
            file.write(result)

        if os.path.exists(rendered_template_path):
            self.logger.debug(
                f"Render Jinja2 template: '{template_path}' to '{rendered_template_path}' successfully."
            )
            os.remove(template_path)
            self.logger.debug(
                f"Delete rendered Jinja2 template: '{template_path}' successfully."
            )
            return True
        else:
            self.logger.error(f"Failed to render Jinja2 template: '{template_path}'!")

        return False

    def render_j2_templates(self, templates_path: str, output_path: str):
        """Render Jinja2 templates"""

        self.logger.debug(f"Start to render templates: '{templates_path}'...")

        # Copy template to output dir
        templates_dst = os.path.join(output_path, os.path.basename(templates_path))
        pathlib.Path(templates_dst).mkdir(parents=True, exist_ok=True)
        shutil.copytree(templates_path, templates_dst, dirs_exist_ok=True)

        self.logger.debug(
            f"Copy template to output dir '{templates_dst}' successfully."
        )

        env = Environment(
            loader=FileSystemLoader(templates_dst),
            undefined=ChainableUndefined,
            lstrip_blocks=True,
            trim_blocks=True,
        )

        for dir, _, files in os.walk(templates_dst):
            for file in files:
                file_path = os.path.join(dir, file)
                template_rel_path = os.path.relpath(file_path, templates_dst)
                if not self.render_j2_template(templates_dst, template_rel_path, env):
                    return False

        self.logger.debug(f"Render templates: '{templates_path}' successfully.")
        return True
