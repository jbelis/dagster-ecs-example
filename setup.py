from setuptools import find_packages, setup

setup(
    name="example_pipeline",
    packages=find_packages(exclude=["example_pipeline_test"]),
    install_requires=[
        "dagster",
        "dagster-aws",
        "pandas",
        "s3fs",
        "pyarrow",
        "envtpl"
#        "dagster-cloud"
    ],
    extras_require={"dev": ["dagster-webserver", "pytest"]},
)
