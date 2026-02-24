#!/usr/bin/env python3
"""
Gunicorn configuration file using deprecated gunicorn_paste() method
This method is available in gunicorn 21.2.0 but deprecated in 23.0.0
"""

import os
from gunicorn.app.base import BaseApplication
from gunicorn.config import Config
from gunicorn.workers.sync import SyncWorker

# Server socket
bind = "0.0.0.0:5000"
backlog = 2048

# Worker processes
workers = 4
worker_class = "sync"
worker_connections = 1000
timeout = 30
keepalive = 2

# Restart workers after this many requests, to help prevent memory leaks
max_requests = 1000
max_requests_jitter = 100

# Logging
loglevel = "info"
accesslog = "-"
errorlog = "-"

# Process naming
proc_name = 'vulnerable_flask_service'

# Server mechanics
daemon = False
pidfile = '/var/run/gunicorn.pid'
tmp_upload_dir = None

def gunicorn_paste():
    """
    Deprecated method available in gunicorn 21.2.0
    This method was used for Paste Deploy integration
    Deprecated in gunicorn 23.0.0
    """
    paste_config = {
        'use': 'egg:gunicorn#main',
        'host': '0.0.0.0',
        'port': '5000',
        'workers': str(workers),
        'timeout': str(timeout),
    }
    
    # Legacy paste configuration handling
    # This demonstrates usage of the deprecated method
    print(f"[DEPRECATED] Using gunicorn_paste() method: {paste_config}")
    return paste_config

def when_ready(server):
    """Called just after the server is started."""
    server.log.info("Server is ready. Spawning workers")
    # Use the deprecated method
    paste_config = gunicorn_paste()
    server.log.info(f"Paste config loaded: {paste_config}")

def worker_int(worker):
    """Called just after a worker has been killed (SIGINT/SIGTERM)."""
    worker.log.info("worker received INT or QUIT signal")

def pre_fork(server, worker):
    """Called just before a worker is forked."""
    server.log.info("Worker about to be forked")

def post_fork(server, worker):
    """Called just after a worker has been forked."""
    server.log.info("Worker spawned (pid: %s)", worker.pid)

def post_worker_init(worker):
    """Called just after a worker has initialized the application."""
    worker.log.info("Worker initialized")