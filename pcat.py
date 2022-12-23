#!/usr/bin/env python3
import sys
from rich import print as rprint
import os
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("files", nargs="*")
parser.add_argument("-b","--banner", dest="banner", action="store_true", help="shows the name of the file")
parser.add_argument("-n", "--number", dest="number", action="store_true", help="shows the line number")
parser.add_argument("-e", "--show-ends", dest="ends", action="store_true", help="displays $ at the end of each line")

args = parser.parse_args()
def check_files(files:list):
    for file in files:
        if not os.path.exists(file):
            rprint(f"[red]\[pcat error][/red]: \"{file}\": No such file or directory (os error 1)")
            sys.exit(1)
        
def main():
    files = args.files
    check_files(files)
    for current_file in files:
        with open(current_file, "r") as file:
            lines = file.readlines()
            if args.banner:
                print(f"CONTENTS OF {current_file}\n{'-'*(12+len(current_file))}")
            elif len(files) > 1:
                print() # spaces out each file
            for number,line in enumerate(lines, start=1):
                line = line.replace("\n","")
                line = f"{line}$" if args.ends else line
                print(f"{number} {line}" if args.number else line)

if __name__ == "__main__":
    main()