from django.apps import AppConfig


class ProveratorAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'proverator_app'

    def ready(self):
        """
        Cнимает регистрацию моделей SolarSchedule и ClockedSchedule 
        из админки django_celery_beat
        """

        from django.contrib import admin
        from django_celery_beat.models import (

            SolarSchedule,
            ClockedSchedule,
        )

        try:
            admin.site.unregister(SolarSchedule)
            admin.site.unregister(ClockedSchedule)

        except admin.sites.NotRegistered:
            pass
