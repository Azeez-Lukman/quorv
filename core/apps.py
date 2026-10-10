import sys
import logging
from django.apps import AppConfig

logger = logging.getLogger(__name__)


class CoreConfig(AppConfig):
    name = 'core'

    def ready(self):
        # Skip during build or static tasks
        if any(cmd in sys.argv for cmd in ['makemigrations', 'collectstatic', 'dumpdata', 'loaddata']):
            return

        import warnings
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")

            # 1. Self-healing DB check: Ensure image_url column exists in core_industry
            # Works on SQLite and catches schema mismatches before any view queries run.
            try:
                from django.db import connection
                with connection.cursor() as cursor:
                    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='core_industry';")
                    if cursor.fetchone():
                        cursor.execute("PRAGMA table_info(core_industry);")
                        cols = [row[1] for row in cursor.fetchall()]
                        if cols and 'image_url' not in cols:
                            cursor.execute("ALTER TABLE core_industry ADD COLUMN image_url varchar(500) DEFAULT '';")
            except Exception as e:
                logger.warning(f"Core schema heal notice: {e}")

            # 2. Automatically apply pending migrations to sync Django migration state
            try:
                from django.core.management import call_command
                call_command('migrate', interactive=False)
            except Exception as e:
                err = str(e).lower()
                if 'duplicate column' in err or 'already exists' in err:
                    try:
                        from django.core.management import call_command
                        call_command('migrate', 'core', fake=True)
                    except Exception:
                        pass
                else:
                    logger.warning(f"Core auto-migrate notice: {e}")


