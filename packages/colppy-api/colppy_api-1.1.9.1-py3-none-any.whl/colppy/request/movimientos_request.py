from colppy.request.request import Request


class MovimientosRequest(Request):
    def __init__(self, colppy_session_token="", page_size=1000,
                 id_empresa="", from_date="2013-01-01", to_date="2040-01-01", filters=None):
        super().__init__(
            colppy_session_token=colppy_session_token,
            provision="Contabilidad",
            operacion="listar_movimientosdiario",
            id_empresa=id_empresa,
            page_size=page_size,
            from_date=from_date,
            to_date=to_date,
            filters=filters
        )
