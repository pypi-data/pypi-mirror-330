from dataclasses import dataclass, field
from typing import TypedDict

from colppy.helpers.formatters import BaseModel


class FilterItem(TypedDict):
    field: str
    op: str
    value: str | int


@dataclass(init=False)
class ComprobanteCompra(BaseModel):
    id_factura: int = field(metadata={"alias": "idFactura", "field_name": "id_colppy", "unique": True}, default=None)
    id_tipo_factura: str = field(metadata={"alias": "idTipoFactura"}, default=None)
    id_tipo_comprobante: str = field(metadata={"alias": "idTipoComprobante"}, default=None)
    id_proveedor: str = field(metadata={"alias": "idProveedor"}, default=None)
    nro_factura: str = field(metadata={"alias": "nroFactura"}, default=None)
    id_moneda: str = field(metadata={"alias": "idMoneda"}, default=None)
    fecha_factura: str = field(metadata={"alias": "fechaFactura"}, default=None)
    fecha_factura_doc: str = field(metadata={"alias": "fechaFacturaDoc"}, default=None)
    fecha_pago: str = field(metadata={"alias": "fechaPago"}, default=None)
    id_condicion_pago: str = field(metadata={"alias": "idCondicionPago"}, default=None)
    descripcion: str = field(metadata={"alias": "descripcion"}, default=None)
    id_estado_factura: str = field(metadata={"alias": "idEstadoFactura"}, default=None)
    total_factura: str = field(metadata={"alias": "totalFactura"}, default=None)
    id_ret_ganancias: str = field(metadata={"alias": "idRetGanancias"}, default=None)
    iibb_local: str = field(metadata={"alias": "IIBBLocal"}, default=None)
    iibb_otro: str = field(metadata={"alias": "IIBBOtro"}, default=None)
    iva_105: str = field(metadata={"alias": "IVA105"}, default=None)
    iva_21: str = field(metadata={"alias": "IVA21"}, default=None)
    iva_27: str = field(metadata={"alias": "IVA27"}, default=None)
    neto_gravado: str = field(metadata={"alias": "netoGravado"}, default=None)
    neto_no_gravado: str = field(metadata={"alias": "netoNoGravado"}, default=None)
    percepcion_iibb: str = field(metadata={"alias": "percepcionIIBB"}, default=None)
    percepcion_iibb1: str = field(metadata={"alias": "percepcionIIBB1"}, default=None)
    percepcion_iibb2: str = field(metadata={"alias": "percepcionIIBB2"}, default=None)
    percepcion_iva: str = field(metadata={"alias": "percepcionIVA"}, default=None)
    total_iva: str = field(metadata={"alias": "totalIVA"}, default=None)
    valor_cambio: str = field(metadata={"alias": "valorCambio"}, default=None)
    total_aplicado: float = field(metadata={"alias": "totalaplicado"}, default=0.0)
    razon_social: str = field(metadata={"alias": "RazonSocial"}, default=None)
    nombre_fantasia: str = field(metadata={"alias": "NombreFantasia"}, default=None)


