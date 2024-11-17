provider "aws" {
  region = "us-east-1" # Change this to your desired region
}

resource "aws_instance" "example" {
  ami           = "ami-0dd09ed8692591dd8" # Replace with your AMI ID
  instance_type = "t2.micro"              # Free tier eligible
  key_name      = aws_key_pair.client.key_name

  # Use user_data to install and configure Nginx
  user_data = <<-EOF
              #!/bin/bash
              sudo yum update -y
              sudo yum install -y nginx
              sudo sed -i 's/listen       80;/listen       8080;/g' /etc/nginx/nginx.conf
              sudo systemctl enable nginx
              sudo systemctl start nginx
            EOF

  tags = {
    Name = "TerraformExampleInstance"
  }

  # Associate the instance with the security group
  security_groups = [aws_security_group.nginx_access.name]
}

resource "aws_key_pair" "yourkey" {
  key_name   = "yourkey"
  public_key = file("yourkey.pub")
}

# Define a security group to allow access to port 8080
resource "aws_security_group" "nginx_access" {
  name        = "nginx_access"
  description = "Allow HTTP access on port 8080"

  ingress {
    from_port   = 8080
    to_port     = 8080
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"] # Open to all; restrict as needed
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1" # Allow all outbound traffic
    cidr_blocks = ["0.0.0.0/0"]
  }
}

