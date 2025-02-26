from setuptools import setup, find_packages
from setuptools.config.expand import entry_points

setup(
    name="pymysqlhelper",
    version="1.2.0",
    description="A simple MySQL database helper for easy interactions",
    author="DEAMJAVA",
    author_email="deamminecraft3@gmail.com",
    packages=find_packages(),
    install_requires=["pymysql", "sqlalchemy"],
    python_requires=">=3.6",
    entry_points={"console_scripts":["pymysqlhelper = pymysqlhelper:pymysqlhelper"]}
)
