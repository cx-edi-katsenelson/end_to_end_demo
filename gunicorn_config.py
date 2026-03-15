"""Gunicorn configuration file"""
import multiprocessing

# Server socket
bind = "0.0.0.0:5000"
backlog = 2048

# Worker processes
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "sync"
worker_connections = 1000
timeout = 30
keepalive = 2

# Logging
accesslog = "-"
errorlog = "-"
loglevel = "info"

# Process naming
proc_name = "data-processor"

# Server mechanics
daemon = False
pidfile = None
umask = 0
user = None
group = None
tmp_upload_dir = None


# TODO: Paste Deploy integration was removed in gunicorn 23.0.0
# If Paste Deploy configuration is required, consider alternative approaches:
# - Use a WSGI middleware wrapper
# - Migrate to a different configuration management solution
# - Use gunicorn's native configuration options (as shown above)
