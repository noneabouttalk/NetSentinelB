# Usamos la base de Ubuntu 24.04 (Noble Numbat)
FROM ubuntu:24.04

# Evitamos que las instalaciones se detengan por prompts de configuración
ENV DEBIAN_FRONTEND=noninteractive

# 1. Instalación de dependencias de sistema
# Incluimos dos2unix para corregir scripts creados en Windows
RUN apt-get update && apt-get install -y \
    suricata \
    python3-pip \
    python3-venv \
    dos2unix \
    curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# 2. Configuración del Entorno Virtual de Python
# Esto garantiza que las librerías no entren en conflicto con el sistema
RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# 3. Instalación de dependencias de Python (requirements.txt)
# Copiamos primero el archivo para aprovechar la caché de capas de Docker
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. Preparación de Suricata
# Creamos las carpetas donde se guardarán los pcaps, los logs y las reglas
RUN mkdir -p /data/pcaps /var/log/suricata /var/lib/suricata/rules && \
    suricata-update

# 5. Copia de scripts del proyecto
COPY app.py .
COPY entrypoint.sh /entrypoint.sh

# 6. Corrección de formato y permisos
# dos2unix elimina el carácter oculto \r que Windows añade al guardar archivos
RUN dos2unix /entrypoint.sh && \
    chmod +x /entrypoint.sh

# Puerto por defecto para Streamlit
EXPOSE 8501

# Definimos el script de entrada (actualización de reglas)
ENTRYPOINT ["/entrypoint.sh"]

# Lanzamos la aplicación Streamlit
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]