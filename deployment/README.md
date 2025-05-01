# Deployment Instructions

This directory contains files needed for deploying the HR AI Workflow application to a production server.

## Prerequisites

1. A server running Ubuntu (or similar Linux distribution)
2. Nginx installed
3. Python 3.9+ installed
4. Node.js 18+ installed
5. MySQL installed and configured

## Manual Deployment Steps

### Backend Setup

1. Copy the `hr-ai-backend.service` file to `/etc/systemd/system/`
2. Edit the file to update paths and environment variables as needed
3. Enable and start the service:
   ```
   sudo systemctl enable hr-ai-backend.service
   sudo systemctl start hr-ai-backend.service
   ```

### Frontend Setup

1. Create a directory for the frontend files:
   ```
   sudo mkdir -p /var/www/hr-ai-workflow
   ```
2. Copy the `nginx-config` file to `/etc/nginx/sites-available/hr-ai-workflow`
3. Create a symbolic link to enable the site:
   ```
   sudo ln -s /etc/nginx/sites-available/hr-ai-workflow /etc/nginx/sites-enabled/
   ```
4. Test the Nginx configuration:
   ```
   sudo nginx -t
   ```
5. Restart Nginx:
   ```
   sudo systemctl restart nginx
   ```

## Automatic Deployment with GitHub Actions

The project is set up to automatically deploy to the production server when changes are pushed to the main branch. The deployment process is defined in the `.github/workflows/deploy.yml` file.

### Required GitHub Secrets

The following secrets need to be set in the GitHub repository settings:

- `SERVER_HOST`: The hostname or IP address of your server
- `SERVER_USERNAME`: The SSH username
- `SERVER_SSH_KEY`: The private SSH key for authentication
- `SERVER_PORT`: The SSH port (usually 22)
- `OPENAI_API_KEY`: Your OpenAI API key
- `DB_HOST`: Database hostname
- `DB_USER`: Database username
- `DB_PASSWORD`: Database password
- `DB_NAME`: Database name

## Database Setup

1. Create a MySQL database:
   ```sql
   CREATE DATABASE hr_ai;
   ```

2. Create the necessary tables:
   ```sql
   USE hr_ai;
   
   CREATE TABLE candidates (
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
   );
   ```

## Troubleshooting

- Check the service logs:
  ```
  sudo journalctl -u hr-ai-backend.service
  ```
- Check Nginx logs:
  ```
  sudo tail -f /var/log/nginx/error.log
  ```
