from colppy.helpers.errors import ColppyError
from colppy.models.comprobante_venta_details import ComprobanteVentaDetails, ComprobanteVentaDetailsItem
from colppy.response.response import Response


class ComprobanteVentaDetailsResponse(Response):
    def __init__(self, http_response):
        super().__init__(ComprobanteVentaDetails, http_response)

    def get_items(self):
        if not ColppyError(self._response).is_error():
            if self._response['response']['infofactura']:
                items = self._response['response']['itemsFactura'] or []
                items_objects = [ComprobanteVentaDetailsItem(**item) for item in items]
                details = ComprobanteVentaDetails(**self._response['response']['infofactura'])
                details.items = items_objects
                return details
            return None
