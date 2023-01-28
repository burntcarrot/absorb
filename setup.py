from setuptools import setup, find_packages

setup(
    name="absorb",
    version="0.1.2",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "Click",
        "rich",
        "python-json-logger",
        "gitpython",
        "click-plugins",
    ],
    entry_points="""
        [console_scripts]
        absorb = absorb.main:cli
    """,
)
