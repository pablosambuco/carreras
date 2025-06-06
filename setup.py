import subprocess
import sys
from setuptools import setup, find_packages

install_requires = (["windows-curses; platform_system == 'Windows'"],)
extras_require = {"gui": ["pygame"]}

try:
    import pygame  # noqa: F401
except ImportError:
    print("Pygame no está instalado. Intentando instalar...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pygame"])
        print("Pygame instalado exitosamente.")
        install_requires.append("pygame")
    except subprocess.CalledProcessError as e:
        print(f"Error al instalar Pygame: {e}")
        print("La instalación continuará sin soporte para Pygame.")

setup(
    name="carreras",
    version="0.1",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    install_requires=install_requires,
    extras_require=extras_require,
    entry_points={
        "console_scripts": [
            "carreras=carreras.main:main",
        ],
    },
)
