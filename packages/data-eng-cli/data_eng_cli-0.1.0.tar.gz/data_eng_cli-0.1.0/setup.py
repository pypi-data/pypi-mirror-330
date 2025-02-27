# from setuptools import setup, find_packages

# setup(
#     name="data-eng-cli",
#     version="0.1",
#     packages=find_packages(),
#     install_requires=[
#         "click",
#         "pandas",
#         "requests",
#         "pyyaml"
#     ],
#     entry_points={
#         "console_scripts": [
#             "data-eng-cli = data_eng_cli.cli:cli"
#         ]
#     },
# )
from setuptools import setup, find_packages

setup(
    name="data-eng-cli",
    version="0.1.0",
    author="Vic Kibira",
    author_email="victorahonakibira@gmail.com",
    description="A simple CLI tool for data engineering tasks",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/vicKibira/CLI",
    packages=find_packages(),
    install_requires=[
        "click",
        "sqlalchemy",
        "duckdb",
        "pymysql"
    ],
    entry_points={
        "console_scripts": [
            "data-eng-cli=data_eng_cli.cli:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)
