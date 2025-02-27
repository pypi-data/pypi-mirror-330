from colppy.models.compras_pago_details import CompraPagoDetail
from colppy.response.response import Response


class ComprasPagoDetailsResponse(Response):
    def __init__(self, http_response):
        super().__init__(CompraPagoDetail, http_response)
