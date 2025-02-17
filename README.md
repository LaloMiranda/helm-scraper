# Helm Scraper

## Descripción
Helm Scraper es una herramienta diseñada para ejecutarse dentro de un clúster de Kubernetes. Su función principal es recopilar información sobre todas las releases de Helm desplegadas en el clúster para luego enviar esta información a Notion y así lograr un seguimiento y documentación centralizados.

## Características
- **Recopilación de Releases**: Escanea todos los namespaces del clúster para identificar las releases de Helm instaladas.
- **Integración con Notion**: Envía detalles de las releases y sus versiones a una página de Notion especificada para una fácil referencia y seguimiento.

## Requisitos Previos
- **Kubernetes**: Un clúster de Kubernetes en funcionamiento.
- **Helm**: Helm instalado y configurado.
- **Notion**: Una cuenta de Notion y una integración configurada para recibir datos.

## Instalación del repositorio de Helm
El despliegue de Helm Scraper en el clúster se realiza mediante un chart de Helm disponible en el siguiente repositorio: [helm-scraper-chart](https://github.com/LaloMiranda/helm-scraper-chart).

Agregar el repositorio del chart:

```bash
helm repo add helm-scraper https://lalomiranda.github.io/helm-scraper-chart/
helm repo update
```

## Configuración

### Notion
- `notionToken`: Token secreto de la integración de Notion.
- `databaseID`: ID de la base de datos de Notion donde se almacenará la información.
Estas variables se pueden establecer en el archivo *values.yaml* del chart de Helm:

```yaml
[...]
notion: 
  notionToken: ""
  databaseId: ""
```
### ArgoCD
- `enabled`: Habilita el scraping del servidor de Argo.
- `server`: URL del servidor de Argo a escanear.
- `user`: Usuario para autenticarse en Argo.
- `password`: Contraseña del usuario anterior,

Estas variables se establecen en el siguiente fragmento del archivo *values.yaml*:

```yaml
[...]
argocd:
  enabled: false
  server: ""
  user: ""
  password: ""
```

## Uso
Una vez desplegada, la aplicación ejecutará periódicamente el proceso de scraping de las releases de Helm en el clúster y la información se enviará a Notion si la integración está correctamente configurada.