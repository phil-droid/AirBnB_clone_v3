#!/usr/bin/env bash

# Install Nginx if not already installed
if ! dpkg -s nginx > /dev/null 2>&1; then
    sudo apt-get update
    sudo apt-get -y install nginx
fi

# Create directories if not already exist
sudo mkdir -p /data/web_static/{releases,test,shared}

# Create fake HTML file
echo "Hello World!" | sudo tee /data/web_static/releases/test/index.html

# Create symbolic link
sudo ln -sf /data/web_static/releases/test /data/web_static/current

# Give ownership of /data folder to ubuntu user and group
sudo chown -R ubuntu:ubuntu /data

# Update Nginx configuration
sudo sed -i '/^\s*server_name\s*/a \\n\tlocation /hbnb_static {\n\t\talias /data/web_static/current/;\n\t}\n' /etc/nginx/sites-available/default

# Restart Nginx
sudo service nginx restart
