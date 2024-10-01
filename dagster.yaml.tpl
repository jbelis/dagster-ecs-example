compute_logs:
  module: dagster_aws.s3.compute_log_manager
  class: S3ComputeLogManager
  config:
    bucket: "{{ AWS_BUCKET }}"
    prefix: "logs/"
    use_ssl: true
    verify: true
    skip_empty_files: true
