"""
Parse TMA configuration.
"""

import ast
from typing import List
from simplify_ast import simplify_ast, collect_name_from_ast

def get_ast(file_path: str) -> ast.Module:
    """
    Return ast of file.
    """
    with open(file_path, "r", encoding="utf-8") as file_obj:
        file_text_str = file_obj.read()
        module_ast = ast.parse(file_text_str)
        return module_ast

def __is_decision_tree_state(assign_state: ast.Assign):
    if len(assign_state.targets) != 1:
        return False

    assign_target: ast.Attribute = assign_state.targets[0]
    assign_value: ast.Subscript = assign_state.value
    if not isinstance(assign_target, ast.Attribute):
        return False
    if not isinstance(assign_value, ast.Subscript):
        return False

    target_value: ast.Subscript = assign_target.value
    target_attr: str =  assign_target.attr
    if not isinstance(target_value, ast.Subscript):
        return False
    if target_attr != "parent":
        return False

    target_value_value: ast.Name = target_value.value
    if not isinstance(target_value_value, ast.Name):
        return False
    if target_value_value.id != "o":
        return False

    value_value: ast.Name = assign_value.value
    if not isinstance(value_value, ast.Name):
        return False
    if value_value.id != "o":
        return False

    return True

def __get_decision_tree_setup_init(init_func: ast.FunctionDef):
    top_level = []
    child_dict = dict()

    for node in init_func.body:
        if isinstance(node, ast.Assign) and __is_decision_tree_state(node):
            assign_target: ast.Attribute = node.targets[0]
            assign_value: ast.Subscript = node.value
            target_value: ast.Subscript = assign_target.value
            target_value_slice: ast.Constant = target_value.slice
            target_value_slice_str: str = target_value_slice.s
            value_slice: ast.Constant = assign_value.slice
            value_slice_str: str = value_slice.s

            # Find parent item.
            if value_slice_str not in child_dict:
                top_level.append(value_slice_str)
                child_dict[value_slice_str] = []

            # Append child
            child_dict[value_slice_str].append(target_value_slice_str)
            child_dict[target_value_slice_str] = []

    return top_level, child_dict

def get_decision_tree(module_ast: ast.Module):
    """
    Return decision tree.
    """
    # Get __init__ function of setup.
    for node in module_ast.body:
        if isinstance(node, ast.ClassDef) and node.name == "Setup":
            for node1 in node.body:
                if isinstance(node1, ast.FunctionDef) and node1.name == "__init__":
                    top_level, child_dict = __get_decision_tree_setup_init(node1)
                    return top_level, child_dict


def get_metrics_dict(module_ast: ast.Module) -> dict:
    """
    Get metrics dictionary
    """
    metrics_dict = dict()

    for item in module_ast.body:
        if isinstance(item, ast.ClassDef):
            if item.name == "Setup":
                continue

            metrics_dict[item.name] = item

    return metrics_dict

def get_function_dict(module_ast: ast.Module) -> dict:
    """
    Get function dictionary
    """
    function_dict = dict()

    for item in module_ast.body:
        if isinstance(item, ast.FunctionDef):
            function_dict[item.name] = item

    return function_dict


def get_metric_name(metric_ast: ast.ClassDef) -> str | None:
    """
    Get metric name
    """
    for assign in metric_ast.body:
        if isinstance(assign, ast.Assign):
            assign_target: ast.Name = assign.targets[0]
            if assign_target.id != "name":
                continue

            assign_value: ast.Constant = assign.value
            return assign_value.s

    return None

def get_metric_domain(metric_ast: ast.ClassDef) -> str | None:
    """
    Get metric domain
    """
    for assign in metric_ast.body:
        if isinstance(assign, ast.Assign):
            assign_target: ast.Name = assign.targets[0]
            if assign_target.id != "domain":
                continue

            assign_value: ast.Constant = assign.value
            return assign_value.s

    return None

def get_metric_area(metric_ast: ast.ClassDef) -> str | None:
    """
    Get metric area
    """
    for assign in metric_ast.body:
        if isinstance(assign, ast.Assign):
            assign_target: ast.Name = assign.targets[0]
            if assign_target.id != "area":
                continue

            assign_value: ast.Constant = assign.value
            return assign_value.s

    return None

def get_metric_desc(metric_ast: ast.ClassDef) -> str | None:
    """
    Get metric description
    """
    for assign in metric_ast.body:
        if isinstance(assign, ast.Assign):
            assign_target: ast.Name = assign.targets[0]
            if assign_target.id != "desc":
                continue

            assign_value: ast.Constant = assign.value
            return assign_value.s.replace("\n", " ").replace("  ", " ").replace("  ", " ").strip()

    return None


def get_metric_max_val(metric_ast: ast.ClassDef) -> str | None:
    """
    Get metric maximum value
    """
    for assign in metric_ast.body:
        if isinstance(assign, ast.Assign):
            assign_target: ast.Name = assign.targets[0]
            if assign_target.id != "maxval":
                continue

            assign_value: ast.Constant = assign.value
            if isinstance(assign_value, ast.Constant):
                if assign_value.s in ["0", 0, 0.0]:
                    return None
                else:
                    return str(assign_value.s)
            else:
                return ast.unparse(assign_value)

    return None

def get_metric_metric_group(metric_ast: ast.ClassDef) -> List[str] | None:
    """
    Get metric maximum value
    """
    for assign in metric_ast.body:
        if isinstance(assign, ast.Assign):
            assign_target: ast.Name = assign.targets[0]
            if assign_target.id != "metricgroup":
                continue

            assign_value: ast.List = assign.value
            elements = []
            for elem in (assign_value.elts):
                elements.append(elem.s)
            return elements

    return None

def get_metric_sample(metric_ast: ast.ClassDef) -> List[str] | None:
    """
    Get metric sample
    """
    for assign in metric_ast.body:
        if isinstance(assign, ast.Assign):
            assign_target: ast.Name = assign.targets[0]
            if assign_target.id != "sample":
                continue

            assign_value: ast.List = assign.value
            elements = []
            for elem in (assign_value.elts):
                elements.append(elem.s)
            return elements

    return None


def get_metric_threshold(metric_ast: ast.ClassDef) -> str | None:
    """
    Get metric threshold
    """
    for func in metric_ast.body:
        if isinstance(func, ast.FunctionDef):
            func_try: ast.Try = func.body[0]
            if isinstance(func_try, ast.Try):
                threshold_assign: ast.Assign = func_try.body[-1]
                threshold_assign_target: ast.Attribute = threshold_assign.targets[0]
                if threshold_assign_target.attr != "thresh":
                    continue

                threshold_assign_value_ast = simplify_ast(threshold_assign.value)
                threshold_assign_value = ast.unparse(threshold_assign_value_ast)
                return threshold_assign_value
    return None

def get_metric_formula(metric_ast: ast.ClassDef) -> str | None:
    """
    Get metric formula
    """
    for func in metric_ast.body:
        if isinstance(func, ast.FunctionDef):
            func_try = func.body[0]
            if isinstance(func_try, ast.Try):
                formula_assign: ast.Assign = func_try.body[0]
                formula_assign_target: ast.Attribute = formula_assign.targets[0]
                if formula_assign_target.attr != "val":
                    continue

                formula_assign_value_ast = simplify_ast(formula_assign.value)
                formula_assign_value = ast.unparse(formula_assign_value_ast)
                return formula_assign_value
            elif isinstance(func_try, ast.Return):
                formula_return_value_ast = simplify_ast(func_try.value)
                formula_return_value = ast.unparse(formula_return_value_ast)
                return formula_return_value

    return None

def get_metric_reference(metric_ast: ast.ClassDef) -> str | None:
    """
    Get metric formula
    """
    for func in metric_ast.body:
        if isinstance(func, ast.FunctionDef):
            func_try = func.body[0]
            if isinstance(func_try, ast.Try):
                formula_assign: ast.Assign = func_try.body[0]
                formula_assign_target: ast.Attribute = formula_assign.targets[0]
                if formula_assign_target.attr != "val":
                    continue

                formula_assign_value_ast = simplify_ast(formula_assign.value)
                reference_list = collect_name_from_ast(formula_assign_value_ast)
                return reference_list
            elif isinstance(func_try, ast.Return):
                formula_return_value_ast = simplify_ast(func_try.value)
                reference_list = collect_name_from_ast(formula_return_value_ast)
                return reference_list

    return None


def get_function_formula(function_ast: ast.ClassDef) -> str | None:
    """
    Get function formula
    """
    if isinstance(function_ast.body[0], ast.Return):
        return_ast: ast.Return = function_ast.body[0]
        formula_ast = simplify_ast(return_ast.value)
        formula_ast_str = ast.unparse(formula_ast)
        return formula_ast_str
    elif isinstance(function_ast.body[0], ast.Assign):
        assign_ast: ast.Assign = function_ast.body[0]
        formula_ast = simplify_ast(assign_ast.value)
        formula_ast_str = ast.unparse(formula_ast)
        return formula_ast_str
    elif not isinstance(function_ast.body[0], ast.Return) \
            and not isinstance(function_ast.body[0], ast.Assign):
        return_ast: ast.Return = function_ast.body[-1]
        formula_ast = simplify_ast(return_ast.value)
        formula_ast_str = ast.unparse(formula_ast)
        return formula_ast_str

    return None

def get_function_reference(function_ast: ast.ClassDef) -> str | None:
    """
    Get function formula
    """
    if isinstance(function_ast.body[0], ast.Return):
        return_ast: ast.Return = function_ast.body[0]
        formula_ast = simplify_ast(return_ast.value)
        reference_list = collect_name_from_ast(formula_ast)
        return reference_list
    elif isinstance(function_ast.body[0], ast.Assign):
        assign_ast: ast.Assign = function_ast.body[0]
        formula_ast = simplify_ast(assign_ast.value)
        reference_list = collect_name_from_ast(formula_ast)
        return reference_list
    elif not isinstance(function_ast.body[0], ast.Return) \
            and not isinstance(function_ast.body[0], ast.Assign):
        return_ast: ast.Return = function_ast.body[-1]
        formula_ast = simplify_ast(return_ast.value)
        reference_list = collect_name_from_ast(formula_ast)
        return reference_list

    return None
