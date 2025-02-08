def get_release_page_id(name):
    """
    Busca una release en la base de datos de Notion y devuelve su ID si existe.
    """
    try:
        response = notion.databases.query(
            **{
                "database_id": DATABASE_ID,
                "filter": {
                    "property": "Name",
                    "title": {
                        "equals": name
                    }
                }
            }
        )
        results = response.get("results", [])
        if results:
            return results[0]["id"]  # Retorna el ID de la página si ya existe
        return None
    except Exception as e:
        print(f"Error al buscar la release en Notion: {e}")
        return None

def add_or_update_release(name, namespace, app_version, chart_version, manager):
    """
    Agrega o actualiza una release en la base de datos de Notion.
    """
    page_id = get_release_page_id(name)

    if page_id:
        # Si la release ya existe, la actualiza
        try:
            notion.pages.update(
                **{
                    "page_id": page_id,
                    "properties": {
                        "Namespace": {"rich_text": [{"text": {"content": namespace}}]},
                        "App Version": {"rich_text": [{"text": {"content": app_version}}]},
                        "Chart Version": {"rich_text": [{"text": {"content": chart_version}}]},
                        "Manager": {"rich_text": [{"text": {"content": manager}}]}
                    }
                }
            )
            print(f"Release '{name}' actualizada en Notion.")
        except Exception as e:
            print(f"Error al actualizar la release en Notion: {e}")
    else:
        # Si la release no existe, la crea
        try:
            notion.pages.create(
                **{
                    "parent": {"database_id": DATABASE_ID},
                    "properties": {
                        "Name": {"title": [{"text": {"content": name}}]},
                        "Namespace": {"rich_text": [{"text": {"content": namespace}}]},
                        "App Version": {"rich_text": [{"text": {"content": app_version}}]},
                        "Chart Version": {"rich_text": [{"text": {"content": chart_version}}]},
                        "Manager": {"rich_text": [{"text": {"content": manager}}]}
                    }
                }
            )
            print(f"Release '{name}' agregada a Notion con éxito.")
        except Exception as e:
            print(f"Error al agregar la release a Notion: {e}")
