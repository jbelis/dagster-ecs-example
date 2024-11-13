# dagster-ecs-example

This project contains a simplistic data pipeline, implemented using dagster, to be executed as an AWS ECS standalone task. The data pipeline reads a CSV file from S3 and exports it back to the same bucket in parquet format.

## Local Development

python version: 3.12

```bash
python --version
python -m venv .venv
source ./.venv/bin/activate
pip install -r requirements.txt
```

Also, install your Dagster code location as a Python package. By using the --editable flag, pip will install your Python package in ["editable mode"](https://pip.pypa.io/en/latest/topics/local-project-installs/#editable-installs) so that as you develop, local code changes will automatically apply.

```bash
pip install -e .
```

### Environment variables

```bash
AWS_ACCESS_KEY_ID=<your AWS access key>
AWS_SECRET_ACCESS_KEY=<your AWS access key secret>
AWS_SESSION_TOKEN=<your AWS session token>
AWS_BUCKET=<your AWS bucket>
SOURCE_FILENAME=<path of input file within bucket>
```

Note: One of AWS_SESSION_TOKEN or { AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY } must be provided

Note: One way to manage environment variable is to create a .env file in the base directory containing the the above. You can then export the contents to the environments as follows:
```bash
set -a            
source .env
set +a
```

Any file ending with .env is ignored by git via .gitignore. Whatever your do, be careful to never
commit your AWS credentials to git!

### Running locally using the Dagster UI web server:

```bash
pip install dagster-webserver
dagster dev
```

### Running locally using a python main

```bash
export DAGSTER_HOME=`pwd`
python main.py
```

### Running locally using docker

```bash
docker build . -t codekarma/dagster-ecs-example
docker run --env-file .env codekarma/dagster-ecs-example:latest
```

### Inspecting the docker image

The following will give you a prompt inside the container instead of running the app.
```bash
docker run -ti --env-file .env codekarma/dagster-ecs-example:latest bash
```

### Unit testing

Tests are in the `test` directory and you can run tests using `pytest`:

```bash
pytest example_pipeline_test
```

## Packaging and Deployment on AWS ECR

```bash
docker build . -t codekarma/dagster-ecs-example
docker tag codekarma/dagster-ecs-example <your-ecr-registry>
aws ecr get-login-password --region <your-aws-region> | docker login --username AWS --password-stdin <your-ecr-registry>
docker push <your-ecr-registry>:latest
```

