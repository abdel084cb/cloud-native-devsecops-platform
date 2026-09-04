resource "aws_ecr_repository" "repo" {
  name                 = "image_repository"
  image_tag_mutability = "IMMUTABLE"

  image_scanning_configuration {
    scan_on_push = true
  }

  tags = {
    Name = "ecr"
  }
}