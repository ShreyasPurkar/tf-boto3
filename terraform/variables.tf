# Variables for resources
variable "region" {
  type        = string
  description = "AWS region"
  default     = "us-east-2"
}

variable "profile" {
  type        = string
  description = "AWS profile"
}