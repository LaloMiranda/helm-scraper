from kubernetes import client, config
import subprocess

def get_helm_releases(namespace=None):
    """
    Ejecuta el comando `helm list` para obtener todas las releases de Helm.
    :param namespace: Namespace a filtrar (opcional). Si es None, busca en todos los namespaces.
    :return: Lista de releases con sus detalles.
    """
    try:
        # Construir el comando de Helm
        cmd = ["helm", "list", "--all", "--output", "json"]
        if namespace:
            cmd.extend(["--namespace", namespace])

        # Ejecutar el comando
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        releases = result.stdout

        print("=== Releases de Helm ===")
        print(releases)
    except subprocess.CalledProcessError as e:
        print(f"Error ejecutando Helm: {e.stderr}")
    except Exception as e:
        print(f"Error inesperado: {e}")


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

    # Obtener releases de Helm para cada namespace
    for namespace in namespaces:
        print(f"\nObteniendo releases de Helm en el namespace '{namespace}':")
        get_helm_releases(namespace=namespace)
