from loguru import logger
from django.db.models import QuerySet

from proverator_app.tasks import VERIFI_PERIOD


def chunk_history(history: list[str], parts: int = 12) -> list[list[str], list[str]]:
    """Разбивает список history на 'parts' частей для графика."""

    if not history:
        return [[] for _ in range(parts)]

    chunk_size = len(history) // parts or 1
    chunks = [history[i : i + chunk_size] for i in range(0, len(history), chunk_size)]
    return chunks
    return chunks[:parts]


def uptime_cal(downtime: int = 0, total_time: int = 0) -> float:
    """Расчитать время доступности сайта"""

    logger.info(f"downtime={downtime} | total_time={total_time}")

    if total_time <= 0:
        return 0.0

    try:
        uptime_percent = (total_time - downtime) / total_time * 100
        print(f"Uptime: {uptime_percent:.2f}%")
        return round(uptime_percent, 2)
    except Exception as e:
        logger.error(e)


def pars_requests(domains: QuerySet) -> dict[str, str | int]:
    """Распарсить данные запросов"""

    context = {}
    # Список значений о работе сайта (up, down)
    lst_history = []
    downtime = 0
    uptime = 0
    try:
        domain = domains.first()
        domain_query = domain.request_set.all()
        for domain in domain_query:
            # Сайт
            context["domain"] = str(domain.domain).replace("http://", "")
            # Статус код
            context["status_code"] = domain.status_code 
            # Время ответа
            context["response_time"] = domain.response_time
            # Последнее время проверки
            context["last_check_time"] = (
                str(domain.verified_at).split()[1].split(".")[0]
            )
            # Сайт
            context["url"] = domain.domain
            # если статус 
            if 200 <= domain.status_code <= 226:
                lst_history.append("up")
                # Время работы
                uptime += VERIFI_PERIOD
            else:
                # Время простоя
                downtime += VERIFI_PERIOD
                lst_history.append("down")

            # Сколько работал сайт в % за время проверки - min=0 max=24 часа
            context["uptime_percent"] = uptime_cal(
                downtime=downtime, total_time=downtime + uptime
            )
            # Разбить данные о проверки сайта на чанги для графика
            context["history"] = chunk_history(lst_history)
            # Последнее в проверки (работал/не работал)
            context["is_up"] = True if context["history"][-1][-1] == "up" else False
            # Период проверки для вывода
            context["total_time"] = round((downtime + uptime) / 60 / 60, 1)
            # Список доменов
            context["domains"]=list(domains)
    except Exception as e:
        logger.error(e)

    return context
