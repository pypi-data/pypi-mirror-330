include {
  path = find_in_parent_folders()
}

terraform {
  source = "git::git@bitbucket.org:wiliot/wiliot-cloud-modules.git//common/databricks/clusters"
}

generate "data" {
  path      = "data.tf"
  if_exists = "overwrite_terragrunt"
  contents  = <<EOF
variable "dbc_mws_secret_arn" {
  type = string
}

data "aws_secretsmanager_secret" "app_secret" {
  arn = var.dbc_mws_secret_arn
}

data "aws_secretsmanager_secret_version" "app_secret" {
  secret_id = data.aws_secretsmanager_secret.app_secret.id
}

locals {
  app_secrets = jsondecode(
    data.aws_secretsmanager_secret_version.app_secret.secret_string
  )
  host  = local.app_secrets.host
  token = local.app_secrets.token
}

provider "databricks" {
  host  = local.host
  token = local.token
}
EOF
}

locals {
  # Automatically load common variables shared across all accounts
  common_vars = read_terragrunt_config(find_in_parent_folders("common.hcl"))

  # Extract the name prefix for easy access
  name_prefix = "${local.common_vars.locals.name_prefix}-${local.common_vars.locals.databricks_prefix}"

  # Automatically load account-level variables
  account_vars = read_terragrunt_config(find_in_parent_folders("account.hcl"))

  # Extract the account_name for easy access
  account_name = local.account_vars.locals.account_name

  # Automatically load region-level variables
  region_vars = read_terragrunt_config(find_in_parent_folders("region.hcl"))

  # Extract the region for easy access
  aws_region = local.region_vars.locals.aws_region

  # Automatically load Databricks variables
  databricks_vars = read_terragrunt_config(find_in_parent_folders("dbc.hcl"))
}

inputs = {
  dbc_mws_secret_arn = local.databricks_vars.locals.dbc_mws_secret_arn

  group_name = "team_network_system"
  clusters = {
    system-network = {
      spark_version = "13.3.x-scala2.12",
      spark_conf = {
        "spark.databricks.cluster.profile"          = "singleNode",
        "spark.executor.processTreeMetrics.enabled" = "true",
        "spark.master"                              = "local[*]",
        "spark.ui.prometheus.enabled"               = "true",
        "spark.sql.streaming.metricsEnabled"        = "true"
      },
      aws_attributes = {
        first_on_demand        = 1,
        availability           = "SPOT_WITH_FALLBACK",
        zone_id                = "auto",
        instance_profile_arn   = "${local.databricks_vars.locals.instance_profile_arn}",
        spot_bid_price_percent = 100,
        ebs_volume_type        = "GENERAL_PURPOSE_SSD",
        ebs_volume_count       = 1,
        ebs_volume_size        = 32
      },
      node_type_id            = "m6gd.xlarge"
      driver_node_type_id     = "m6gd.xlarge"
      autotermination_minutes = 60
      init_scripts = [
        {
          s3 = {
            destination = "s3://wiliot-dbc-us-east-2-${local.account_name}-monitoring-and-logs/monitoring/init-scripts/initialize-metrics.sh",
            region      = "us-east-2"
          }
        },
        {
          s3 = {
            destination = "s3://wiliot-dbc-us-east-2-${local.account_name}-monitoring-and-logs/clusters/init-scripts/system-network/install_packages.sh",
            region      = "us-east-2"
          }
        }
      ],
      policy_id          = "9A644F43BC0001C7"
      data_security_mode = "NONE",
      runtime_engine     = "STANDARD"
      num_workers        = 0,
      custom_tags = {
        ResourceClass = "SingleNode",
        aws_region    = local.aws_region
        environment   = local.account_name
      }
    }
  }
}
