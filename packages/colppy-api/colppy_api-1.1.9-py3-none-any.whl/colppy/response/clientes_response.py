from colppy.models.clientes import Cliente
from colppy.response.response import Response


class ClientesResponse(Response):
    def __init__(self, http_response):
        super().__init__(Cliente, http_response)
