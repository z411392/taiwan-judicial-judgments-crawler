from injector import Injector
from httpx import AsyncClient as HttpConnectionPool


async def shutdown(injector: Injector):
    http_connection_pool = injector.get(HttpConnectionPool)
    await http_connection_pool.aclose()
