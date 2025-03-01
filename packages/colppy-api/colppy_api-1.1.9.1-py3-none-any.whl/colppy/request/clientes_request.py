from colppy.request.request import Request


class ClientesRequest(Request):
    def __init__(self, page_size=50, colppy_session_token="",
                 id_empresa="", only_active=True):
        self._order = [
            {
                "field": "NombreFantasia",
                "dir": "asc"
            }
        ]

        self._filters = []
        if only_active:
            self._filters.append({
                "field": "Activo",
                "op": "=",
                "value": "1"
            })

        super().__init__(
            colppy_session_token=colppy_session_token,
            provision="Cliente",
            operacion="listar_cliente",
            id_empresa=id_empresa,
            page_size=page_size,
            filters=self._filters,
            order=self._order
        )
