import httpx
from colppy.helpers.logger import logger

class Request:
    def __init__(self, page_size=50, admits_paging=True):
        self._admits_paging = admits_paging
        self._page_size = page_size
        self._start = 0
        self._limit = self._page_size

    def next_page(self):
        self._start += self._page_size

    def admits_paging(self):
        return self._admits_paging


async def request_items(_base_url, request, response_class):
    async with httpx.AsyncClient(timeout=30.0) as client:
        try:
            response = await client.post(_base_url, json=request.to_dict())
            response.raise_for_status()

            response = response_class(response.json())
            return response.get_items()

        except httpx.HTTPStatusError as e:
            logger.error(f"Error getting objects: {e}")
            return []


async def request_items_paginated(_base_url, request, response_class):
    if not request.admits_paging(): #Si la request no es paginada (No deberia llamarse este metodo...)
        raise Exception(f"La clase {response_class} no admite request con paginado!\nHint: Usar request_items")

    ret: list = []
    items = await request_items(_base_url, request, response_class)

    while items:
        ret.extend(items)
        request.next_page()
        items = await request_items(_base_url, request, response_class)

    logger.debug(f"REQUEST: Se consiguio una respuesta de {response_class} con {len(ret)} items")
    return ret