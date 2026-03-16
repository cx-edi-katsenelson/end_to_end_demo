import os

# Server socket
bind = "0.0.0.0:5000"

# Worker processes
workers = 2
worker_class = "sync"
threads = 2

# Logging
accesslog = "-"
errorlog = "-"
loglevel = "info"

# Timeout
timeout = 120

# Process naming
proc_name = "flask_rest_api"

# NOTE: Paste Deploy integration (gunicorn.app.pasterapp) was removed in gunicorn 23.0.0
# Previous deprecated code using paste_server has been removed for compatibility
