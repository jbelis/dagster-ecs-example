#!/bin/bash

# generate dagster config from template + environment
envtpl dagster.yaml.tpl

# run the pipeline
python main.py