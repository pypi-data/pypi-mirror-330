from setuptools import setup, find_packages

setup(
    name="lifter_hub",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "psycopg2-binary",  # PostgreSQL driver
    ],
    python_requires=">=3.11",
)
