from colppy.helpers.errors import ColppyError
from colppy.models.movimientos import Movimiento
from colppy.response.response import Response


class MovimientosResponse(Response):
    def __init__(self, http_response):
        super().__init__(Movimiento, http_response)

    def get_items(self):
        if not ColppyError(self._response).is_error():
            if self._response['response']['movimientos']:
                return [Movimiento(**movimiento) for movimiento in self._response['response']['movimientos']]

        return []
