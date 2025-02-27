from setuptools import setup, find_packages

setup(
    name="tppc",
    version="2.1.2",
    author="Sean Tichenor",
    author_email="sean.tichenor@olivia-tgdk.com",
    description="TPPC Interpreter for T++ Language",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/seantichenor/tppc",
    license="MIT",
    packages=find_packages(),
    python_requires=">=3.6",
    entry_points={
        "console_scripts": [
            "tppc=tppc.main:run"  # Corrected structure
        ],
    },
)
