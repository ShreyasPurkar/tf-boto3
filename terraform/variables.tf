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

variable "s3_transition_days" {
  type        = number
  description = "Number of days after which to transition objects to STANDARD_IA storage class"
  default     = 30
}

variable "s3_transition_storage_class" {
  type        = string
  description = "Storage class to transition objects to"
  default     = "STANDARD_IA"
}