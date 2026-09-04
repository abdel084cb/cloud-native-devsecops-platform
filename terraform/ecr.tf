resource "aws_ecr_repository" "api" {
  name                 = "devsecops-api"
  image_tag_mutability = "IMMUTABLE"

  image_scanning_configuration {
    scan_on_push = true
  }

  tags = {
    Project   = "cloud-native-devsecops-platform"
    ManagedBy = "Terraform"
  }
}
