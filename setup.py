"""Setup file for the library."""

from pathlib import Path

from setuptools import find_packages, setup

from moadaly.__about__ import (
    APP_VERSION,
    __author__,
    __description__,
    __license__,
    __maintainer__,
)

HERE = Path(__file__).parent

README = (HERE / "README.md").read_text()

URL = "https://github.com/zer0-x/moadaly"
ISSUES = "https://github.com/zer0-x/moadaly/issues"
CHANGELOG = "https://github.com/zer0-x/moadaly/blob/main/CHANGELOG.md"

setup(
    name="moadaly",
    version=APP_VERSION,
    author=__author__,
    maintainer=__maintainer__,
    license=__license__,
    description=__description__,
    long_description_content_type="text/markdown",
    long_description=README,
    url=URL,
    project_urls={
        "Issues": ISSUES,
        "Changelog": CHANGELOG,
    },
    packages=find_packages(),
    entry_points={"console_scripts": ["moadaly = moadaly.__main__:main"]},
    keywords=[
        "gpa",
        "gpa-calculator",
        "cgpa",
        "qt6",
        "pyside6",
        "gpa-calculation-tool",
        "gui-application",
        "linux_desktop",
        "database-gui",
    ],
    classifiers=[
        "Environment :: X11 Applications :: Qt",
        "Environment :: X11 Applications :: KDE",
        "Intended Audience :: End Users/Desktop",
        "Intended Audience :: Education",
        "Topic :: Database",
        "Topic :: Database :: Front-Ends",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
    ],
)
