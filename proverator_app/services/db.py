from loguru import logger
from django.db import IntegrityError
from proverator_app.models import Domain
from proverator_app.services.util import pars_requests


def get_domain(domain_id: int = None):
    """Получить домен и вернуть распарсенные данные о проверке"""

    try:
        logger.info(domain_id)
        if domain_id is not None:
            # logger.info(domain_id)
            domains = Domain.objects.prefetch_related("request_set").filter(id=domain_id)
        else:
            domains = Domain.objects.prefetch_related("request_set").all()

        logger.debug(domains)
        # Распарсить
        return pars_requests(domains)
    except Exception as e:
        logger.error(e)

def add_domain(domain:str)-> None:


    try:
        Domain.objects.create(domain=domain)
    except IntegrityError:
        return {"results":False,"message":f"❗ Домен '{domain}' уже существует!"}
    except Exception as e:
        logger.error(e)
        return {"results":False,"message":"f❗ {e}"}
    return {"results":True,"message":f"✅ Домен '{domain}' успешно добавлен!"}