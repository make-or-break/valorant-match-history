import pathlib
from importlib.metadata import entry_points

from setuptools import find_packages
from setuptools import setup

here = pathlib.Path(__file__).parent.resolve()

# Get the long description from the README file
long_description = (here / "README.md").read_text(encoding="utf-8")

requires = [
    "sqlalchemy>=1.4.37",
]

setup(
    name="valorant-match-history",
    version="0.2.0",
    description="A valorant match history scraper",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/make-or-break/valorant-match-history",
    license="",
    author="MayNiklas",
    author_email="info@niklas-steffen.de",
    project_urls={
        "Bug Reports": "https://github.com/make-or-break/valorant-match-history/issues",
        "Source": "https://github.com/make-or-break/valorant-match-history",
    },
    keywords="valorant-match-history",
    python_requires=">=3.8, <4",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Intended Audience :: Other Audience",
        "Topic :: Communications :: Chat",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3 :: Only",
        "Typing :: Typed",
    ],
    install_requires=requires,
    package_dir={"": "src/"},
    packages=find_packages(where="src/"),
    entry_points={
        "console_scripts": ["valorant-match-history=match_crawler:check_new_matches"]
    },
)
