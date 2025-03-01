from setuptools import setup, find_packages

setup(
    name="fastapi_db_mixins",
    version="1.0.1",
    packages=find_packages(),
    install_requires=[
        "sqlalchemy",
    ],
    description="FastAPI database mixins"
)