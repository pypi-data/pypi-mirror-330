from colppy.request.request import Request


class MovimientosRequest(Request):
    def __init__(self, auth_user, auth_password, params_user, token, id_empresa, from_date, to_date,
                 page_size=1000):
        super().__init__(page_size)
        self._auth_user = auth_user
        self._auth_password = auth_password
        self._params_user = params_user
        self._token = token
        self._id_empresa = id_empresa
        self._from_date = from_date
        self._to_date = to_date

    def to_dict(self):
        return {
            "auth": {
                "usuario": self._auth_user,
                "password": self._auth_password
            },
            "service": {
                "provision": "Contabilidad",
                "operacion": "listar_movimientosdiario"
            },
            "parameters": {
                "sesion": {
                    "usuario": self._params_user,
                    "claveSesion": self._token
                },
                "idEmpresa": self._id_empresa,
                "fromDate": self._from_date,
                "toDate": self._to_date,
                "start": self._start,
                "limit": self._limit,
            }
        }
