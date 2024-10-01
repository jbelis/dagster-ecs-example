FROM public.ecr.aws/docker/library/python:3.12-slim

# Set the working directory inside the container
WORKDIR /app

# set environment
ENV DAGSTER_HOME=/app

# Copy the requirements.txt file into the container
COPY requirements.txt .

# Install Python dependencies from requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code into the container
COPY dagster.yaml.tpl .
COPY pyproject.toml .
COPY setup.cfg .
COPY setup.py .
COPY main.py .
ADD hwp hwp
ADD docker/start.sh .

# run the data pipeline
CMD ["bash", "start.sh"]