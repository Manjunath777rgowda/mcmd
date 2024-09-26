from setuptools import setup, find_packages
from install_scripts import CustomInstallCommand

setup(
    name="mcmd",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "typer","setuptools"
    ],
    entry_points={
        "console_scripts": [
            "mcmd=app.cli:app",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    cmdclass={
        'install': CustomInstallCommand,
    }
)
