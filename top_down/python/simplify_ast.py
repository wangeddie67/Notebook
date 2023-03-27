"""
Simplify AST
"""

import ast
from typing import List

def simplify_ast(ast_complex: ast.stmt) -> ast.stmt:
    """
    Simplify unnecessary AST.
    """
    if isinstance(ast_complex, ast.Attribute):
        ast_value = ast_complex.value
        if isinstance(ast_value, ast.Name):
            if ast_value.id == "self" and ast_complex.attr == "val":
                return ast.Name(id="")
        elif isinstance(ast_value, ast.Attribute):
            ast_value_value = ast_value.value
            if isinstance(ast_value_value, ast.Name):
                if ast_value_value.id == "self" \
                        and ast_value.attr == "parent" and ast_complex.attr == "thresh":
                    return ast.Name(id="parent over threshold")

        return ast_complex

    elif isinstance(ast_complex, ast.Call):
        ast_func = ast_complex.func
        ast_args = ast_complex.args
        if isinstance(ast_func, ast.Name) and ast_func.id == "EV":
            # EV(reg, level)
            if isinstance(ast_args[0], ast.Constant):
                return ast.Name(id=ast_args[0].s)
        elif isinstance(ast_func, ast.Attribute) and len(ast_args) == 1 and ast_args[0].id == "EV":
            # self.regname.compute(EV)
            ast_func_value = ast_func.value
            if isinstance(ast_func_value, ast.Attribute) and ast_func_value.value.id == "self":
                return ast.Name(id=ast_func_value.attr)
        elif isinstance(ast_func, ast.Name) and len(ast_args) == 3:
            # name(self, EV, level)
            if isinstance(ast_args[0], ast.Name) and ast_args[0].id == "self" and \
                    isinstance(ast_args[1], ast.Name) and ast_args[1].id == "EV" and \
                    isinstance(ast_args[2], (ast.Constant, ast.Name)):
                return ast.Name(id=ast_func.id)

        # For normal function call, simplify arguments.
        ast_complex.args = [simplify_ast(x) for x in ast_complex.args]
        return ast_complex

    # Operators
    elif isinstance(ast_complex, ast.Compare):
        # self.val does not necessary in compare left.
        ast_complex.left = simplify_ast(ast_complex.left)
        ast_complex.comparators = [simplify_ast(x) for x in ast_complex.comparators]
        return ast_complex
    elif isinstance(ast_complex, ast.BoolOp):
        ast_complex.values = [simplify_ast(x) for x in ast_complex.values]
        return ast_complex
    elif isinstance(ast_complex, ast.BinOp):
        ast_complex.left = simplify_ast(ast_complex.left)
        ast_complex.right = simplify_ast(ast_complex.right)
        return ast_complex
    elif isinstance(ast_complex, ast.IfExp):
        ast_complex.test = simplify_ast(ast_complex.test)
        ast_complex.body = simplify_ast(ast_complex.body)
        ast_complex.orelse = simplify_ast(ast_complex.orelse)
        return ast_complex

    # Do nothing
    elif isinstance(ast_complex, ast.Constant):
        return ast_complex
    elif isinstance(ast_complex, ast.Name):
        return ast_complex
    elif isinstance(ast_complex, ast.Lambda):
        return ast_complex

    else:
        print(ast_complex)

    return ast_complex


def collect_name_from_ast(ast_complex: ast.stmt) -> List[str]:
    """
    Collect name from AST
    """
    name_list = []
    for node in ast.walk(ast_complex):
        if isinstance(node, ast.Name):
            if node.id and node.id not in ["max", "min"]:
                name_list.append(node.id)

    return list(set(name_list))
