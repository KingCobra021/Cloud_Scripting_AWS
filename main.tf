provider "aws" {
  region = "us-east-1" # Change this to your preferred region
}

resource "aws_instance" "example" {
  ami           = "ami-0dd09ed8692591dd8" # Replace with your AMI ID
  instance_type = "t2.micro"
  key_name      = aws_key_pair.yourkey.key_name

  # Configure Nginx with user_data script
  user_data = <<-EOF
              #!/bin/bash
              sudo apt update -y
              sudo apt install -y nginx
              echo '
              server {
                  listen 8080;
                  server_name localhost;

                  root /var/www/html;
                  index index.html index.htm;

                  location / {
                      try_files \$uri \$uri/ =404;
                  }
              }
              ' | sudo tee /etc/nginx/sites-available/default
              sudo ln -sf /etc/nginx/sites-available/default /etc/nginx/sites-enabled/default
              sudo nginx -t
              sudo systemctl restart nginx
            EOF

  # Associate the instance with the security group
  security_groups = [aws_security_group.allow_ports.name]

  tags = {
    Name = "NginxOn8080"
  }
}

resource "aws_key_pair" "yourkey" {
  key_name   = "yourkey"
  public_key = file("yourkey.pub")
}

# Security Group to Allow Ports 22, 8080, and 8000
resource "aws_security_group" "allow_ports" {
  name        = "allow_ports"
  description = "Allow SSH, HTTP on 8080, and Custom on 8000"

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"] # Allow SSH from anywhere (replace with specific IP for security)
  }

  ingress {
    from_port   = 8080
    to_port     = 8080
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"] # Open HTTP on 8080 to the world
  }

  ingress {
    from_port   = 8000
    to_port     = 8000
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"] # Open Custom port 8000
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"] # Allow all outbound traffic
  }
}

