terraform {
  required_version = ">= 1.5.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

# Main provider — everything in the project lives here
provider "aws" {
  region = var.aws_region   # set this to ap-south-1 in terraform.tfvars
}

# CloudWatch billing metrics (AWS/Billing) are only published in us-east-1,
# regardless of where the rest of the project's resources live.
# This alias exists ONLY for the billing alarm in budget.tf.
provider "aws" {
  alias  = "billing"
  region = "us-east-1"
}