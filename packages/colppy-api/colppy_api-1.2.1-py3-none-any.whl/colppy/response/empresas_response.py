from colppy.models.empresas import Empresa
from colppy.response.response import Response


class EmpresasResponse(Response):
    def __init__(self, http_response):
        super().__init__(Empresa, http_response)
