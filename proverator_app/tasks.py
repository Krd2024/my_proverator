from celery import shared_task

VERIFI_PERIOD=300

@shared_task
def check_domain():
    pass

