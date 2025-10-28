from decouple import config

from django_celery_beat.models import PeriodicTask, IntervalSchedule

def tasks_check_domains( **kwargs):
    """
    Создаёт или обновляет расписание для периодической задачи проверки доменов.
    """

    schedule, _ = IntervalSchedule.objects.update_or_create(
        every=int(config("VERIFI_PERIOD",default=300)),
        period=IntervalSchedule.SECONDS,
    )

    PeriodicTask.objects.update_or_create(
        name="check_domains",
        task="proverator_app.tasks.check_domains",
        defaults={
            "interval": schedule,
            "enabled": True,
        },
    )

def tasks_clear_domains( **kwargs):
    """
    Создаёт или обновляет расписание для периодической задачи очистки БД 
    от старых результатов проверок.
    """
    schedule, _ = IntervalSchedule.objects.update_or_create(
        every=int(config("CLEAR_PERIOD",default=2)),
        period=IntervalSchedule.HOURS,
    )

    PeriodicTask.objects.update_or_create(
        name="clear_domains",
        task="proverator_app.tasks.clear_domains",
        defaults={
            "interval": schedule,
            "enabled": True,
        },
    )