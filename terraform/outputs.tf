output "sns_topic_arn" {
  description = "ARN of the SNS topic billing/budget alerts publish to."
  value       = aws_sns_topic.billing_alerts.arn
}

output "budget_name" {
  description = "Name of the AWS Budgets budget created."
  value       = aws_budgets_budget.monthly.name
}

output "billing_alarm_name" {
  description = "Name of the CloudWatch billing alarm created."
  value       = aws_cloudwatch_metric_alarm.billing_alarm.alarm_name
}
