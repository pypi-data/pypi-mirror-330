from colppy.request.request import Request


class EmpresasRequest(Request):
    def __init__(self, colppy_session_token=""):
        super().__init__(
            colppy_session_token=colppy_session_token,
            provision="Empresa",
            operacion="listar_empresa"
        )