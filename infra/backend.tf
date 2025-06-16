terraform {
  backend "s3" {
    bucket         = "epam-devops-tfstate"
    key            = "terraform/dev/terraform.tfstate"
    region         = "us-east-1"
    dynamodb_table = "terraform-locks"
    encrypt        = true
  }
}
