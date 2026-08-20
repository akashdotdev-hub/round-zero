resource "aws_dynamodb_table" "round_zero_matches" {
  name         = "round-zero-matches"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "PK"
  range_key    = "SK"

  attribute {
    name = "PK"
    type = "S"
  }

  attribute {
    name = "SK"
    type = "S"
  }

  point_in_time_recovery {
    enabled = true
  }

  server_side_encryption {
    enabled = true
  }

  tags = {
    Project     = "Round Zero"
    Environment = "dev"
    Purpose     = "Processed Valorant match data"
  }
}