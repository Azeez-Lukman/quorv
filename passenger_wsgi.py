import os
import sys

# Add the project root directory to the Python path
sys.path.insert(0, os.path.dirname(__file__))

# Set Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# Import and instantiate WSGI application
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

# Safe auto-migrate on startup to ensure new database tables exist without manual terminal commands
try:
    from django.core.management import call_command
    call_command('migrate', interactive=False)
except Exception:
    pass

