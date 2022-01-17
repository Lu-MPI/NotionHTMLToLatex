""" dom dict to latex """

import json


def dict2latex(dom_dict: dict):
    """ dict to latex """

    # 逐步替换，从外层开始，逐步替换为 latex

    # 每个标签增加 start 和 end

    latex = {}

    latex["_start"] = r"% this doc is gen by no2ml" + "\n" \
                      r"\documentclass{article}" + "\n" \
                      r"\usepackage[utf8]{inputenc}" + "\n\n" \

    latex["_inner"] = [
        _do_header(dom_dict["children"][0]),
        _do_document(dom_dict["children"][1]),
    ]

    latex["_end"] = "\n"

    latex_text = latex_dict_2_latex(latex)
    return latex_text


def latex_dict_2_latex(latex_dict):

    text = _merge_text(latex_dict)

    return text


def _merge_text(data: dict):

    inner_list = []
    if "_inner" in data:
        for inner in data["_inner"]:
            inner_list.append(_merge_text(inner))

    inner_text = ''.join(map(str, inner_list))
    # return "__start: " + data["_start"] + " __inner: " + inner_text + " __end: " + data["_end"]
    return data["_start"] + inner_text + data["_end"]


def _do_document(document: dict):
    latex = {}

    latex["_start"] = r"\begin{document}" + "\n" \
                      r"\maketitle" + "\n\n\n"

    inner = []

    for line in document["children"]:
        inner.append(_do_line(line))

    latex["_inner"] = inner

    latex["_end"] = r"\end{document}" + "\n"
    return latex


def _do_line(line: dict):

    line_tex = {
        "_start": None,
        "_inner": [],
        "_end": ""
    }
    if "name" in line:
        if line["name"] == "p":
            line_tex["_end"] = "\n\n"
            if "children" in line:
                line_tex["_start"] = ""
                for child in line["children"]:
                    line_tex["_inner"].append(_do_line(child))
                del line["children"]

            if len(list(line.keys())) == 2 and "content" in line:
                line_tex["_start"] = line["content"]

        if line["name"] == "a":
            line_tex["_start"] = r"\href{" + line["attr"]["href"] + "}{" + line["content"] + "}"

        if line["name"] == "h2":
            line_tex["_start"] = r"\section{" + line["children"][0]["content"] + "}"
            line_tex["_end"] = "\n\n"

        if line["name"] == "h3":
            line_tex["_start"] = r"\subsection{" + line["children"][0]["content"] + "}"
            line_tex["_end"] = "\n\n"

        if line["name"] == "ol":
            line_tex["_start"] = line["attr"]["start"] + ". " + line["children"][0]["content"]
            line_tex["_end"] = "\n\n"

        if line["name"] == "ul":
            line_tex["_start"] = "-  " + line["children"][0]["content"]
            line_tex["_end"] = "\n\n"

        if line["name"] == "strong":
            if "children" in line:
                line_tex["_start"] = r"\textbf{"
                for child in line["children"]:
                    line_tex["_inner"].append(_do_line(child))
                del line["children"]
                line_tex["_end"] = "}"
            if "content" in line:
                line_tex["_start"] = r"\textbf{" + line["content"] + "}"

    if len(list(line.keys())) == 1 and "content" in line:
        line_tex["_start"] = line["content"]

    if line_tex["_start"] is None:
        line_tex["_start"] = json.dumps(line, ensure_ascii=False)
        line_tex["_end"] = "\n\n"

    return line_tex


def _do_header(header: dict):
    title = header["children"][0]["children"][0]["content"]

    latex = r"\title{" + title + r"}" + "\n" \
            r"\author{The author}" + "\n\n"

    header = {
        "_start": latex,
        "_end": "\n"
    }

    return header
