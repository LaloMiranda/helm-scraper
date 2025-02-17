import subprocess
import json
from kubernetes import client

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

        # Agregar el namespace y manager a cada release
        for release in releases:
            release["namespace"] = namespace if namespace else "default"
            release["manager"] = "Helm"

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
