from django_celery_beat.models import PeriodicTask, IntervalSchedule

from decouple import config


# def tasks_check_domains(sender, **kwargs):
def tasks_check_domains( **kwargs):
    schedule, _ = IntervalSchedule.objects.get_or_create(
        every=config("VERIFI_PERIOD"),
        period=IntervalSchedule.SECONDS,
    )

    PeriodicTask.objects.get_or_create(
        name="check_domains",
        task="proverator_app.tasks.check_domains",
        defaults={
            "interval": schedule,
            "enabled": True,
        },
    )
