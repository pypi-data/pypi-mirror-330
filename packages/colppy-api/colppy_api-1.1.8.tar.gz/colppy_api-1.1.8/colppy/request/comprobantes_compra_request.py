from colppy.request.request import Request


class ComprobanteCompraRequest(Request):
    def __init__(self, auth_user, auth_password, params_user, token, id_empresa,
                 id_tipo_comprobante=None, filters=None, order_fields=None, order=None, page_size=100):
        super().__init__(page_size)
        self._auth_user = auth_user
        self._auth_password = auth_password
        self._params_user = params_user
        self._token = token
        self._id_empresa = id_empresa
        self._filters = [filters] if filters else []
        if id_tipo_comprobante:
            self._filters.append({
                "field": "idTipoComprobante",
                "op": "=",
                "value": id_tipo_comprobante
            })
        self._order_fields = order_fields if order_fields else ["idFactura"]
        self._order = order if order else "desc"

    def to_dict(self):
        return {
            "auth": {
                "usuario": self._auth_user,
                "password": self._auth_password
            },
            "service": {
                "provision": "FacturaCompra",
                "operacion": "listar_facturasCompra"
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
                "order": {
                    "field": self._order_fields,
                    "order": self._order
                }
            }
        }
