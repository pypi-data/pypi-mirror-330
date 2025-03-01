from colppy.request.request import Request


class ComprobanteVentaRequest(Request):
    def __init__(self, page_size=100, colppy_session_token="",
                 id_empresa="", id_tipo_comprobante="", order_fields="", order="", filters=None):
        self._filters = [filters] if filters else []

        if id_tipo_comprobante:
            self._filters.append({
                "field": "idTipoComprobante",
                "op": "=",
                "value": id_tipo_comprobante
            })

        self._order_fields = order_fields if order_fields else ["idFactura"]
        self._order = order if order else "desc"
        self._order_dict = {
            "field": self._order_fields,
            "order": self._order
            }

        super().__init__(
            colppy_session_token=colppy_session_token,
            provision="FacturaVenta",
            operacion="listar_facturasventa",
            id_empresa=id_empresa,
            page_size=page_size,
            filters=self._filters,
            order=self._order_dict
        )

