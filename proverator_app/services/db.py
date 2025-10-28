import time
from loguru import logger
from django.db import IntegrityError
from proverator_app.models import Domain, Request
from proverator_app.services.util import pars_requests
from django.utils import timezone


def get_domain(domain_id: int = None):
    """Получить домен  и вернуть распарсенные данные о проверке"""

    try:
        if domain_id is not None:
            domains = Domain.objects.prefetch_related("request_set").filter(
                id=domain_id
            )
        else:
            domains = Domain.objects.prefetch_related("request_set").all()
    except Exception as e:
        logger.error(e)
        domains = []

    # Распарсить
    return pars_requests(domains)


def add_domain(domain: str) -> None:
    """Добавить домен в БД"""

    try:
        Domain.objects.create(domain=domain)
    except IntegrityError:
        return {"results": False, "message": f"❗ Домен '{domain}' уже существует!"}
    except Exception as e:
        logger.error(e)
        return {"results": False, "message": "f❗ {e}"}
    return {"results": True, "message": f"✅ Домен '{domain}' успешно добавлен!"}


def domain_all() -> list[object]:
    "Получить и вернуть все домены"
    try:
        return list(Domain.objects.all())
    except Exception as e:
        logger.error(e)
        return []


def create_results_requests(results: list[dict[str, str | int]]):
    try:
        lst_obj_request = []
        for data in results:
            lst_obj_request.append(
                Request(
                    domain_id=int(data.get("domain_id")),
                    status_code=data.get("status"),
                    response_time=data.get("time_ms"),
                    verified_at=timezone.now(),
                )
            )
        logger.info(lst_obj_request)

        Request.objects.bulk_create(lst_obj_request)

    except Exception as e:
        logger.error(e)
