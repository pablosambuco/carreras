from setuptools import setup, find_packages

setup(
    name="carreras",
    version="0.1",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "pygame",
        "windows-curses; platform_system=='Windows'",
    ],
    entry_points={
        "console_scripts": [
            "carreras = main:main",
        ],
    },
    python_requires=">=3.10",
    description="Horse Racing Game (terminal and pygame)",
    author="Pablo",
    license="MIT",
)

