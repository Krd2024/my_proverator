from loguru import logger

from proverator_app.models import Domain
from proverator_app.services.util import pars_requests


def get_domain(domain_id: int = None):
    """Получить домен и вернуть распарсенные данные о проверке"""

    try:
        domain = Domain.objects.prefetch_related("request_set")
        logger.debug(domain)
        # Распарсить
        return pars_requests(list(domain))
    except Exception as e:
        logger.error(e)
