import requests
import os
from dotenv import load_dotenv

load_dotenv()

# Configuración
ARGOCD_SERVER = os.getenv("ARGOCD_SERVER")
ARGOCD_USERNAME = os.getenv("ARGOCD_USERNAME")
ARGOCD_PASSWORD = os.getenv("ARGOCD_PASSWORD")

def get_argocd_token():
    """Obtiene un token de autenticación en ArgoCD."""
    url = f"{ARGOCD_SERVER}/api/v1/session"
    response = requests.post(url, json={"username": ARGOCD_USERNAME, "password": ARGOCD_PASSWORD})
    
    if response.status_code == 200:
        return response.json()["token"]
    else:
        raise Exception(f"Error al obtener token: {response.text}")

def get_applications(token):
    """Obtiene el listado de aplicaciones desde ArgoCD."""
    url = f"{ARGOCD_SERVER}/api/v1/applications"
    headers = {"Authorization": f"Bearer {token}"}
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        return response.json()["items"]
    else:
        raise Exception(f"Error al obtener aplicaciones: {response.text}")

def process_application_sets(apps):
    """Procesa solo los ApplicationSets."""
    app_data = []

    for app in apps:
        if "sources" not in app.get("spec", {}):
            continue  # Saltamos las aplicaciones normales

        name = app["metadata"]["name"]
        destination = app.get("spec", {}).get("destination", {})
        namespace = destination.get("namespace") or destination.get("name") or "N/A"

        chart_version = None
        app_version = None

        sources = app["spec"]["sources"]

        for source in sources:
            if "chart" in source or "helm" in source:
                chart_version = source.get("targetRevision", "Desconocido")  # Usa targetRevision como versión del chart
                app_version = source.get("targetRevision", "Desconocido")
                break  # Tomamos el primer Helm válido y salimos

        if chart_version is None:
            chart_version = "Desconocido"
            app_version = "Desconocido"

        app_data.append({
            "name": name,
            "namespace": namespace,
            "chart_version": chart_version,
            "app_version": app_version
        })
    
    return app_data

if __name__ == "__main__":
    try:
        token = get_argocd_token()
        apps = get_applications(token)

        # Procesamos solo los ApplicationSets
        app_sets = process_application_sets(apps)

        # Imprimimos resultados de ApplicationSets
        print("\n🔹 ApplicationSets:")
        for app in app_sets:
            print(f"Nombre: {app['name']}, Namespace: {app['namespace']}, "
                  f"Chart Version: {app['chart_version']}, App Version: {app['app_version']}")

    except Exception as e:
        print(f"Error: {e}")
