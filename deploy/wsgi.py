"""Web Server Gateway Interface

https://www.youtube.com/watch?v=KWIIPKbdxD0

for use with gunicorn
"""
from my_package import app

if __name__ == "__main__":
    app.run()

# to run:
# $ gunicorn --bind 0.0.0.0:5000 wsgi:app

# service file:

# [Unit]
# Description=Gunicorn instance to serve Flask app
# After=network.target
# 
# [Service]
# User=tony
# Group=www-data
# WorkingDirectory=/home/tony/hike
# Environment="PATH=/home/tony/env/teton/bin"
# ExecStart=/home/tony/env/teton/bin/gunicorn --workers 3 --bind unix:peak.sock -m 007 wsgi:app
# 
# [Install]
# WantedBy=multi-user.target


# sudo systemctl daemon-reload
# sudo systemctl start peak
# sudo systemctl enable peak
# sudo systemctl status peak

