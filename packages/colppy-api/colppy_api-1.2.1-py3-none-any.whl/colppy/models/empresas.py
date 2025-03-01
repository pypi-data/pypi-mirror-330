from dataclasses import dataclass, field

from colppy.helpers.formatters import BaseModel


@dataclass(init=False)
class Empresa(BaseModel):
    id_empresa: int = field(metadata={'alias': 'IdEmpresa',"field_name": "id_colppy", "unique": True}, default=None)
    razon_social: str = field(metadata={'alias': 'razonSocial'}, default=None)
    nombre: str = field(metadata={'alias': 'Nombre'}, default=None)
    id_plan: str = field(metadata={'alias': 'idPlan', 'to_sql': False}, default=None)
    tipo: str = field(metadata={'alias': 'tipo', 'to_sql': False}, default=None)
    es_administrador: str = field(metadata={'alias': 'esAdministrador', 'to_sql': False}, default=None)
    logo_path: str = field(metadata={'alias': 'logoPath', 'to_sql': False}, default=None)
    # activa: int = field(metadata={'alias': 'activa'}, default=0)
    activa: int = field(metadata={'alias': 'activa',  'to_sql': False}, default=0)
    fecha_vencimiento: str = field(metadata={'alias': 'fechaVencimiento', 'to_sql': False}, default=None)
    ultimo_login: str = field(metadata={'alias': 'UltimoLogin', 'to_sql': False}, default=None)
    cuit: str = field(metadata={'alias': 'CUIT'}, default=None)
    fecha_cierre_impuesto: str = field(metadata={'alias': 'fecha_cierre_impuesto', 'to_sql': False}, default=None)
    actividad_economica: str = field(metadata={'alias': 'actividad_economica', 'to_sql': False}, default=None)


