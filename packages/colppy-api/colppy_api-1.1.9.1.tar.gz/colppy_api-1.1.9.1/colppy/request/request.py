from argparse import ArgumentTypeError

import httpx
from colppy.helpers.logger import logger
from colppy.operations.config import get_config


class Request:
    def __init__(self, colppy_session_token="",
                 page_size=50, admits_paging=True, id_empresa=None,
                 provision="", operacion="", filters="", order="", from_date="", to_date=""):
        if not colppy_session_token:
            raise ValueError("Se debe proveer un token de colppy!")
        if not provision or not operacion:
            raise ValueError("Se debe proveer una provision o operacion!")
        if order and not (isinstance(order, list) or isinstance(order, dict)):
            raise ArgumentTypeError("El campo order debe ser una lista o un dict!")
        if filters and not isinstance(filters, list):
            raise ArgumentTypeError("El campo filters debe ser una lista!")

        self._admits_paging = admits_paging

        config = get_config()
        self._auth_user = config['ColppyAPI']['COLPPY_AUTH_USER']
        self._auth_password = config['ColppyAPI']['COLPPY_AUTH_PASSWORD']
        self._params_user = config['ColppyAPI']['COLPPY_PARAMS_USER']
        self._params_password = config['ColppyAPI']['COLPPY_PARAMS_PASSWORD']
        self._colppy_session_token = colppy_session_token

        self._start = 0
        self._page_size = page_size
        self._limit = self._page_size

        self._provision = provision
        self._operacion = operacion
        self._filters = filters
        self._id_empresa = id_empresa
        self._order = order
        self._from_date = from_date
        self._to_date = to_date

        self._auth_user = config['ColppyAPI']['COLPPY_AUTH_USER']
        self._auth_password = config['ColppyAPI']['COLPPY_AUTH_PASSWORD']
        self._params_user = config['ColppyAPI']['COLPPY_PARAMS_USER']
        self._params_password = config['ColppyAPI']['COLPPY_PARAMS_PASSWORD']

    @property
    def id_empresa(self):
        return self._id_empresa

    @id_empresa.setter
    def id_empresa(self, new_id_empresa):
        if not new_id_empresa:
            raise ValueError("El id_empresa no puede estar vacio!")
        self._id_empresa = new_id_empresa

    def init_paging(self):
        self._start = 0

    def next_page(self):
        self._start += self._page_size

    def admits_paging(self):
        return self._admits_paging

    def to_dict(self):
        data = {
            "auth": {
                "usuario": self._auth_user,
                "password": self._auth_password
            },
            "service": {
                "provision": self._provision,
                "operacion": self._operacion
            },
            "parameters": {
                "sesion": {
                    "usuario": self._params_user,
                    "claveSesion": self._colppy_session_token
                }
            }
        }

        # Agregar solo los parámetros que tienen valor
        optional_params = {
            "start": self._start,
            "limit": self._limit,
            "idEmpresa": self._id_empresa,
            "filter": self._filters,
            "order": self._order,
            "fromDate": self._from_date,
            "toDate": self._to_date
        }

        # Filtrar y agregar solo los valores que no sean None, "" o listas vacías
        data["parameters"].update({k: v for k, v in optional_params.items() if v not in [None, "", []]})

        return data


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