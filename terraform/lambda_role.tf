# IAM policy document for Lambda function to assume the role
data "aws_iam_policy_document" "assume_role" {
  statement {
    effect = "Allow"
    principals {
      type        = "Service"
      identifiers = ["lambda.amazonaws.com"]
    }
    actions = ["sts:AssumeRole"]
  }
}

# IAM role for Lambda function
resource "aws_iam_role" "iam_role_for_lambda" {
  name               = "iam_for_lambda"
  assume_role_policy = data.aws_iam_policy_document.assume_role.json
}

# IAM policy for Lambda function to access S3 and CloudWatch logs
resource "aws_iam_role_policy" "lambda_all_permissions" {
  name = "lambda-merged-policy"
  role = aws_iam_role.iam_role_for_lambda.id

  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Effect = "Allow",
        Action = [
          "logs:CreateLogGroup",
          "logs:CreateLogStream",
          "logs:PutLogEvents"
        ],
        Resource = "*"
      },
      {
        Effect = "Allow",
        Action = [
          "s3:GetObject",
          "s3:PutObject"
        ],
        Resource = "arn:aws:s3:::29651de9-6eb1-adac-5179-392ba397f0ed/*"
      }
    ]
  })
}

# Output the IAM role ARN
output "lambda_role_arn" {
  value = aws_iam_role.iam_role_for_lambda.arn
}