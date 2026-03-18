"""Gunicorn configuration file with deprecated gunicorn_paste() method"""
import multiprocessing
import os


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

# Server mechanics
daemon = False
pidfile = None
umask = 0
user = None
group = None
tmp_upload_dir = None

# Process naming
proc_name = "flask_app"


# TODO: Removed deprecated gunicorn_paste() method (removed in gunicorn 23.0.0+)
# If PasteDeploy integration is required, migrate to alternative configuration approach.
# Previously used settings: app='app:app', workers=workers, bind=bind, timeout=timeout
