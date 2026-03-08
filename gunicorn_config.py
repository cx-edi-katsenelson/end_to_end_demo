import os
import multiprocessing
# REMOVED: from gunicorn.app.pasterapp import paste_server
# Paste Deploy integration was removed in gunicorn 23.0.0
# See: https://docs.gunicorn.org/en/latest/news.html

# Server socket
bind = "0.0.0.0:5000"
backlog = 2048

# Worker processes
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = 'sync'
worker_connections = 1000
timeout = 30
keepalive = 2

# Logging
accesslog = '-'
errorlog = '-'
loglevel = 'info'
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'

# Process naming
proc_name = 'gunicorn_flask_app'

# Server mechanics
daemon = False
pidfile = None
umask = 0
user = None
group = None
tmp_upload_dir = None

# SSL (for future use)
keyfile = None
certfile = None

def gunicorn_paste():
    """
    Legacy paste integration method available in gunicorn 21.2.0
    This method is deprecated in gunicorn 23.0.0
    
    This function demonstrates the usage of paste server loading
    which was commonly used for WSGI app configuration
    """
    config_file = os.environ.get('PASTE_CONFIG', 'paste.ini')
    
    # This would load a WSGI application from a Paste Deploy configuration file
    # Example usage: paste_server(None, None, config_file, 'main')
    # 
    # Note: This is a demonstration of the deprecated functionality
    # In production with gunicorn 21.2.0, you would use:
    # gunicorn --paste config.ini -c gunicorn_config.py
    
    print(f"[DEPRECATED] gunicorn_paste() method - loading from {config_file}")
    print("This functionality is deprecated in gunicorn 23.0.0+")
    
    return config_file

# REMOVED: Configuration hook for paste integration
# paste_config = gunicorn_paste()
# 
# TODO: Migrate from Paste Deploy to native WSGI configuration
# Gunicorn 23.0.0 removed PasteScript/Paste Deploy support.
# If using Paste Deploy, migrate to:
# 1. Native WSGI application factory in the Flask app
# 2. Use gunicorn app:app syntax instead of --paste
# 3. Or use alternative configuration management (e.g., environment variables)
