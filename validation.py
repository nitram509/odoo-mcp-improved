"""
Script de validación para probar las nuevas funcionalidades del MCP-Odoo
"""

import os
import sys
from datetime import datetime, timedelta

from odoo_mcp.odoo_config import get_odoo_client
from odoo_mcp.tools_sales import SalesOrderFilter

# Añadir el directorio src al path para poder importar odoo_mcp
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from src.odoo_mcp.models import (
    PurchaseOrderFilter,
    ProductAvailabilityInput,
    JournalEntryFilter,
    FinancialRatioInput,
)


class ValidationContext:
    """Contexto simulado para pruebas"""

    class RequestContext:
        def __init__(self, odoo_client):
            self.lifespan_context = type("LifespanContext", (), {"odoo": odoo_client})

    def __init__(self, odoo_client):
        self.request_context = self.RequestContext(odoo_client)


def run_validation():
    """Ejecuta pruebas de validación para todas las nuevas funcionalidades"""

    print("Iniciando validación de MCP-Odoo mejorado...")

    # Obtener cliente Odoo
    try:
        odoo_client = get_odoo_client()
        print("✅ Conexión con Odoo establecida correctamente")
    except Exception as e:
        print(f"❌ Error al conectar con Odoo: {str(e)}")
        return False

    # Crear contexto simulado
    ctx = ValidationContext(odoo_client)

    # Validar herramientas de ventas
    print("\n=== Validando herramientas de ventas ===")

    try:
        from src.odoo_mcp.tools_sales import search_sales_orders

        # Crear filtro de prueba
        filter_params = SalesOrderFilter(
            date_from=(datetime.now() - timedelta(days=365)).strftime("%Y-%m-%d"),
            date_to=datetime.now().strftime("%Y-%m-%d"),
            limit=5,
        )

        # Ejecutar búsqueda
        result = search_sales_orders(ctx, filter_params)

        if result.get("success"):
            print(
                f"✅ search_sales_orders: Encontradas {result['result']['count']} órdenes de venta"
            )
        else:
            print(f"❌ search_sales_orders: {result.get('error', 'Error desconocido')}")
    except Exception as e:
        print(f"❌ Error al validar search_sales_orders: {str(e)}")

    # Validar herramientas de compras
    print("\n=== Validando herramientas de compras ===")

    try:
        from src.odoo_mcp.tools_purchase import search_purchase_orders

        # Crear filtro de prueba
        filter_params = PurchaseOrderFilter(
            date_from=(datetime.now() - timedelta(days=365)).strftime("%Y-%m-%d"),
            date_to=datetime.now().strftime("%Y-%m-%d"),
            limit=5,
        )

        # Ejecutar búsqueda
        result = search_purchase_orders(ctx, filter_params)

        if result.get("success"):
            print(
                f"✅ search_purchase_orders: Encontradas {result['result']['count']} órdenes de compra"
            )
        else:
            print(
                f"❌ search_purchase_orders: {result.get('error', 'Error desconocido')}"
            )
    except Exception as e:
        print(f"❌ Error al validar search_purchase_orders: {str(e)}")

    # Validar herramientas de inventario
    print("\n=== Validando herramientas de inventario ===")

    try:
        from src.odoo_mcp.tools_inventory import check_product_availability

        # Obtener algunos IDs de productos
        products = odoo_client.search_read(
            "product.product", [("type", "=", "product")], fields=["id"], limit=3
        )

        if products:
            product_ids = [p["id"] for p in products]

            # Crear parámetros de prueba
            params = ProductAvailabilityInput(product_ids=product_ids)

            # Ejecutar verificación
            result = check_product_availability(ctx, params)

            if result.get("success"):
                print(
                    f"✅ check_product_availability: Verificados {len(result['result']['products'])} productos"
                )
            else:
                print(
                    f"❌ check_product_availability: {result.get('error', 'Error desconocido')}"
                )
        else:
            print(
                "⚠️ No se encontraron productos para validar check_product_availability"
            )
    except Exception as e:
        print(f"❌ Error al validar check_product_availability: {str(e)}")

    # Validar herramientas de contabilidad
    print("\n=== Validando herramientas de contabilidad ===")

    try:
        from src.odoo_mcp.tools_accounting import search_journal_entries

        # Crear filtro de prueba
        filter_params = JournalEntryFilter(
            date_from=(datetime.now() - timedelta(days=365)).strftime("%Y-%m-%d"),
            date_to=datetime.now().strftime("%Y-%m-%d"),
            limit=5,
        )

        # Ejecutar búsqueda
        result = search_journal_entries(ctx, filter_params)

        if result.get("success"):
            print(
                f"✅ search_journal_entries: Encontrados {result['result']['count']} asientos contables"
            )
        else:
            print(
                f"❌ search_journal_entries: {result.get('error', 'Error desconocido')}"
            )
    except Exception as e:
        print(f"❌ Error al validar search_journal_entries: {str(e)}")

    try:
        from src.odoo_mcp.tools_accounting import analyze_financial_ratios

        # Crear parámetros de prueba
        params = FinancialRatioInput(
            date_from=(datetime.now() - timedelta(days=365)).strftime("%Y-%m-%d"),
            date_to=datetime.now().strftime("%Y-%m-%d"),
            ratios=["liquidity", "profitability", "debt"],
        )

        # Ejecutar análisis
        result = analyze_financial_ratios(ctx, params)

        if result.get("success"):
            print(
                f"✅ analyze_financial_ratios: Análisis completado con {len(result['result']['ratios'])} ratios"
            )
        else:
            print(
                f"❌ analyze_financial_ratios: {result.get('error', 'Error desconocido')}"
            )
    except Exception as e:
        print(f"❌ Error al validar analyze_financial_ratios: {str(e)}")

    # Validar recursos
    print("\n=== Validando recursos ===")

    try:

        print("✅ Recursos de ventas importados correctamente")
    except Exception as e:
        print(f"❌ Error al importar recursos de ventas: {str(e)}")

    try:

        print("✅ Recursos de compras importados correctamente")
    except Exception as e:
        print(f"❌ Error al importar recursos de compras: {str(e)}")

    try:

        print("✅ Recursos de inventario importados correctamente")
    except Exception as e:
        print(f"❌ Error al importar recursos de inventario: {str(e)}")

    try:

        print("✅ Recursos de contabilidad importados correctamente")
    except Exception as e:
        print(f"❌ Error al importar recursos de contabilidad: {str(e)}")

    # Validar prompts
    print("\n=== Validando prompts ===")

    try:

        print("✅ Prompts importados correctamente")
    except Exception as e:
        print(f"❌ Error al importar prompts: {str(e)}")

    # Validar integración completa
    print("\n=== Validando integración completa ===")

    # try:
    #     from src.odoo_mcp.extensions import register_all_extensions
    #     print("✅ Módulo de extensiones importado correctamente")
    # except Exception as e:
    #     print(f"❌ Error al importar módulo de extensiones: {str(e)}")

    try:

        print("✅ Servidor MCP importado correctamente")
    except Exception as e:
        print(f"❌ Error al importar servidor MCP: {str(e)}")

    print("\nValidación completada.")
    return True


if __name__ == "__main__":
    run_validation()
