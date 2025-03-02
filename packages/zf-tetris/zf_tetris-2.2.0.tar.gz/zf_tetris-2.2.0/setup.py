from os import path as os_path
from sys import platform as sys_platform

import setuptools

PACKAGE_NAME = "zf-tetris"
AUTHOR_NAME = "Zeff Muks"
AUTHOR_EMAIL = "zeffmuks@gmail.com"

with open("README.md", "r") as f:
    readme = f.read()


def read_version():
    version_file = os_path.join(os_path.dirname(__file__), "tetris", "version.py")
    with open(version_file) as file:
        exec(file.read())
    version = locals()["__version__"]
    print(f"Building {PACKAGE_NAME} v{version}")
    return version

def read_requirements():
    install_requires = [
        line.strip() for line in open("requirements.txt").readlines() if not line.startswith("#") and line.strip() != ""
    ]
    return install_requires


setuptools.setup(
    name=PACKAGE_NAME,
    version=read_version(),
    author=AUTHOR_NAME,
    author_email=AUTHOR_EMAIL,
    description="tetris is a tool for identifying social media trends",
    license="PROPRIETARY",
    long_description=readme,
    long_description_content_type="text/markdown",
    install_requires=read_requirements(),
    packages=setuptools.find_packages(exclude=["tests*"]),
    package_data={
        "tetris": ["*.json", "*.pt", "*.dev"],
        "tetris.annotator": ["*"],
        "tetris.library": ["*"],
        "tetris.models": ["*"],
        "tetris.trender": ["*"],
    },
    data_files=[("tetris", ["tetris/.env.dev"])],
    include_package_data=True,
    exclude_package_data={"": ["*.pyc", "*.pyo", "*.pyd", "__pycache__", "*.so", ".DS_Store"]},
    entry_points={"console_scripts": ["tetris = tetris.__main__:cli"]},
)
