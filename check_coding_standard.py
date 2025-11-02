#!/usr/bin/env python3
import sys
import os

# === Absolute paths for templates ===
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_C = os.path.join(SCRIPT_DIR, "templates", "template_c.txt")
TEMPLATE_H = os.path.join(SCRIPT_DIR, "templates", "template_h.txt")


def insert_template(file_path, template_path):
    """Insert NKD coding standard layout for empty C/H files"""
    with open(template_path, "r", encoding="utf-8") as f:
        template_body = f.read()

    # Ghi nội dung layout vào file
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(template_body)


def has_content(file_path):
    """Check if file is empty or not"""
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read().strip()
    return len(content) > 0


def process_file(file_path):
    """Process .c/.h file"""
    _, ext = os.path.splitext(file_path)
    if ext not in [".c", ".h"]:
        return

    if not has_content(file_path):
        template_path = TEMPLATE_C if ext == ".c" else TEMPLATE_H
        insert_template(file_path, template_path)
        print(f"[NKD Hook] Added coding standard layout to empty file: {file_path}")
    else:
        print(f"[NKD Hook] Checked existing file: {file_path}")


def main():
    for file_path in sys.argv[1:]:
        process_file(file_path)


if __name__ == "__main__":
    main()
