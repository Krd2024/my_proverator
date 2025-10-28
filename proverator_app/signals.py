from django_celery_beat.models import PeriodicTask, IntervalSchedule

from decouple import config


def tasks_check_domains( **kwargs):
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