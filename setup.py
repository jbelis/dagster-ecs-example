from setuptools import find_packages, setup

setup(
    name="hwp",
    packages=find_packages(exclude=["hwp_test"]),
    install_requires=[
        "dagster",
        "dagster-aws",
        "pandas",
        "s3fs",
        "python-dotenv",
        "pyarrow",
        "envtpl"
#        "dagster-cloud"
    ],
    extras_require={"dev": ["dagster-webserver", "pytest"]},
)
