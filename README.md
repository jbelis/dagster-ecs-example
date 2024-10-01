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
pip install -e hwp
```

### Running locally using the Dagster UI web server:

Create a .env file in the base directory containing the following environment variables
```bash
AWS_ACCESS_KEY_ID=<your AWS access key>
AWS_SECRET_ACCESS_KEY=<your AWS access key secret>
AWS_SESSION_TOKEN=<your AWS session token>
AWS_BUCKET=<your AWS bucket>
```
One of AWS_SESSION_TOKEN or { AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY } must be provided

```bash
pip install dagster-webserver
dagster dev
```

### Running locally using a python main

```bash
set -a            
source .env
set +a
export DAGSTER_HOME=`pwd`
python main.py
```

### Running locally using docker

```bash
docker build . -t codekarma/dagster-ecs-example
docker run --env-file .env codekarma/dagster-ecs-example:latest
```

### Unit testing

Tests are in the `test` directory and you can run tests using `pytest`:

```bash
pytest hwp_test
```

## Packaging and Deployment

```bash
docker build . -t codekarma/dagster-ecs-example
docker tag codekarma/dagster-ecs-example <your-ecr-registry>
aws ecr get-login-password --region <your-aws-region> | docker login --username AWS --password-stdin <your-ecr-registry>
docker push <your-ecr-registry>:latest
```

