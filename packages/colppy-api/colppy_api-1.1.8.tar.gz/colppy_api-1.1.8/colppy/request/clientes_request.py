from colppy.request.request import Request


class ClientesRequest(Request):
    def __init__(self, auth_user, auth_password, params_user, token, id_empresa,
                 only_active=True, page_size=50):
        super().__init__(page_size)
        self._auth_user = auth_user
        self._auth_password = auth_password
        self._params_user = params_user
        self._id_empresa = id_empresa
        self._only_active = only_active
        self._filters = []
        self._token = token

    def to_dict(self):
        if self._only_active:
            self._filters.append({
                "field": "Activo",
                "op": "=",
                "value": "1"
            })

        return {
            "auth": {
                "usuario": self._auth_user,
                "password": self._auth_password
            },
            "service": {
                "provision": "Cliente",
                "operacion": "listar_cliente"
            },
            "parameters": {
                "sesion": {
                    "usuario": self._params_user,
                    "claveSesion": self._token
                },
                "idEmpresa": self._id_empresa,
                "start": self._start,
                "limit": self._limit,
                "filter": self._filters,
                "order": [
                    {
                        "field": "NombreFantasia",
                        "dir": "asc"
                    }
                ]
            }
        }
