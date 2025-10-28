import time
import httpx
import asyncio
from loguru import logger


async def check_url(client: httpx.AsyncClient, url: object) -> dict[str,str|int]:
    """
    Проверяет доступность одного URL.

    Измеряет время запроса, возвращает словарь:
      - ID домена в БД
      - URL
      - статус 
      - время отклика
    """

    start = time.perf_counter()
    try:
        response = await client.get(url.domain, timeout=5.0)
        request_ms = (time.perf_counter() - start) * 1000
        logger.info(f"{url} -> {response.status_code}")
        return {
            "domain_id":url.id,
            "url": url,
            "status": response.status_code,
            "time_ms": int(request_ms),
        }
    except httpx.RequestError as exc:
        request_ms = (time.perf_counter() - start) * 1000
        logger.warning(f"{url} -> Ошибка запроса: {exc}")
        return {
            "domain_id":url.id,
            "url": url,
            "status": 0,
            "time_ms": int(request_ms),
        }

    except Exception as e:
        request_ms = (time.perf_counter() - start) * 1000
        logger.error(e)
        return {
            "domain_id":url.id,
            "url": url,
            "status": -1,
            "time_ms": int(request_ms),
        }


async def check_all(urls:list[object]) -> dict[str,str|int]:
    """
    Cоздаёт один экземпляр httpx.AsyncClient и запускает
    параллельную проверку каждого URL с помощью check_url.
    
    """

    async with httpx.AsyncClient(verify=False, follow_redirects=True) as client:
        results = await asyncio.gather(*(check_url(client, url) for url in urls))
    return results
