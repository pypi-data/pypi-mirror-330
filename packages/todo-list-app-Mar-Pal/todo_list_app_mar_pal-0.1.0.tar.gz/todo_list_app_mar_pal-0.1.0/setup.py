import os
from setuptools import setup, find_packages


parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

with open(os.path.join(parent_dir, "README.md"), encoding="utf-8") as f:
    long_description = f.read()


setup(
    name="todo_list_app_Mar_Pal",  # Replace with your package name
    version="0.1.0",  # Update the version as needed
    author="Marko Palinec",
    author_email="marko.palin@gmail.com",
    description="A todo list app",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mp9466/todo-list-app",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",  # Choose the appropriate license
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
        "fastapi",
        "uvicorn",
        "sqlalchemy",
        "pydantic",
        "pydantic-settings",
        "psycopg2-binary",
        "alembic",
        "python-dotenv",
        "pytest",
        "httpx",
        "pytest-asyncio"
    ],
    entry_points={
        "console_scripts": [
            "start-todo-app = main:app"
        ]
    },
)
