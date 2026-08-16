variable "aws_region" {
  description = "AWS region for all resources. Must be us-east-1 for CloudWatch billing alarms to function."
  type        = string
  default     = "us-east-1"
}

variable "project_name" {
  description = "Short name used to prefix/tag all resources in this project."
  type        = string
  default     = "round-zero"
}

variable "alert_email" {
  description = "Email address that receives budget and billing alarm notifications."
  type        = string
}

variable "monthly_budget_usd" {
  description = "Monthly budget amount in USD. Alerts fire at percentages of this."
  type        = number
  default     = 20
}

variable "billing_alarm_threshold_usd" {
  description = "Absolute USD threshold for the raw CloudWatch billing alarm (separate from the AWS Budgets % alerts)."
  type        = number
  default     = 15
}
