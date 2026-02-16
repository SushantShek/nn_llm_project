variable "aws_region" {
  description = "AWS region to deploy resources"
  type        = string
  default     = "eu-north-1"
}

variable "cluster_name" {
  description = "Name of the EKS cluster"
  type        = string
  default     = "person-finder-cluster"
}
variable "github_repo" {
  description = "The GitHub repository in the format 'username/repo'"
  type        = string
  default     = "sushant/nn_llm_project"
}
