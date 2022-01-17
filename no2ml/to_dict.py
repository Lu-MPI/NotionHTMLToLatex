""" to json """


class_black_list = ["bulleted-list", "page", "page-title", "page-body", "sans"]


def soup2dict(node) -> dict:
    """ convert soup dom to json """
    data = _soup2dict(node)
    data = data["children"][0]  # document >> html
    data = data["children"][1]  # html >> body
    data = data["children"][0]  # body >> article

    # check is except notion note,
    # if any error, the html is not from notion, or notion html is updated
    assert len(data["children"]) == 2  # header and div
    assert data["children"][0]["name"] == "header"
    assert data["children"][1]["name"] == "div"

    return data


def _soup2dict(node):
    dom_dict = {}

    if hasattr(node, "name") and node.name:
        dom_dict['name'] = node.name

    if hasattr(node, "attrs") and node.attrs:
        dom_dict["attr"] = node.attrs

    if hasattr(node, "children"):
        dom_dict['children'] = [_soup2dict(child) for child in node.children if child is not None]
    else:
        dom_dict['content'] = node.string

    return dom_dict
