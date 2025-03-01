from typing import List

from colppy.models.proveedores import FilterItem, OrderItem
from colppy.request.request import Request


class ProveedoresRequest(Request):
    def __init__(self, page_size=50, colppy_session_token="",
                 id_empresa="", filters=None, order=None):
        self._filters: List[FilterItem] = (filters or []) + [
            {"field": "Activo", "op": "=", "value": 1}]
        self._order: List[OrderItem] = (order or []) + [
            {"field": "NombreFantasia", "dir": "desc"}]
        super().__init__(
            colppy_session_token=colppy_session_token,
            provision="Proveedor",
            operacion="listar_proveedor",
            id_empresa=id_empresa,
            page_size=page_size,
            filters=self._filters,
            order=self._order
        )
