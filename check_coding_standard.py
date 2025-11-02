#!/usr/bin/env python3
import sys
import os
import argparse
from datetime import datetime

# ============================================================
# CONFIGURATION
# ============================================================

AUTHOR = "Nguyen Kha Duong"
CONTACT = "duongnguyenkha.daniel@gmail.com"

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_C = os.path.join(SCRIPT_DIR, "templates", "template_c.txt")
TEMPLATE_H = os.path.join(SCRIPT_DIR, "templates", "template_h.txt")

# ============================================================
# COPYRIGHT SECTION
# ============================================================

def get_copyright_header(filename):
    """Generate NKD copyright header text."""
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
    """Check if file already contains NKD copyright header."""
    return "Author: Nguyen Kha Duong" in content or "Created on:" in content


def prepend_header_to_existing_file(file_path, header_text):
    """Insert copyright header at top of file if not present."""
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    new_content = header_text.strip() + "\n\n" + content
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(new_content)

    print(f"[NKD Hook] Added copyright header to: {file_path}")

# ============================================================
# CODING STANDARD SECTION
# ============================================================

def insert_coding_standard(file_path, template_path=None, header_text=None):
    """
    Insert NKD coding standard layout and/or copyright header.

    If template_path is None → only header will be added.
    If header_text is None → only coding layout will be added.
    """
    template_body = ""

    # Load layout if available
    if template_path:
        with open(template_path, "r", encoding="utf-8") as f:
            template_body = f.read().strip()

    # Combine layout + header according to mode
    if header_text and template_body:
        final_content = header_text.strip() + "\n\n" + template_body + "\n"
    elif header_text:
        final_content = header_text.strip() + "\n"
    elif template_body:
        final_content = template_body + "\n"
    else:
        # This case should never happen, but we guard it
        print(f"[NKD Hook] Warning: no header or template provided for {file_path}")
        return

    # Write final content
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(final_content)


def has_content(file_path):
    """Check whether file has any content."""
    with open(file_path, "r", encoding="utf-8") as f:
        return len(f.read().strip()) > 0

# ============================================================
# MAIN PROCESSING LOGIC
# ============================================================

def process_file(file_path, mode):
    """Apply the chosen NKD processing mode on a single file."""
    _, ext = os.path.splitext(file_path)
    if ext not in [".c", ".h"]:
        return

    header_text = get_copyright_header(file_path)

    # --- Case 1: File is empty ---
    if not has_content(file_path):
        template_path = TEMPLATE_C if ext == ".c" else TEMPLATE_H

        if mode == "both":
            insert_coding_standard(file_path, template_path, header_text)
            print(f"[NKD Hook] Added copyright + coding standard layout to: {file_path}")

        elif mode == "style":
            insert_coding_standard(file_path, template_path)
            print(f"[NKD Hook] Added coding standard layout to: {file_path}")

        elif mode == "copyright":
            insert_coding_standard(file_path, template_path=None, header_text=header_text)
            print(f"[NKD Hook] Added copyright header only to empty file: {file_path}")

        return

    # --- Case 2: File has existing content ---
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    if mode in ["copyright", "both"] and not has_copyright(content):
        prepend_header_to_existing_file(file_path, header_text)

    print(f"[NKD Hook] Checked existing file: {file_path} (OK)")

# ============================================================
# ENTRY POINT
# ============================================================

def main():
    parser = argparse.ArgumentParser(
        description="NKD pre-commit coding standard & copyright tool"
    )
    parser.add_argument(
        "--mode",
        choices=["copyright", "style", "both"],
        default="both",
        help="Select mode: copyright / style / both",
    )
    parser.add_argument("files", nargs="*", help="Files to process")
    args = parser.parse_args()

    if not args.files:
        print("[NKD Hook] No files to process.")
        sys.exit(0)

    for file_path in args.files:
        if os.path.isfile(file_path):
            process_file(file_path, args.mode)

if __name__ == "__main__":
    main()
