resource "aws_s3_bucket" "tfer--ecstest924" {
  bucket        = "dagster-ecs-example"
  force_destroy = "false"

  grant {
    id          = "2857de0512a8973c79c0a9d2f7e6187e950d057b2bbc0dec19e2e07f2ff44271"
    permissions = ["FULL_CONTROL"]
    type        = "CanonicalUser"
  }

  object_lock_enabled = "false"
  request_payer       = "BucketOwner"

  server_side_encryption_configuration {
    rule {
      apply_server_side_encryption_by_default {
        sse_algorithm = "AES256"
      }

      bucket_key_enabled = "true"
    }
  }

  versioning {
    enabled    = "false"
    mfa_delete = "false"
  }
}

# ECR
resource "aws_ecr_repository" "tfer--codekarma-002F-ecstest924" {
  encryption_configuration {
    encryption_type = "AES256"
  }

  image_scanning_configuration {
    scan_on_push = "false"
  }

  image_tag_mutability = "MUTABLE"
  name                 = "codekarma/ecstest924"
}

# VPC
resource "aws_vpc" "tfer--vpc-05b4cbf0aa18ab847" {
  assign_generated_ipv6_cidr_block     = "false"
  cidr_block                           = "172.31.0.0/16"
  enable_dns_hostnames                 = "true"
  enable_dns_support                   = "true"
  enable_network_address_usage_metrics = "false"
  instance_tenancy                     = "default"
  ipv6_netmask_length                  = "0"
}

# subnets
resource "aws_subnet" "tfer--subnet-085768f31593af0db" {
  assign_ipv6_address_on_creation                = "false"
  cidr_block                                     = "172.31.0.0/20"
  enable_dns64                                   = "false"
  enable_lni_at_device_index                     = "0"
  enable_resource_name_dns_a_record_on_launch    = "false"
  enable_resource_name_dns_aaaa_record_on_launch = "false"
  ipv6_native                                    = "false"
  map_customer_owned_ip_on_launch                = "false"
  map_public_ip_on_launch                        = "true"
  private_dns_hostname_type_on_launch            = "ip-name"
  vpc_id                                         = "${data.terraform_remote_state.vpc.outputs.aws_vpc_tfer--vpc-05b4cbf0aa18ab847_id}"
}

resource "aws_subnet" "tfer--subnet-0a55affe4cff5d696" {
  assign_ipv6_address_on_creation                = "false"
  cidr_block                                     = "172.31.32.0/20"
  enable_dns64                                   = "false"
  enable_lni_at_device_index                     = "0"
  enable_resource_name_dns_a_record_on_launch    = "false"
  enable_resource_name_dns_aaaa_record_on_launch = "false"
  ipv6_native                                    = "false"
  map_customer_owned_ip_on_launch                = "false"
  map_public_ip_on_launch                        = "true"
  private_dns_hostname_type_on_launch            = "ip-name"
  vpc_id                                         = "${data.terraform_remote_state.vpc.outputs.aws_vpc_tfer--vpc-05b4cbf0aa18ab847_id}"
}

resource "aws_subnet" "tfer--subnet-0f025dea8d2cedb53" {
  assign_ipv6_address_on_creation                = "false"
  cidr_block                                     = "172.31.16.0/20"
  enable_dns64                                   = "false"
  enable_lni_at_device_index                     = "0"
  enable_resource_name_dns_a_record_on_launch    = "false"
  enable_resource_name_dns_aaaa_record_on_launch = "false"
  ipv6_native                                    = "false"
  map_customer_owned_ip_on_launch                = "false"
  map_public_ip_on_launch                        = "true"
  private_dns_hostname_type_on_launch            = "ip-name"
  vpc_id                                         = "${data.terraform_remote_state.vpc.outputs.aws_vpc_tfer--vpc-05b4cbf0aa18ab847_id}"
}

# ECS
resource "aws_iam_role" "tfer--ecsTaskExecutionRole" {
  assume_role_policy = <<POLICY
{
  "Statement": [
    {
      "Action": "sts:AssumeRole",
      "Effect": "Allow",
      "Principal": {
        "Service": "ecs-tasks.amazonaws.com"
      },
      "Sid": "Statement1"
    }
  ],
  "Version": "2012-10-17"
}
POLICY

  description          = "allows a task definition to execute tasks"
  managed_policy_arns  = ["arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy"]
  max_session_duration = "3600"
  name                 = "ecsTaskExecutionRole"
  path                 = "/"
}

resource "aws_ecs_cluster" "tfer--codekarma-cluster" {
  name = "codekarma-cluster"

  setting {
    name  = "containerInsights"
    value = "disabled"
  }
}

resource "aws_ecs_task_definition" "tfer--task-definition-002F-ecstest924" {
  container_definitions    = "[{\"environment\":[{\"name\":\"AWS_ACCESS_KEY_ID\",\"value\":\"AKIA5NQ3RPFZMFO7VIHG\"},{\"name\":\"AWS_BUCKET\",\"value\":\"ecstest924\"},{\"name\":\"AWS_SECRET_ACCESS_KEY\",\"value\":\"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\"}],\"environmentFiles\":[],\"essential\":true,\"image\":\"922401995122.dkr.ecr.eu-central-1.amazonaws.com/codekarma/ecstest924:latest\",\"logConfiguration\":{\"logDriver\":\"awslogs\",\"options\":{\"awslogs-stream-prefix\":\"ecs\",\"awslogs-group\":\"/ecs/ecstest924\",\"mode\":\"non-blocking\",\"awslogs-create-group\":\"true\",\"max-buffer-size\":\"25m\",\"awslogs-region\":\"eu-central-1\"},\"secretOptions\":[]},\"mountPoints\":[],\"name\":\"ecstest924\",\"portMappings\":[],\"systemControls\":[],\"volumesFrom\":[]}]"
  cpu                      = "256"
  execution_role_arn       = "arn:aws:iam::922401995122:role/ecsTaskExecutionRole"
  family                   = "ecstest924"
  memory                   = "512"
  network_mode             = "awsvpc"
  requires_compatibilities = ["FARGATE"]
  track_latest             = "false"
}

