terraform {
  required_version = ">=1.5.7"
  required_providers {
    aws = {
      source = "hashicorp/aws"
    }
  }
}

provider "aws" {
  region = "eu-central-1"
}
