import asyncio
from colppy.operations.main import ColppyAPIClient
from groovindb import GroovinDB
from colppy.helpers.formatters import sql_bulk
from db_types import GeneratedClient

async def main():
    db: GeneratedClient = GroovinDB().client
    colppy_client = ColppyAPIClient()
    await colppy_client.get_token()

    items = await colppy_client.get_empresas()
    query_empresas = sql_bulk(models=items, schema_db="norm_colppy", table_name="empresas")
    await db.dev.execute(query_empresas)

    items = await colppy_client.get_all_clientes()
    query_clientes = sql_bulk(models=items, schema_db="norm_colppy", table_name="clientes")

    items = await colppy_client.get_all_proveedores()
    query_proveedores = sql_bulk(models=items, schema_db="norm_colppy", table_name="proveedores")

    items = await colppy_client.get_all_movimientos()
    query_movimientos = sql_bulk(models=items, schema_db="norm_colppy", table_name="movimientos")
    print(query_movimientos)

    items = await colppy_client.get_all_movimientos()
    query_movimientos = sql_bulk(models=items, schema_db="norm_colppy", table_name="movimientos")

    # items = await colppy_client.get_all_comprobantes_compra()
    # query_comprobantes_compra = sql_bulk(models=items, schema_db="norm_colppy", table_name="comprobantes_compra")
    # print(query_comprobantes_compra)
    #
    # items = await colppy_client.get_all_comprobantes_venta()
    # query_comprobantes_venta = sql_bulk(models=items, schema_db="norm_colppy", table_name="comprobantes_venta")
    # print(query_comprobantes_venta)

    # items = await colppy_client.get_all_comprobante_compra_details_by_id()
    # query_comprobante_compra_details = sql_bulk(models=items, schema_db="norm_colppy", table_name="comprobante_compra_details")
    #
    # items = await colppy_client.get_all_comprobante_venta_details_by_id()
    # query_comprobante_venta_details = sql_bulk(models=items, schema_db="norm_colppy", table_name="comprobante_venta_details")

    # items = await colppy_client.get_all_cobro_factura()
    # query_cobro_factura = sql_bulk(models=items, schema_db="norm_colppy", table_name="cobro_factura")

    await db.dev.execute("truncate table norm_colppy.empresas;")
    await db.dev.execute("truncate table norm_colppy.clientes;")
    await db.dev.execute("truncate table norm_colppy.proveedores;")
    await db.dev.execute("truncate table norm_colppy.movimientos;")
    # await db.dev.execute("truncate table norm_colppy.comprobantes_compra;")
    # await db.dev.execute("truncate table norm_colppy.comprobantes_venta;")
    # await db.dev.execute("truncate table norm_colppy.comprobante_compra_details;")
    # await db.dev.execute("truncate table norm_colppy.comprobante_venta_details;")
    # await db.dev.execute("truncate table norm_colppy.cobro_factura;")

    await db.dev.execute(query_empresas)
    await db.dev.execute(query_clientes)
    await db.dev.execute(query_proveedores)
    await db.dev.execute(query_movimientos)
    # await db.dev.execute(query_comprobantes_compra)
    # await db.dev.execute(query_comprobantes_venta)
    # await db.dev.execute(query_comprobante_compra_details)
    # await db.dev.execute(query_comprobante_venta_details)
    # await db.dev.execute(query_cobro_factura)

    print(f"EMPRESAS: {await db.dev.execute('select count(*) from norm_colppy.empresas')}\n" 
          f"CLIENTES: {await db.dev.execute('select count(*) from norm_colppy.clientes')}\n"
          f"PROVEEDORES: {await db.dev.execute('select count(*) from norm_colppy.proveedores')}\n"
          f"MOVIMIENTOS: {await db.dev.execute('select count(*) from norm_colppy.movimientos')}\n"
          # f"COMPROBANTES COMPRA: {await db.dev.execute('select count(*) from norm_colppy.comprobantes_compra')}\n"
          # f"COMPROBANTES VENTA: {await db.dev.execute('select count(*) from norm_colppy.comprobantes_venta')}\n"
          )

    await colppy_client.logout()

if __name__ == "__main__":
    asyncio.run(main())
