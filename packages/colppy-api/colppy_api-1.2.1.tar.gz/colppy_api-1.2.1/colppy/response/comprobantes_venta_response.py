from colppy.models.comprobantes_venta import ComprobanteVenta
from colppy.response.response import Response


class ComprobanteVentaResponse(Response):
    def __init__(self, http_response):
        super().__init__(ComprobanteVenta, http_response)
