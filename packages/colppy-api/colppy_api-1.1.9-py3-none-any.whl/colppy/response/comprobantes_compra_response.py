from colppy.models.comprobantes_compra import ComprobanteCompra
from colppy.response.response import Response


class ComprobanteCompraResponse(Response):
    def __init__(self, http_response):
        super().__init__(ComprobanteCompra, http_response)
