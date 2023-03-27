"""
Parse TMA configuration and generate report.
"""

import os
import argparse
import ast

import parse_tma
from report_index import generate_index

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


def __print_metric(metric_ast: ast.ClassDef,
                   metrics_dict: dict,
                   function_dict: dict) -> str:

    # name = parse_tma.get_metric_name(metric_ast)
    domain = parse_tma.get_metric_domain(metric_ast)
    max_val = parse_tma.get_metric_max_val(metric_ast)
    area = parse_tma.get_metric_area(metric_ast)
    metric_group = parse_tma.get_metric_metric_group(metric_ast)
    desc = parse_tma.get_metric_desc(metric_ast)
    sample = parse_tma.get_metric_sample(metric_ast)
    threshold = parse_tma.get_metric_threshold(metric_ast)

    report_str = ""

    if desc:
        report_str = report_str + desc + "\n\n"
    if domain:
        report_str = report_str + "- Domain: " + domain + "\n"
    if max_val:
        report_str = report_str + "- Max value: " + max_val + "\n"
    if threshold:
        report_str = report_str + "- Threshold: " + threshold + "\n"
    if area:
        report_str = report_str + "- Area: " + area + "\n"
    if metric_group:
        report_str = report_str + "- Metric group: " + ", ".join(metric_group) + "\n"
    if sample:
        report_str = report_str + "- sample: " + ", ".join(sample) + "\n"
    report_str = report_str + "\n"

    formula_list, ref_metric_list = __formula_reference_iter(metric_ast, function_dict)

    if formula_list:
        report_str = report_str + "```python\n" + "\n".join(formula_list) + "\n```\n\n"

    for item in ref_metric_list:
        if item in metrics_dict:
            report_str = report_str + f"- [{item}](#{item.lower()})\n"
        else:
            report_str = report_str + f"- {item}\n"

    report_str = report_str + "\n"

    return report_str


def __print_decision_tree_iter(child_dict: dict, metrics_dict: dict, function_dict: dict,
                               parent: str, header="#", index="1"):
    report_str = ""
    report_str = report_str + header + " " + index + " " \
        + "<a id=\"" + parent.lower() + "\">" + parent + "</a>" + "\n\n"
    report_str = report_str + __print_metric(metrics_dict[parent],
                                             function_dict=function_dict,
                                             metrics_dict=metrics_dict)

    for child_idx, child in enumerate(child_dict[parent], 1):
        new_idx = f"{child_idx}" if index=="" else f"{index}.{child_idx}"
        report_str = report_str + __print_decision_tree_iter(child_dict=child_dict,
                                                             metrics_dict=metrics_dict,
                                                             function_dict=function_dict,
                                                             parent=child,
                                                             header=header + "#",
                                                             index=new_idx)

    return report_str


def generate_report(tma_file: str,
                    report_file: str):
    """
    Generate reports of TMA configuration.
    """
    module_ast = parse_tma.get_ast(file_path=tma_file)

    metrics_dict = parse_tma.get_metrics_dict(module_ast=module_ast)
    function_dict = parse_tma.get_function_dict(module_ast=module_ast)

    top_level, child_dict = parse_tma.get_decision_tree(module_ast=module_ast)

    decision_tree_metrics_list = list(child_dict.keys())
    general_metrics_list = list(set(metrics_dict.keys()) - set(decision_tree_metrics_list))

    report_str=""

    for idx, item in enumerate(top_level, 1):
        report_str = report_str + __print_decision_tree_iter(child_dict=child_dict,
                                                             metrics_dict=metrics_dict,
                                                             function_dict=function_dict,
                                                             parent=item,
                                                             header="#",
                                                             index=f"{idx}")

    section_idx = len(top_level) + 1
    subsection_idx = 1
    report_str = report_str + f"# {section_idx} General Metrics\n\n"
    for item in general_metrics_list:
        report_str = report_str + \
            f"## {section_idx}.{subsection_idx} <a id=\"{item.lower()}\">{item}</a>\n\n"
        report_str = report_str + __print_metric(metrics_dict[item],
                                                 metrics_dict=metrics_dict,
                                                 function_dict=function_dict)
        subsection_idx = subsection_idx + 1

    with open(report_file, "w", encoding="utf-8") as file_obj:
        file_obj.write(report_str)

    print(f"{tma_file} --> {report_file}")

def main():
    """
    Main function of command.
    """
    # Command line
    cmdline = argparse.ArgumentParser(prog="report_tma")
    cmdline.add_argument("--tma_file", default="",
                         help="File path of TMA configuration.")
    cmdline.add_argument("--report_file", default="",
                         help="File path of TMA report.")
    cmdline.add_argument("--all", action="store_true")
    args = cmdline.parse_args()

    if args.all:
        known_cpus = [
            "snb_client_ratios",
            "jkt_server_ratios",
            "ivb_client_ratios",
            "ivb_server_ratios",
            "hsw_client_ratios",
            "hsx_server_ratios",
            #"slm_ratios",
            "bdx_server_ratios",
            "bdw_client_ratios",
            "skl_client_ratios",
            #"knl_ratios",
            "skx_server_ratios",
            "clx_server_ratios",
            "icl_client_ratios",
            "icx_server_ratios",
            "adl_glc_ratios",
            "adl_grt_ratios",
            "spr_server_ratios",
            "ehl_ratios"
        ]
        root_folder = os.path.dirname(os.path.dirname(__file__))
        for cpu in known_cpus:
            generate_report(tma_file=root_folder + "/pmu-tools/" + cpu + ".py",
                            report_file=root_folder + "/reports/" + cpu + ".md")

        v45 = [
            "snb_client_ratios",
            "jkt_server_ratios",
            "ivb_client_ratios",
            "ivb_server_ratios",
            "hsw_client_ratios",
            "hsx_server_ratios",
            "bdx_server_ratios",
            "bdw_client_ratios",
            "skl_client_ratios",
            "skx_server_ratios",
            "clx_server_ratios",
            "icl_client_ratios",
            "icx_server_ratios",
            "adl_glc_ratios",
            "spr_server_ratios"
        ]

        v20 = [
            #"knl_ratios",
            #"slm_ratios",
            "adl_grt_ratios",
            "ehl_ratios"
        ]

        generate_index(tma_file_list=[root_folder + "/pmu-tools/" + cpu + ".py" \
                                      for cpu in v20],
                       report_file=root_folder + "/reports/index_v20.md")
        generate_index(tma_file_list=[root_folder + "/pmu-tools/" + cpu + ".py" \
                                      for cpu in v45],
                       report_file=root_folder + "/reports/index_v45.md")

    else:
        if not os.path.exists(args.tma_file):
            raise FileNotFoundError(args.tma_file)
        if not os.path.exists(os.path.dirname(args.report_file)):
            raise FileNotFoundError(args.report_file)

        generate_report(tma_file=args.tma_file,
                        report_file=args.report_file)

if __name__ == "__main__":
    main()
