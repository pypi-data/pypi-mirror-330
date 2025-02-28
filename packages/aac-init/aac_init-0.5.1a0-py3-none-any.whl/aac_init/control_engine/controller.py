import os
from datetime import datetime
import functools
import inspect
import copy
import time


from aac_init.control_engine.global_cache import context_cache
from aac_init.log_utils import LazyLogger

# logger = setup_logger("control_engine.log")


def call_with_params(func, params):
    signature = inspect.signature(func)
    func_params = signature.parameters.keys()
    filtered_params = {k: params[k] for k in func_params if k in params}
    return func(**filtered_params)


class Controller:
    def __init__(self):
        self.validators_registry = {}
        self.parameters_registry = {}
        self.functions_registry = {}
        self.dependencies_registry = {}
        self.order_registry = {}
        self.alias_registry = {}

    def register_alias(self, alias, project, product):
        self.alias_registry[alias] = (project, product)

    def resolve_alias(self, alias):
        return self.alias_registry.get(alias)

    def register(self, project, product, operation, description="", dependencies=None, order=None):
        """
        Register an operation under a specific project and product.
        """
        def decorator(func):
            key = (project, product, operation)
            self.functions_registry[key] = {"func": func, "description": description}
            self.dependencies_registry[key] = dependencies or []
            self.order_registry[key] = order

            @functools.wraps(func)
            def wrapper(*args, **kwargs):
                return func(*args, **kwargs)

            return wrapper

        return decorator

    def parameters(self, project, product, operation):
        """
        Register parameters schema for a specific operation.
        """
        def decorator(schema_func):
            key = (project, product, operation)
            self.parameters_registry[key] = schema_func
            return schema_func

        return decorator

    def validator(self, project, product=None, operation=None):
        """
        Register a validator for specific project/product/operation combinations.
        """
        def decorator(func):
            key = (project, product, operation)
            if key not in self.validators_registry:
                self.validators_registry[key] = []
            self.validators_registry[key].append(func)
            return func

        return decorator

    def resolve_execution_order(self, operations, project, product):
        """
        Resolve execution order for operations based on dependencies and order.
        """
        keys = [(project, product, op) for op in operations]
        keys_with_order = [(key, self.order_registry.get(key, float('inf'))) for key in keys]
        sorted_keys = sorted(keys_with_order, key=lambda x: x[1])

        executed = set()
        ordered_operations = []

        for key, _ in sorted_keys:
            operation = key[2]
            dependencies = self.dependencies_registry.get(key, [])

            for dep in dependencies:
                dep_key = (project, product, dep)
                if dep_key not in executed:
                    raise ValueError(f"Dependency '{dep}' must be executed before '{operation}'.")

            ordered_operations.append(operation)
            executed.add(key)

        return ordered_operations

    def get_all_operations(self, project, product):
        operations = [
            operation
            for (proj, prod, operation), ord_val in self.order_registry.items()
            if proj == project and prod == product
        ]
        if operations:
            return operations
        else:
            return []

    def get_operation_by_order(self, project, product, order: int):
        if isinstance(order, str):
            order = int(order)

        for (proj, prod, operation), ord_val in self.order_registry.items():
            if proj == project and prod == product and ord_val == order:
                return operation
        return None

    def check_params(self, project, product, operation, params):
        key = (project, product, operation)
        parameters_func = self.parameters_registry.get(key)
        if not parameters_func:
            return True, None

        parameters = parameters_func()
        for param in parameters:
            param_name = param['name']
            if param_name in params:
                value = params[param_name]
                if isinstance(param['type'], list):
                    if not any(isinstance(value, eval(t)) for t in param['type']):
                        return False, f"Parameter '{param_name}' must be one of the types {param['type']}."
                else:
                    if not isinstance(value, eval(param['type'])):
                        return False, f"Parameter '{param_name}' must be one of the types {param['type']}."
            elif param.get('required', False):
                return False, f"Parameter '{param_name}' is required."

        return True, None

    def execute(self, tasks, output_dir=None):
        """
        Execute a batch of tasks while ensuring dependencies and order are respected.
        """
        if not tasks:
            raise ValueError("No tasks provided for execution.")

        if not output_dir:
            current_datetime = datetime.now().strftime("%Y%m%d-%H%M%S")
            base_dir_template = "aac_init_{fabric_name}_" + f"working_dir_{current_datetime}"
            output_base_dir_template = os.path.join(os.getcwd(), base_dir_template)
            output_dir = output_base_dir_template.format(fabric_name="work")

        context_cache.output_dir = output_dir

        results = {}
        if not context_cache.get("tasks"):
            context_cache.tasks = []
        for task in tasks:
            alias = task.get("alias")
            if alias:
                project, product = self.resolve_alias(alias)
            else:
                project = task.get("project")
                product = task.get("product")
            operations = task["operations"]

            if not (project and project) and not alias:
                raise False

            if not operations:
                raise False

            ordered_operations = self.resolve_execution_order(operations, project, product)

            # generate results
            for operation in ordered_operations:
                key = (project, product, operation)
                context_cache.tasks.append(key)
                results[key] = {
                    "project": project,
                    "product": product,
                    "operation": operation
                }

            # check params
            params = task.get("params", {})
            params_failed = False
            for operation in ordered_operations:
                key = (project, product, operation)
                status, details = self.check_params(project, product, operation, params)
                if not status:
                    params_failed = True
                    results[key].update({"status": key})
                    if details:
                        if "details" not in results[key]:
                            results[key].update({"details": details})
                        else:
                            results[key]["details"] += details

            if params_failed:
                return results.values()

            validate_failed = False
            for operation in ordered_operations:
                key = (project, product, operation)
                validator_keys = [(project, None, None), (project, product, None)]
                validator_keys += [(project, product, op) for op in task['operations']]
                tmp_params = copy.deepcopy(params)
                tmp_params.update({
                    "project": project,
                    "product": product,
                    "operation": operation,
                    "operations": operations
                })
                for v_key in validator_keys:
                    if v_key in self.validators_registry:
                        for validator in self.validators_registry[v_key]:
                            status, msg = call_with_params(validator, tmp_params)
                            if not status:
                                validate_failed = True
                                results[key].update({"status": status})
                                if msg:
                                    results[key].update({"details": f"Operation validation failed. Reason:{msg}"})
                                    break

            if validate_failed:
                return results.values()

            execute_failed_flag = False
            for operation in operations:
                key = (project, product, operation)
                func_info = self.functions_registry[key]
                func = func_info["func"]

                if execute_failed_flag:
                    results[key].update(
                        {"status": status, "details": "Due to the failure of the previous operation, it was not executed."})
                    continue

                status = func(**params)
                if status:
                    results[key].update({"status": status})
                else:
                    results[key].update({"status": status, "details": "Execute operation failed, please check the log."})
                    execute_failed_flag = True

        return results.values()

    def get_function_description(self, project, product, operation):
        """
        Get the description of a registered function.
        """
        key = (project, product, operation)
        return self.functions_registry.get(key, {}).get("description", "Description not available.")


controller = Controller()