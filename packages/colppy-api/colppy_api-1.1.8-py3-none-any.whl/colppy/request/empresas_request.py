from colppy.request.request import Request


class EmpresasRequest(Request):
    def __init__(self, auth_user, auth_password, params_user, token, filters=None):
        super().__init__()
        self._auth_user = auth_user
        self._auth_password = auth_password
        self._params_user = params_user
        self._token = token
        self._filters = filters if filters else []

    def to_dict(self):
        return {
            "auth": {
                "usuario": self._auth_user,
                "password": self._auth_password
            },
            "service": {
                "provision": "Empresa",
                "operacion": "listar_empresa"
            },
            "parameters": {
                "sesion": {
                    "usuario": self._params_user,
                    "claveSesion": self._token
                },
                "start": self._start,
                "limit": self._limit,
                "filter": self._filters
            }
        }
