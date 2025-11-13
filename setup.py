from setuptools import setup

setup(
    name="check_coding_standard_nkd",
    version="1.0.0",
    description="Pre-commit hook to enforce NKD C coding standard and copyright header",
    author="Nguyen Kha Duong",
    author_email="duong.nguyen.kha.daniel@gmail.com",
    url="https://github.com/duong102030/Check_coding_standard.git",
    py_modules=["check_coding_standard"],
    entry_points={
        "console_scripts": [
            "check_coding_standard = check_coding_standard:main",
        ],
    },
    install_requires=[],
)
