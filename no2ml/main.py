""" main file for package """
import os
import argparse
from pathlib import Path

from no2ml.core import html2latex


def main():
    """ main func for cmd """
    print("no2ml: parse notion html to latex")

    # argparse
    parser = argparse.ArgumentParser(description='Test.')
    parser.add_argument('source', type=str, help='The Source File')
    parser.add_argument('target', type=str, help='The Target File')
    args = parser.parse_args()

    # io file
    work_dir = os.getcwd()
    source_file = Path(work_dir, args.source)
    target_file = Path(work_dir, args.target)

    # core
    html = read_text(source_file)

    latex = html2latex(html)

    write_text(target_file, latex)


def read_text(file) -> str:
    """ read html to text """
    return Path(file).read_text("UTF8")


def write_text(filepath, text):
    """ write latex text to file """
    Path(filepath).write_text(text)
