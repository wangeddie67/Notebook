"""
Parse TMA configuration and generate report.
"""

import os
from typing import List, Dict
import ast

import parse_tma

def __collect_all_decision_tree(cpu_dict: List):
    top_level_all = []
    child_dict_all = dict()

    for cpu_item in cpu_dict:
        top_level: List = cpu_item[1]
        child_dict: Dict[str, List[str]] = cpu_item[2]

        for item in top_level:
            if item not in top_level_all:
                top_level_all.append(item)

        for key, value in child_dict.items():
            if key not in child_dict_all:
                child_dict_all[key] = value
            else:
                for item in value:
                    if item not in child_dict_all[key]:
                        child_dict_all[key].append(item)

    return top_level_all, child_dict_all


def __collect_all_metrics(cpu_dict):
    metrics_list_all = []

    for cpu_item in cpu_dict:
        metrics_list: List[str] = cpu_item[3]

        for item in metrics_list:
            if item not in metrics_list_all:
                metrics_list_all.append(item)

    return metrics_list_all


def __formula_reference_iter(ast_def: ast.ClassDef | ast.FunctionDef,
                             function_dict: dict):
    if isinstance(ast_def, ast.ClassDef):
        formula = ast_def.name + " = " + parse_tma.get_metric_formula(ast_def)
        reference_list = parse_tma.get_metric_reference(ast_def)
    else:
        formula = ast_def.name + " = " + parse_tma.get_function_formula(ast_def)
        reference_list = parse_tma.get_function_reference(ast_def)
    formula_list = [formula]

    ref_metric = []
    for reference in reference_list:
        if reference in function_dict:
            sub_formula_list, sub_ref_list = \
                __formula_reference_iter(function_dict[reference], function_dict)
            formula_list = sub_formula_list + formula_list
            ref_metric.extend(sub_ref_list)
        else:
            ref_metric.append(reference)

    formula_list_1 = []
    for item in formula_list:
        if item not in formula_list_1:
            formula_list_1.append(item)

    ref_metric_1 = []
    for item in ref_metric:
        if item not in ref_metric_1:
            ref_metric_1.append(item)
    return formula_list_1, ref_metric_1


def __print_metric(metric: str,
                   cpu_dict: dict) -> str:
    report_str = ""
    report_str = report_str + "|"
    for item in cpu_dict:
        name = item[0]
        md_name = name.replace(".py", ".md")
        child_dict = item[2]
        metric_list = item[3]

        if metric in child_dict or metric in metric_list:
            report_str = report_str \
                + f" [:heavy_check_mark:]({md_name}#{metric.lower()}) |"
        else:
            report_str = report_str + "  |"

    return report_str


def __print_table_head(cpu_list: list) -> str:
    report_str = ""
    report_str = report_str + "| Metrics | " \
        + " | ".join([x.replace("_ratios.py", "") for x in cpu_list]) + " |\n"
    report_str = report_str + "| ---- |" + " :----: |" * len(cpu_list) + "\n"
    return report_str


def __print_decision_tree_iter(child_dict: dict, cpu_dict: List,
                               parent: str, header="#", index="1"):
    report_str = ""
    report_str = report_str + "| " + index + " " + parent + " "
    report_str = report_str + __print_metric(parent,
                                             cpu_dict=cpu_dict) + "\n"

    for child_idx, child in enumerate(child_dict[parent], 1):
        new_idx = f"{child_idx}" if index=="" else f"{index}.{child_idx}"
        report_str = report_str + __print_decision_tree_iter(child_dict=child_dict,
                                                             cpu_dict=cpu_dict,
                                                             parent=child,
                                                             header=header + "#",
                                                             index=new_idx)

    return report_str


def generate_index(tma_file_list: List[str],
                   report_file: str):
    """
    Generate reports of TMA configuration.
    """
    cpu_dict = []
    for tma_file in tma_file_list:
        module_ast = parse_tma.get_ast(file_path=tma_file)

        metrics_dict = parse_tma.get_metrics_dict(module_ast=module_ast)

        top_level, child_dict = parse_tma.get_decision_tree(module_ast=module_ast)

        decision_tree_metrics_list = list(child_dict.keys())
        general_metrics_list = list(set(metrics_dict.keys()) - set(decision_tree_metrics_list))

        cpu_dict.append([os.path.basename(tma_file), top_level, child_dict, general_metrics_list])

    top_level_all, child_dict_all = __collect_all_decision_tree(cpu_dict)
    metrics_list_all = __collect_all_metrics(cpu_dict)

    report_str=""

    report_str = report_str + "# Decision Tree\n\n"
    report_str = report_str + __print_table_head([x[0] for x in cpu_dict])
    for idx, item in enumerate(top_level_all, 1):
        report_str = report_str + __print_decision_tree_iter(child_dict=child_dict_all,
                                                             cpu_dict=cpu_dict,
                                                             parent=item,
                                                             header="#",
                                                             index=f"{idx}")

    section_idx = len(top_level_all) + 1
    subsection_idx = 1
    report_str = report_str + "# General Metrics\n\n"
    report_str = report_str + __print_table_head([x[0] for x in cpu_dict])
    for item in metrics_list_all:
        report_str = report_str + \
            f"| {section_idx}.{subsection_idx} {item} "
        report_str = report_str + __print_metric(item,
                                                 cpu_dict=cpu_dict) + "\n"
        subsection_idx = subsection_idx + 1

    with open(report_file, "w", encoding="utf-8") as file_obj:
        file_obj.write(report_str)

    print(f"Report metrics index {report_file}.")
