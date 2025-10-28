import time
import httpx
import asyncio
from loguru import logger


async def check_url(client: httpx.AsyncClient, url: object) -> dict[str,str|int]:
    start = time.perf_counter()
    try:
        response = await client.get(url.domain, timeout=5.0)
        logger.info(f"{url} -> {response.status_code}")
        request_ms = (time.perf_counter() - start) * 1000
        return {
            "domain_id":url.id,
            "url": url,
            "status": response.status_code,
            "time_ms": int(request_ms),
        }
    except httpx.RequestError as exc:
        request_ms = (time.perf_counter() - start) * 1000

        logger.warning(f"{url} -> Ошибка запроса: {exc}")
        return {"url": url, "status": "error", "time_ms": int(request_ms)}


async def check_all(urls:list[object]) -> dict[str,str|int]:

    async with httpx.AsyncClient(verify=False, follow_redirects=True) as client:
        results = await asyncio.gather(*(check_url(client, url) for url in urls))
    return results
