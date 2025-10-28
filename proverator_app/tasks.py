import asyncio
from celery import shared_task
from loguru import logger

from proverator_app.models import Domain
from proverator_app.services.checker import check_all
from proverator_app.services.db import create_results_requests, domain_all




@shared_task
def check_domains():
    logger.info("Проверка Celery...")
    results = asyncio.run(check_all(domain_all()))  
    logger.info(f"Результаты: {results}")

    for data in results:
        print(
            f"Домен:{data.get('url')}\n"
            f"Статус: {data.get('status')}\n"
            f"Время ответа: {data.get('time_ms')}"
            )
    create_results_requests(results)
