""" core part """
from pathlib import Path
from bs4 import BeautifulSoup
import json


def html2latex(html_text):
    """ notion html to latex """

    print(html_text)

    soup = BeautifulSoup(html_text, "html.parser")

    dom_dict = soup2dict(soup)

    print(json.dumps(dom_dict, ensure_ascii=False))

    latex_text = dict2latex(dom_dict)

    return latex_text


def soup2dict(soup):
    """ TODO: parse soup to dict """
    return {}


def dict2latex(dom_dict):
    """ TODO: parse dom dict to latex """
    return ""


# for test without build and install
if __name__ == '__main__':
    html2latex(Path('Z:\\html\\test2.html').read_text("UTF8"))
