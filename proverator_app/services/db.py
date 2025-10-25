from loguru import logger

from proverator_app.models import Domain
from proverator_app.services.util import pars_requests


def get_domain(domain_id: int = 2):
    """Получить домен и вернуть распарсенные данные о проверке"""

    try:
        logger.info(domain_id)
        if domain_id is not None:
            logger.info(domain_id)
            domains = Domain.objects.prefetch_related("request_set").filter(id=domain_id)
        else:
            domains = Domain.objects.prefetch_related("request_set")
        logger.debug(domains)
        # Распарсить
        return pars_requests(domains)
    except Exception as e:
        logger.error(e)
