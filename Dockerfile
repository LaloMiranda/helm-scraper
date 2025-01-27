# Usar una imagen base ligera de Python
FROM python:3.11-slim

# Instalar dependencias necesarias para descargar y configurar Helm
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    tar && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Descargar y configurar Helm
RUN curl -fsSL -o helm.tar.gz https://get.helm.sh/helm-v3.13.0-linux-amd64.tar.gz && \
    tar -zxvf helm.tar.gz && \
    mv linux-amd64/helm /usr/local/bin/helm && \
    chmod +x /usr/local/bin/helm && \
    rm -rf linux-amd64 helm.tar.gz

# Establecer el directorio de trabajo
WORKDIR /app

# Copiar el script de la aplicación
COPY app.py /app/

# Instalar dependencias de Python
RUN pip install --no-cache-dir kubernetes

# Configurar el comando predeterminado
CMD ["python", "app.py"]
