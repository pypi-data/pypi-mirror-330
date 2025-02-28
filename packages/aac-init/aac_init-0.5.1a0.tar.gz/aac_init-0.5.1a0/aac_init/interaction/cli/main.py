import os
import re
import importlib
# from aac_init import __version__

import click
import json
import yaml
from datetime import datetime
from aac_init.control_engine.controller import controller, context_cache


class CLI:
    def __init__(self, controller):
        self.controller = controller

    def _parse_tasks_file(self, tasks_file):
        """
        Parse tasks from a JSON or YAML file.
        """
        with open(tasks_file, 'r') as file:
            if tasks_file.endswith(".yaml") or tasks_file.endswith(".yml"):
                tasks = yaml.safe_load(file)
            elif tasks_file.endswith(".json"):
                tasks = json.load(file)
            else:
                raise ValueError("Unsupported file format. Use JSON or YAML.")
        return tasks

    def _get_operation_parameters(self, project, product, operation):
        """
        Retrieve the required parameters for a given operation.
        """
        key = (project, product, operation)
        print(self.controller.parameters_registry)
        parameters_func = self.controller.parameters_registry.get(key)
        if parameters_func:
            return parameters_func()
        return []

    def generate_click_cli(self):
        @click.group()
        def cli():
            """CLI for managing and executing tasks."""
            pass

        @cli.command(name="list")
        def list_operations():
            """
            List all registered projects, products, and operations with their details.
            """
            # Group operations by project and product for structured display
            projects = {}
            for (project, product, operation), func_info in controller.functions_registry.items():
                description = func_info.get("description", "No description available.")
                key = (project, product)
                if key not in projects:
                    projects[key] = {}
                projects[key][operation] = {
                    "description": description,
                    "parameters": controller.parameters_registry.get((project, product, operation), None),
                }

            current_project = None
            current_product = None

            # Print the structured output with colors
            for (project, product), operations in projects.items():
                if project != current_project:
                    click.echo(click.style(f"Project: {project}", fg="green", bold=True))
                    current_project = project

                if product != current_product:
                    product_str = product
                    alias_str = ""
                    for alias, (pj, pd) in controller.alias_registry.items():
                        if project == pj and product == pd:
                            alias_str = alias
                            break
                    if alias_str:
                        product_str += f"(alias: {alias_str})"
                    click.echo(click.style(f"    Product: {product_str}", fg="cyan"))
                    current_product = product

                ordered_operations = controller.get_all_operations(project, product)
                for op in ordered_operations:
                    operation = op
                    details = operations.get(op)
                    click.echo(click.style(f"        Operation: {operation}", fg="yellow"))
                    click.echo(f"            {click.style('Description:', fg='blue')} {details['description']}")
                    parameters_func = details["parameters"]
                    if parameters_func:
                        parameters = parameters_func()
                        click.echo(click.style("            Parameters:", fg="magenta"))
                        for param in parameters:
                            param_name = param["name"]
                            param_type = param["type"]
                            required = "Required" if param.get("required", False) else "Optional"
                            description = param.get("description", "No description available.")
                            click.echo(f"                - {param_name} ({param_type}, {required}): {description}")
                    else:
                        click.echo(click.style("            Parameters: None", fg="magenta"))

        @cli.command(name="describe")
        @click.option("-j", "--project", required=True, help="Project name.")
        @click.option("-p", "--product", required=True, help="Product name.")
        @click.option("-o", "--operation", required=True, help="Operation name.")
        def describe_operation(project, product, operation):
            """
            Describe the parameters required by a specific operation.
            """
            key = (project, product, operation)
            if key not in controller.functions_registry:
                click.echo(f"No such operation: Project={project}, Product={product}, Operation={operation}")
                return

            parameters_func = controller.parameters_registry.get(key)
            if not parameters_func:
                click.echo(f"No parameters required for operation: {operation}")
                return

            click.echo(f"Parameters for {project}/{product}/{operation}:")
            parameters = parameters_func()
            for param in parameters:
                name = param["name"]
                param_type = param["type"]
                required = "Required" if param.get("required", False) else "Optional"
                description = param.get("description", "No description available.")
                click.echo(f"- {name} ({param_type}, {required}): {description}")

        @cli.command(name="run")
        @click.option("-a", "--alias", help="alias")
        @click.option("-j", "--project", help="Project name(s) for the operations.")
        @click.option("-p", "--product", help="Product name(s) for the operations.")
        @click.option("-e", "--operations",  help="Operation(s) to execute.")
        @click.option("-o", "--output", required=False, help="Output dir path")
        @click.option(
             '--tasks-file',
             type=click.Path(exists=True),
             help="Path to JSON or YAML file containing tasks.",
         )
        @click.option(
            "--params",
            nargs=2,
            multiple=True,
            type=(str, str),
            help="Parameters for operations, specified as key-value pairs.",
        )
        @click.option(
            "-l", "--log-level",
            type=click.Choice(["debug", "info", "warning", "error", "critical"], case_sensitive=False),
            default="info",
            show_default=True,
            help="Specify the logging level. Default setting is 'info'."
        )
        def run(tasks_file, alias, project, product, operations, params, log_level, output=None):
            """
            Execute operations across projects and products.
            """
            if not (project and project) and not alias and not tasks_file:
                raise click.UsageError("You must specify at least one project, one product or one alias or a tasks_file")

            if not operations:
                raise click.UsageError("You must specify at least one project, one product, and one operation.")

            if log_level:
                context_cache.log_level = log_level

            # Parse input into tasks
            task_groups = []
            if tasks_file:
                task_group = self._parse_tasks_file(tasks_file)
                for task in task_group:
                    alias = task.get("alias")
                    project = task.get("project")
                    product = task.get("product")
                    operations = task["operation"]
                    params = task.get("params", {})

                    for op in operations:
                        if op.isdigit():
                            op = controller.get_operation_by_order(project, product, op)

                        required_params = self._get_operation_parameters(alias, project, product, op)
                        for param in required_params:
                            name = param["name"]
                            if name not in params and param.get("required", False):
                                raise ValueError(
                                    f"Missing required parameter '{name}' for {project}-{product}-{op}."
                                )
            else:
                params_dict = dict(params)
                if alias:
                    project, product = controller.resolve_alias(alias)
                ops_list = operations.split(",")
                converted_ops_list = []
                for op in ops_list:
                    if op.isdigit():
                        op = controller.get_operation_by_order(project, product, op)
                    converted_ops_list.append(op)

                ordered_operations = controller.resolve_execution_order(converted_ops_list, product, product)

                task_groups.append({
                    "project": project,
                    "product": product,
                    "operations": ordered_operations,
                    "alias": alias,
                    "params": params_dict,
                })

            data_path = params_dict.get("data_path")
            if not output and data_path:
                current_datetime = datetime.now().strftime("%Y%m%d-%H%M%S")
                base_dir_template = "aac_init_{fabric_name}_" + f"working_dir_{current_datetime}"
                output_base_dir_template = os.path.join(os.getcwd(), base_dir_template)
                data_folder_name = os.path.basename(os.path.normpath(data_path))
                output = output_base_dir_template.format(fabric_name=data_folder_name)

            current_project = None
            current_product = None

            click.secho('YOUR CHOICES ARE AS BELOW:', blink=True, bold=True)
            for one_task in task_groups:
                alias = one_task.get("alias")
                if alias:
                    project, product = controller.resolve_alias(alias)
                else:
                    project = one_task.get("project")
                    product = one_task.get("product")
                operations = one_task.get("operations")
                tmp_params = one_task.get("params")

                if project != current_project:
                    click.echo(click.style(f"Project: {project}", fg="green", bold=True))
                    current_project = project

                if product != current_product:
                    click.echo(click.style(f"    Product: {product}", fg="cyan"))
                    current_product = product

                for one_op in operations:
                    click.echo(click.style(f"        Operation: {one_op}", fg="yellow"))

                for param, value in tmp_params.items():
                    click.echo(f"            param name: {param}, params value: {value}")

            confirm_prompt = (
                "\nAre you sure to proceed with the below choice(s)?\n"
            )

            selections_confirm = click.prompt(
                click.style(confirm_prompt, fg="green"),
                type=click.Choice(["yes", "no"], case_sensitive=False),
                default="yes",
                show_default=True,
                show_choices=True,
            )
            if not re.match(r"yes", selections_confirm, re.IGNORECASE):
                exit()
            # Execute all tasks
            results = controller.execute(task_groups, output)
            if not results:
                return

            for result in results:
                status = result.get("status")
                status = "success" if status else "failed"
                project = result.get("project")
                product = result.get("product")
                operation = result.get("operation")
                msg = f"Task [{project}] -- [{product}] -- [{operation}]: {status}."
                details = result.get("details")
                if details:
                    msg += f" Details: {details}"

                if status == "success":
                    click.echo(click.style(msg, fg="green"))
                else:
                    click.echo(click.style(msg, fg="red"))

        return cli


def main():
    cli_instance = CLI(controller)
    cli = cli_instance.generate_click_cli()
    cli()


if __name__ == "__main__":
    main()
    