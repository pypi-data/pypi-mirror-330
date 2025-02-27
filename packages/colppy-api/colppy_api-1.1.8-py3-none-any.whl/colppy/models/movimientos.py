from dataclasses import dataclass, field

from colppy.helpers.formatters import BaseModel


@dataclass(init=False)
class Movimiento(BaseModel):
    id_empresa: str = field(metadata={"alias": "idEmpresa"}, default=None)
    id_tabla: int = field(metadata={"alias": "idTabla"}, default=0)
    id_elemento: int = field(metadata={"alias": "idElemento"}, default=0)
    id_diario: int = field(metadata={"alias": "idDiario"}, default=0)
    id_elemento_contacto: int = field(metadata={"alias": "idElementoContacto"}, default=0)
    id_objeto_contacto: int = field(metadata={"alias": "idObjetoContacto"}, default=0)
    fecha_contabilizado: str = field(metadata={"alias": "FechaContabilizado"}, default=None)
    fecha_contable: str = field(metadata={"alias": "fechaContable"}, default=None)
    id_plan_cuenta: int = field(metadata={"alias": "idPlanCuenta"}, default=0)
    id_subdiario: int = field(metadata={"alias": "idSubdiario"}, default=0)
    debito_credito: str = field(metadata={"alias": "DebitoCredito"}, default=None)
    importe: float = field(metadata={"alias": "Importe"}, default=0.0)
    id_tabla_aplicado: int = field(metadata={"alias": "idTablaAplicado"}, default=0)
    id_elemento_aplicado: int = field(metadata={"alias": "idElementoAplicado"}, default=0)
    id_item: int = field(metadata={"alias": "idItem"}, default=0)
    id_item_aplicado: int = field(metadata={"alias": "idItemAplicado"}, default=0)
    ccosto1: str = field(metadata={"alias": "ccosto1"}, default=None)
    ccosto2: str = field(metadata={"alias": "ccosto2"}, default=None)
    conciliado: str = field(metadata={"alias": "Conciliado"}, default=None)
    batch: str = field(metadata={"alias": "batch"}, default=None)
    id_tercero: int = field(metadata={"alias": "idTercero"}, default=0)
    is_niif: str = field(metadata={"alias": "isNIIF"}, default=None)
    item_id: int = field(metadata={"alias": "itemId"}, default=0)

















