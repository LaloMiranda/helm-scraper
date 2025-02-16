import os
from dotenv import load_dotenv
from notion_client import Client
from kubernetes import client, config

from helm_scraper import get_helm_releases, list_namespaces
from notion_integration import add_or_update_release
from argo import get_argocd_token, get_applications, process_application

load_dotenv()

# Configurar cliente de Notion
notion = Client(auth=os.getenv("NOTION_TOKEN"))
DATABASE_ID = os.getenv("DATABASE_ID")

# Configuracion de accesos a Argo
ARGOCD_ENABLED = os.getenv("ARGOCD_ENABLED", "false").lower() in ["true", "1", "yes"]
ARGOCD_SERVER = os.getenv("ARGOCD_SERVER")
ARGOCD_USERNAME = os.getenv("ARGOCD_USERNAME")
ARGOCD_PASSWORD = os.getenv("ARGOCD_PASSWORD")

if __name__ == "__main__":
    try:
        config.load_incluster_config()  # Si se ejecuta dentro del cluster
    except config.ConfigException:
        config.load_kube_config()  # Si se ejecuta localmente


    ##### Ejecucion para la obtencion de aplicaciones instaladas con helm de manera directa

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
            namespace = release.get("namespace", "N/A")
            manager = release.get("manager", "N/A")


            add_or_update_release(
                notion=notion,
                database_id=DATABASE_ID,
                name=release_name,
                namespace=namespace,
                app_version=app_version,
                chart_version=chart_version,
                manager=manager
            )

    ##### Ejecucion para la obtencion de aplicaciones gestionadas con Argo
    if(ARGOCD_ENABLED):
        # Autenticacion a Argo
        token = get_argocd_token(ARGOCD_SERVER,ARGOCD_USERNAME,ARGOCD_PASSWORD)
        # Obtenemos el listado de apps
        apps = get_applications(ARGOCD_SERVER,token)
        # Procesamos la info de las applications
        app_sets = process_application(apps)

        for app in app_sets:
            add_or_update_release(
                    notion=notion,
                    database_id=DATABASE_ID,
                    name=app['name'],
                    namespace=app['namespace'],
                    app_version=app['app_version'],
                    chart_version=app['chart_version'],
                    manager=app['manager']
                )