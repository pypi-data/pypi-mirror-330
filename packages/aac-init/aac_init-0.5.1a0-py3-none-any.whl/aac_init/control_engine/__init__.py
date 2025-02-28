import os
import sys
import importlib

current_file = os.path.abspath(__file__)
project_root = os.path.abspath(os.path.join(current_file, "..", ".."))

if project_root not in sys.path:
    sys.path.insert(0, project_root)

base_directory = os.path.join(project_root, "product")

def load_schedulers_from_directory(base_directory):
    for root, dirs, files in os.walk(base_directory):
        if 'scheduler.py' in files:
            relative_path = os.path.relpath(root, base_directory)
            if relative_path == ".":
                relative_path = ""
            else:
                relative_path = relative_path.replace(os.sep, ".") + "."
            for name in ["scheduler", "parameters", "data_validator"]:
                module_name = f"aac_init.product.{relative_path}{name}"
                importlib.import_module(module_name)


load_schedulers_from_directory(base_directory)
