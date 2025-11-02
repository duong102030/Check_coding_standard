#!/usr/bin/env python3
import sys
import os
from datetime import datetime

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_C = os.path.join(SCRIPT_DIR, "templates", "template_c.txt")
TEMPLATE_H = os.path.join(SCRIPT_DIR, "templates", "template_h.txt")

def insert_template(file_path, template_path):
    with open(template_path, "r", encoding="utf-8") as f:
        template = f.read()

    # Thay thế các placeholder
    today = datetime.now().strftime("%B %d, %Y")
    filename = os.path.basename(file_path)
    template = template.replace("${DISCLAIMER_PLACEHOLDER}", f"{filename}\n *\n *  Created on: {today}\n *      Author: Nguyen Kha Duong")

    with open(file_path, "w", encoding="utf-8") as f:
        f.write(template)

def has_content(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read().strip()
    return len(content) > 0

def process_file(file_path):
    _, ext = os.path.splitext(file_path)
    if ext not in [".c", ".h"]:
        return

    if not has_content(file_path):
        template_path = TEMPLATE_C if ext == ".c" else TEMPLATE_H
        insert_template(file_path, template_path)
        print(f"[NKD Hook] Added coding standard to empty file: {file_path}")
    else:
        # TODO: Smart rearrange (Includes, Macros, Functions, etc.)
        print(f"[NKD Hook] Checked format for {file_path}")

def main():
    for file_path in sys.argv[1:]:
        process_file(file_path)

if __name__ == "__main__":
    main()
