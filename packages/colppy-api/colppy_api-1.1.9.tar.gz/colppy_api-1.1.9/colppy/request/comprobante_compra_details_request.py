from colppy.request.request import Request


class ComprobanteCompraDetailsRequest(Request):
    def __init__(self, auth_user, auth_password, params_user, token, id_empresa, id_comprobante):
        super().__init__(admits_paging=False)
        self._auth_user = auth_user
        self._auth_password = auth_password
        self._params_user = params_user
        self._token = token
        self._id_empresa = id_empresa
        self._id_comprobante = id_comprobante

    def to_dict(self):
        return {
            'auth': {
                'usuario': self._auth_user,
                'password': self._auth_password
            },
            'service': {
                'provision': 'FacturaCompra',
                'operacion': 'leer_facturacompra'
            },
            'parameters': {
                'sesion': {
                    'usuario': self._params_user,
                    'claveSesion': self._token
                },
                'idEmpresa': self._id_empresa,
                'idFactura': self._id_comprobante
            }
        }
