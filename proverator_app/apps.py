from django.apps import AppConfig

class ProveratorAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'proverator_app'

    def ready(self):
        from django.db.models.signals import post_migrate

        """
        Cнимает регистрацию моделей SolarSchedule и ClockedSchedule 
        из админки django_celery_beat

        Регистрирует обработчик post_migrate, создающий
        периодические задачи Celery Beat в БД при инициализации приложения.

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

        from .signals import tasks_check_domains,tasks_clear_domains
        
        # Регистрация обработчиков задач
        # чтобы задачи создавались автоматически после применения миграций
        post_migrate.connect(tasks_check_domains, sender=self)
        post_migrate.connect(tasks_clear_domains, sender=self)

        # чтобы задачи были зарегистрированы даже без запуска миграций
        # tasks_check_domains()
        # tasks_clear_domains()
