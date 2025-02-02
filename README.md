# Helm Scraper

## Descripción
Helm Scraper es una herramienta diseñada para ejecutarse dentro de un clúster de Kubernetes. Su función principal es recopilar información sobre todas las releases de Helm desplegadas en el clústerpara luego enviar esta información a Notion para un seguimiento y documentación centralizados.

## Características
- **Recopilación de Releases**: Escanea todos los namespaces del clúster para identificar las releases de Helm instaladas.
- **Integración con Notion**: Envía detalles de las releases y sus versiones a una página de Notion especificada para una fácil referencia y seguimiento.

## Requisitos Previos
- **Kubernetes**: Un clúster de Kubernetes en funcionamiento.
- **Helm**: Helm instalado y configurado.
- **Notion**: Una cuenta de Notion y una integración configurada para recibir datos.

## Instalación
El despliegue de Helm Scraper en el clúster se realiza mediante un chart de Helm disponible en el siguiente repositorio: [helm-scraper-chart](https://github.com/LaloMiranda/helm-scraper-chart).

Agregar el repositorio del chart:

```bash
helm repo add helm-scraper https://lalomiranda.github.io/helm-scraper-chart/
helm repo update
```

### Configuración
La aplicación se puede configurar mediante variables de entorno y valores del chart de Helm. A continuación, se detallan las principales opciones de configuración:

#### Integración con Notion:
- `NOTION_TOKEN`: Token secreto de la integración de Notion.
- `NOTION_DATABASE_ID`: ID de la base de datos de Notion donde se almacenará la información.
Estas variables se pueden establecer en el archivo values.yaml del chart de Helm o mediante la línea de comandos durante la instalación:

```bash
helm install helm-scraper helm-scraper/helm-scraper --set notion.token=your_notion_token --set notion.databaseId=your_database_id
```

## Uso
Una vez desplegada, la aplicación ejecutará periódicamente el proceso de scraping de las releases de Helm en el clúster y la información se enviará a Notion si la integración está configurada.