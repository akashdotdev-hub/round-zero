# --- Milestone 1: Cost guardrails ---
# This is deliberately the first resource deployed in the whole project.
# Nothing billable gets created until this is live and confirmed working.

# SNS topic (main region) that budget/other alerts can publish to.
resource "aws_sns_topic" "billing_alerts" {
  name = "${var.project_name}-billing-alerts"
}

resource "aws_sns_topic_subscription" "billing_email" {
  topic_arn = aws_sns_topic.billing_alerts.arn
  protocol  = "email"
  endpoint  = var.alert_email
}

# --- AWS Budgets: threshold-based alert at % of a monthly $ budget ---
# AWS Budgets is a global service - not tied to any provider region.
resource "aws_budgets_budget" "monthly" {
  name         = "${var.project_name}-monthly-budget"
  budget_type  = "COST"
  limit_amount = tostring(var.monthly_budget_usd)
  limit_unit   = "USD"
  time_unit    = "MONTHLY"

  notification {
    comparison_operator        = "GREATER_THAN"
    threshold                  = 50
    threshold_type             = "PERCENTAGE"
    notification_type          = "ACTUAL"
    subscriber_email_addresses = [var.alert_email]
  }

  notification {
    comparison_operator        = "GREATER_THAN"
    threshold                  = 90
    threshold_type             = "PERCENTAGE"
    notification_type          = "ACTUAL"
    subscriber_email_addresses = [var.alert_email]
  }
}

# --- Dedicated us-east-1 SNS topic, used ONLY by the billing alarm below. ---
# AWS requires a CloudWatch billing alarm's SNS target to also live in
# us-east-1 - cross-region alarm_actions are rejected outright.
resource "aws_sns_topic" "billing_alerts_useast1" {
  provider = aws.billing
  name     = "${var.project_name}-billing-alerts-useast1"
}

resource "aws_sns_topic_subscription" "billing_email_useast1" {
  provider  = aws.billing
  topic_arn = aws_sns_topic.billing_alerts_useast1.arn
  protocol  = "email"
  endpoint  = var.alert_email
}

# --- Raw CloudWatch billing alarm: fires at an absolute $ threshold ---
# Requires "Receive CloudWatch Billing Alerts" enabled in Billing Preferences
# (manual console step - Terraform cannot enable this).
# Must live in us-east-1 - both the alarm itself AND its SNS target.
resource "aws_cloudwatch_metric_alarm" "billing_alarm" {
  provider            = aws.billing
  alarm_name          = "${var.project_name}-billing-alarm"
  comparison_operator = "GreaterThanThreshold"
  evaluation_periods  = 1
  metric_name         = "EstimatedCharges"
  namespace           = "AWS/Billing"
  period              = 21600 # 6 hours - billing metrics update infrequently
  statistic           = "Maximum"
  threshold           = var.billing_alarm_threshold_usd
  alarm_description   = "Fires when estimated AWS charges exceed ${var.billing_alarm_threshold_usd} USD"
  alarm_actions       = [aws_sns_topic.billing_alerts_useast1.arn]

  dimensions = {
    Currency = "USD"
  }
}
