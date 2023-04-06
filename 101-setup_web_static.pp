# Install Nginx
package { 'nginx':
  ensure => installed,
}

# Create directories
file { ['/data', '/data/web_static', '/data/web_static/releases', '/data/web_static/shared', '/data/web_static/releases/test']:
  ensure => 'directory',
}

# Create fake HTML file
file { '/data/web_static/releases/test/index.html':
  content => '<html><head><title>Test HTML Page</title></head><body><p>This is a test page.</p></body></html>',
}

# Create symbolic link
file { '/data/web_static/current':
  ensure => 'link',
  target => '/data/web_static/releases/test',
  force  => true,
}

# Set ownership
file { '/data':
  owner => 'ubuntu',
  group => 'ubuntu',
  recurse => true,
}

# Update Nginx configuration
file { '/etc/nginx/sites-available/default':
  content => "
    server {
        listen 80;
        listen [::]:80;

        location /hbnb_static/ {
            alias /data/web_static/current/;
            index index.html;
        }
    }
  ",
  notify => Service['nginx'],
}

# Restart Nginx service
service { 'nginx':
  ensure => running,
  enable => true,
  require => File['/etc/nginx/sites-available/default'],
}
