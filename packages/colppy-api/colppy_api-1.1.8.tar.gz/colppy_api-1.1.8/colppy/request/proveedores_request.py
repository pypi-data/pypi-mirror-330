from typing import List

from colppy.models.proveedores import FilterItem, OrderItem
from colppy.request.request import Request


class ProveedoresRequest(Request):
    def __init__(self, auth_user, auth_password, params_user, token, id_empresa,
                 page_size=50, filters=None, order=None):
        super().__init__(page_size)
        self._auth_user = auth_user
        self._auth_password = auth_password
        self._params_user = params_user
        self._token = token
        self._id_empresa = id_empresa
        self._current_page = None
        self._total_pages = None
        self._filter: List[FilterItem] = (filters or []) + [
            {"field": "Activo", "op": "=", "value": 1}]
        self._order: List[OrderItem] = (order or []) + [
            {"field": "NombreFantasia", "dir": "desc"}]

    def to_dict(self):
        return {
            "auth": {
                "usuario": self._auth_user,
                "password": self._auth_password
            },
            "service": {
                "provision": "Proveedor",
                "operacion": "listar_proveedor"
            },
            "parameters": {
                "start": self._start,
                "limit": self._limit,
                "filter": self._filter,
                "order": self._order,
                "idEmpresa": self._id_empresa,
                "sesion": {
                    "usuario": self._params_user,
                    "claveSesion": self._token
                },
            }
        }
