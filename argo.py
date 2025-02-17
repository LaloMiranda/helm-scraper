import requests

def get_argocd_token(argocd_server, argocd_username, argocd_password):
    """Obtiene un token de autenticación en ArgoCD."""
    url = f"{argocd_server}/api/v1/session"
    response = requests.post(url, json={"username": argocd_username, "password": argocd_password})
    
    if response.status_code == 200:
        return response.json()["token"]
    else:
        raise Exception(f"Error al obtener token: {response.text}")

def get_applications(argocd_server, token):
    """Obtiene el listado de aplicaciones desde ArgoCD."""
    url = f"{argocd_server}/api/v1/applications"
    headers = {"Authorization": f"Bearer {token}"}
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        return response.json()["items"]
    else:
        raise Exception(f"Error al obtener aplicaciones: {response.text}")

def process_application(apps):
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
            "app_version": app_version,
            "manager": "ArgoCD"
        })
    
    return app_data
