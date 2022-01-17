""" to json """


class_black_list = ["bulleted-list", "page", "page-title", "page-body", "sans"]


def soup2dict(node) -> dict:
    """ convert soup dom to json """
    data = _soup2dict(node)

    data = data["children"][0]  # document >> html
    data = data["children"][1]  # html >> body
    data = data["children"][0]  # body >> article

    data = _filter(data)

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


def _filter(dict_data: dict):
    """ filter dict, make it easy to convert """

    if "children" in dict_data:
        children = []

        # process every child
        for child in dict_data["children"]:

            # skip empty child
            if child is None:
                continue

            # skip empty child (only name)
            if len(child.keys()) == 1 and "name" in child:
                continue

            # spec case
            if "children" in child:
                # child have one sub-child, only have content attr
                # move sub-child content to child
                if len(child["children"]) == 1 and "content" in child["children"][0]:
                    child["content"] = child["children"][0]["content"]
                    del child['children']

            # filter unuseful dict
            child = _filter(child)

            # skip empty child. must be checked last
            if child == {}:
                continue

            children.append(child)

        # set children
        dict_data["children"] = children

        # check children
        if len(dict_data["children"]) == 0:
            del dict_data["children"]

    # process attr
    if "attr" in dict_data:
        # remove id
        if "id" in dict_data["attr"]:
            del dict_data["attr"]["id"]

        # remove empty and black_list class
        if "class" in dict_data["attr"]:
            classes = dict_data["attr"]["class"]
            classes = [x for x in classes if x not in class_black_list]
            dict_data["attr"]["class"] = classes
            if len(dict_data["attr"]["class"]) == 0:
                del dict_data["attr"]["class"]

        # remove some style
        if "style" in dict_data["attr"]:
            if dict_data["attr"]["style"] == "list-style-type:disc":
                del dict_data["attr"]["style"]

        # remove empty attr dict
        if not dict_data["attr"]:
            del dict_data["attr"]

    # remove empty content
    if "content" in dict_data:
        if dict_data["content"] == "\n" or not dict_data["content"].strip():
            del dict_data["content"]

    # remove empty dom
    if len(dict_data.keys()) == 1 and "name" in dict_data:
        return {}

    return dict_data
