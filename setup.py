from setuptools import setup, find_packages

setup(
    name="carreras",
    version="0.1",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    install_requires=[
        "pygame",
        "windows-curses; platform_system == 'Windows'"
    ],
    entry_points={
        "console_scripts": [
            "carreras=carreras.main:main",
        ],
    },
)

