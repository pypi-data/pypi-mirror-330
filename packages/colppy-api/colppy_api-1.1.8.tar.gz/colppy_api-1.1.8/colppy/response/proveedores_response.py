from colppy.models.proveedores import Proveedor
from colppy.response.response import Response


class ProveedoresResponse(Response):
    def __init__(self, http_response):
        super().__init__(Proveedor, http_response)
