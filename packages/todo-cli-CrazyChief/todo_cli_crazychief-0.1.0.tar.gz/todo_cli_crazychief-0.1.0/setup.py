from setuptools import setup, find_packages

setup(
    name="todo-cli",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "pydantic",
        "click",
        "python-dotenv"
    ],
    entry_points={
        "console_scripts": [
            "todo=todo_cli.cli:cli"
        ]
    },
    author="Dmytro Danylov (danilovdmitry94@gmail.com)",
    description="A command-line TODO list application",
    python_requires=">=3.6"
)