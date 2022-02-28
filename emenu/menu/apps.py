from django.apps import AppConfig
import os


class MenuConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'menu'

    def ready(self):
        if os.environ.get('RUN_MAIN', None) != 'true':
            from . import jobs
            jobs.start_scheduler()
