#!/usr/bin/env python3
import sys
from rich import print as rprint
import os
import argparse
import edited_imghdr
from edited_image import DrawImage
from typing import List
import PIL

parser = argparse.ArgumentParser()
# make banner & number default
# get plain to disable number and banner
parser.add_argument("files", nargs="*")
parser.add_argument(
    "-n",
    "--no-number",
    dest="number",
    default=True,
    action="store_false",
    help="shows the line number",
)
parser.add_argument(
    "-b",
    "--no-banner",
    dest="banner",
    default=True,
    action="store_false",
    help="shows the name of the file",
)
parser.add_argument(
    "-e",
    "--show-ends",
    dest="ends",
    default=False,
    action="store_true",
    help="displays $ at the end of each line",
)
parser.add_argument(
    "-p",
    "--plain",
    dest="plain",
    default=False,
    action="store_true",
    help="disables banner and line number",
)
args = parser.parse_args()


def is_image_file(filename: str) -> bool:
    return edited_imghdr.what(filename) is not None


def check_files(files: List[str]) -> None:
    for file in files:
        if not os.path.exists(file):
            rprint(
                f'[red]\[pcat error][/red]: "{file}": No such file or directory (os error 1)'
            )
            sys.exit(1)


def read_file(files: List[str]) -> None:
    if args.plain:
        args.banner = False
        args.number = False
    # files = args.files
    show_banner = args.banner
    show_number = args.number
    files = [files]
    check_files(files)
    for current_file in files:
        with open(current_file, "r") as file:
            lines = file.readlines()
            if show_banner:
                print(f"CONTENTS OF {current_file}\n{'-'*(12+len(current_file))}")
            elif len(files) > 1:
                print()  # spaces out each file
            for number, line in enumerate(lines, start=1):
                line = line.replace("\n", "")
                line = f"{line}$" if args.ends else line
                print(f"{number} {line}" if show_number else line)


def display_image(filename: str):
    print(f"SHOWING {filename}\n{'-'*(8+len(filename))}")
    DrawImage.from_file(filename, size=(40, 20)).draw_image()


if __name__ == "__main__":
    for file in args.files:
        try:
            if is_image_file(file):
                display_image(file)
                continue
        except PIL.UnidentifiedImageError:
            read_file(file)
        else:
            read_file(file)
