from kubernetes import client, config
import subprocess
import json
import os
from notion_client import Client
from dotenv import load_dotenv
from notion_integration import add_or_update_release  # Importamos la función de Notion

load_dotenv()

# Configurar cliente de Notion
notion = Client(auth=os.getenv("NOTION_TOKEN"))

# ID de la base de datos de Notion
DATABASE_ID = os.getenv("DATABASE_ID")

def get_helm_releases(namespace=None):
    """
    Ejecuta el comando `helm list` para obtener todas las releases de Helm en un namespace.
    :param namespace: Namespace a filtrar (opcional). Si es None, busca en todos los namespaces.
    :return: Lista de releases con sus detalles.
    """
    try:
        cmd = ["helm", "list", "--all", "--output", "json"]
        if namespace:
            cmd.extend(["--namespace", namespace])

        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        releases = json.loads(result.stdout)  # Convertimos la salida JSON en un diccionario

        return releases
    except subprocess.CalledProcessError as e:
        print(f"Error ejecutando Helm: {e.stderr}")
        return []
    except Exception as e:
        print(f"Error inesperado: {e}")
        return []

def list_namespaces():
    """
    Lista todos los namespaces disponibles en el cluster.
    :return: Lista de namespaces.
    """
    try:
        v1 = client.CoreV1Api()
        namespaces = v1.list_namespace()
        return [ns.metadata.name for ns in namespaces.items]
    except Exception as e:
        print(f"Error al listar namespaces: {e}")
        return []

if __name__ == "__main__":
    # Cargar la configuración del cluster
    try:
        config.load_incluster_config()  # Si se ejecuta dentro del cluster
    except config.ConfigException:
        config.load_kube_config()  # Si se ejecuta localmente

    # Obtener todos los namespaces
    namespaces = list_namespaces()
    if not namespaces:
        print("No se encontraron namespaces en el cluster.")
    else:
        print(f"Namespaces encontrados: {namespaces}")

    # Obtener releases de Helm para cada namespace y registrarlas en Notion
    for namespace in namespaces:
        print(f"\nObteniendo releases de Helm en el namespace '{namespace}':")
        releases = get_helm_releases(namespace=namespace)

        if not releases:
            print(f"No se encontraron releases en el namespace '{namespace}'.")
            continue

        for release in releases:
            release_name = release.get("name")
            revision = int(release.get("revision", 0))
            app_version = release.get("app_version", "N/A")
            chart_version = release.get("chart", "N/A")  # Notion solo admite strings

            # Registrar en Notion
            add_or_update_release(
                name=release_name,
                revision=revision,
                app_version=app_version,
                chart_version=chart_version
            )
