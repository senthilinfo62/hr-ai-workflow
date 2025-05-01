#!/bin/bash

# Exit on error
set -e

# Update system
echo "Updating system packages..."
sudo apt-get update
sudo apt-get upgrade -y

# Install required packages
echo "Installing required packages..."
sudo apt-get install -y python3 python3-pip python3-venv nginx mysql-server

# Install Node.js
echo "Installing Node.js..."
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt-get install -y nodejs

# Set up MySQL
echo "Setting up MySQL..."
sudo mysql_secure_installation

# Create database and user
echo "Creating database and user..."
sudo mysql -e "CREATE DATABASE IF NOT EXISTS hr_ai;"
sudo mysql -e "CREATE USER IF NOT EXISTS 'hr_ai_user'@'localhost' IDENTIFIED BY 'password';"
sudo mysql -e "GRANT ALL PRIVILEGES ON hr_ai.* TO 'hr_ai_user'@'localhost';"
sudo mysql -e "FLUSH PRIVILEGES;"

# Create database tables
echo "Creating database tables..."
sudo mysql hr_ai -e "
CREATE TABLE IF NOT EXISTS candidates (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(100) NOT NULL,
  email VARCHAR(100) NOT NULL,
  phone VARCHAR(20),
  city VARCHAR(100),
  birthdate VARCHAR(20),
  education TEXT,
  job_history TEXT,
  skills JSON,
  score INT
);"

# Set up application directory
echo "Setting up application directory..."
mkdir -p ~/hr-ai-workflow
mkdir -p /var/www/hr-ai-workflow
sudo chown -R $USER:$USER /var/www/hr-ai-workflow

# Copy systemd service file
echo "Setting up systemd service..."
sudo cp hr-ai-backend.service /etc/systemd/system/
sudo systemctl daemon-reload

# Set up Nginx
echo "Setting up Nginx..."
sudo cp nginx-config /etc/nginx/sites-available/hr-ai-workflow
sudo ln -s /etc/nginx/sites-available/hr-ai-workflow /etc/nginx/sites-enabled/ 2>/dev/null || true
sudo nginx -t
sudo systemctl restart nginx

echo "Server setup complete!"
echo "Please update the hr-ai-backend.service file with your actual environment variables."
echo "Then enable and start the service with: sudo systemctl enable hr-ai-backend.service && sudo systemctl start hr-ai-backend.service"
