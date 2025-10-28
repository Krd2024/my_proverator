import asyncio
from celery import shared_task
from loguru import logger
from decouple import config

from proverator_app.models import Domain
from proverator_app.services.checker import check_all
from proverator_app.services.db import create_results_requests, domain_all


@shared_task
def check_domains():
    try:
        results = asyncio.run(check_all(domain_all()))
    except Exception as e:
        logger.error(e)
    
    create_results_requests(results)


@shared_task
def clear_domains():
    try:
        for domain in domain_all():
            qs = domain.request_set.order_by("verified_at")
            count = qs.count()
            if count > int(config("NUM_CLEAR")):
                cutoff = qs[count - int(config("NUM_CLEAR"))].verified_at
                deleted, _ = domain.request_set.filter(verified_at__lt=cutoff).delete()               
                logger.info(f"✅ {domain} — удалено {deleted} старых записей")
            else:
                logger.info("✅ Нет записей для удаления")

    except Exception as e:
        logger.exception(f"❗Ошибка при очистке доменов: {e}")
