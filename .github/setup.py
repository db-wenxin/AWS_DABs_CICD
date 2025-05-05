from setuptools import setup, find_packages

setup(
    name="bundlesDevOpsDemo",
    version="0.0.1",
    packages=find_packages(where="../src"),
    package_dir={"": "../src"},
    install_requires=[
        "databricks-connect>=13.0",
        "pyspark>=3.3.0",
        "nutter>=0.1.34",
    ],
    python_requires=">=3.10",
) 