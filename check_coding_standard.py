#!/usr/bin/env python3
import sys
import os
from datetime import datetime

# -------------------------------
# COPYRIGHT SECTION
# -------------------------------

AUTHOR = "Nguyen Kha Duong"
CONTACT = "duong nguyen kha.daniel@gmail.com"

def get_copyright_header(filename):
    """Return the copyright header text."""
    today = datetime.now().strftime("%B %d, %Y")
    header = f"""/*
 * {os.path.basename(filename)}
 *
 *  Created on: {today}
 *      Author: {AUTHOR}
 *      Contact via email: {CONTACT}
 */"""
    return header

def has_copyright(content):
    """Check if file already has NKD copyright header."""
    return "Author: Nguyen Kha Duong" in content or "Created on:" in content


# -------------------------------
# CODING STANDARD SECTION
# -------------------------------

# Absolute paths for templates
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_C = os.path.join(SCRIPT_DIR, "templates", "template_c.txt")
TEMPLATE_H = os.path.join(SCRIPT_DIR, "templates", "template_h.txt")


def insert_coding_standard(file_path, template_path, header_text):
    """Insert copyright + NKD coding standard layout"""
    with open(template_path, "r", encoding="utf-8") as f:
        template_body = f.read().strip()

    final_content = header_text.strip() + "\n\n" + template_body + "\n"
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(final_content)


def prepend_header_to_existing_file(file_path, header_text):
    """Insert copyright header at top if not present"""
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    new_content = header_text.strip() + "\n\n" + content
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(new_content)
    print(f"[NKD Hook] Added copyright header to: {file_path}")


def has_content(file_path):
    """Check if file is empty or not"""
    with open(file_path, "r", encoding="utf-8") as f:
        return len(f.read().strip()) > 0


def process_file(file_path):
    """Process C/H file for both copyright and layout"""
    _, ext = os.path.splitext(file_path)
    if ext not in [".c", ".h"]:
        return

    header_text = get_copyright_header(file_path)

    if not has_content(file_path):
        # File rỗng → thêm cả header + layout
        template_path = TEMPLATE_C if ext == ".c" else TEMPLATE_H
        insert_coding_standard(file_path, template_path, header_text)
        print(f"[NKD Hook] Added copyright + coding standard layout to: {file_path}")
    else:
        # File có nội dung → chỉ thêm header nếu chưa có
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
        if not has_copyright(content):
            prepend_header_to_existing_file(file_path, header_text)
        else:
            print(f"[NKD Hook] Checked existing file: {file_path} (OK)")


def main():
    for file_path in sys.argv[1:]:
        process_file(file_path)


if __name__ == "__main__":
    main()
