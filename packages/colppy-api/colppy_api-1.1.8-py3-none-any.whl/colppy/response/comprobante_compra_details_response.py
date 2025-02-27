from colppy.helpers.errors import ColppyError
from colppy.models.comprobante_compra_details import ComprobanteCompraDetails, ComprobanteCompraDetailsItem
from colppy.response.response import Response


class ComprobanteCompraDetailsResponse(Response):
    def __init__(self, http_response):
        super().__init__(ComprobanteCompraDetails, http_response)

    def get_items(self):
        if not ColppyError(self._response).is_error():
            if self._response['response']['infofactura']:
                items = self._response['response']['itemsFactura'] or []
                items_objets = [ComprobanteCompraDetailsItem(**item) for item in items]
                details = ComprobanteCompraDetails(**self._response['response']['infofactura'])
                details.items = items_objets
                return details
            return None
