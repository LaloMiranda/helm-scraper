import os
from dotenv import load_dotenv
from notion_client import Client
from helm_scraper import get_helm_releases, list_namespaces
from notion_integration import add_or_update_release

load_dotenv()

# Configurar cliente de Notion
notion = Client(auth=os.getenv("NOTION_TOKEN"))
DATABASE_ID = os.getenv("DATABASE_ID")

if __name__ == "__main__":
    # Obtener todos los namespaces disponibles
    namespaces = list_namespaces()
    if not namespaces:
        print("No se encontraron namespaces en el cluster.")
    else:
        print(f"Namespaces encontrados: {namespaces}")
    
    # Obtener releases de Helm y registrar en Notion
    for namespace in namespaces:
        print(f"\nObteniendo releases de Helm en el namespace '{namespace}':")
        releases = get_helm_releases(namespace=namespace)

        if not releases:
            print(f"No se encontraron releases en el namespace '{namespace}'.")
            continue

        for release in releases:
            release_name = release.get("name")
            app_version = release.get("app_version", "N/A")
            chart_version = release.get("chart", "N/A")

            # Registrar en Notion con namespace y manager
            add_or_update_release(
                name=release_name,
                namespace=namespace,
                app_version=app_version,
                chart_version=chart_version
                manager="Helm"
            )
