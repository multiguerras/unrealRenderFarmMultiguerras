FROM ghcr.io/epicgames/unreal-engine:dev-5.5

# Instala dependencias como root
USER root
RUN apt-get update && \
    apt-get install -y python3-pip cifs-utils && \
    pip3 install --no-cache-dir flask requests

# Crea el directorio de trabajo (y usuario ue5 existe en la imagen base)
WORKDIR /app

# Copia archivos con permisos de root
COPY ./ProyectoUnreal /app/ProyectoUnreal
COPY ./requestWorker.py /app/
COPY ./util /app/util/
COPY ./entrypoint.sh /app/entrypoint.sh

# Ajusta permisos antes de cambiar a ue5
RUN chmod +x /app/entrypoint.sh

# Cambia el usuario a ue5 (definido en la imagen base)
USER ue5

# Variables de entorno
ENV UNREAL_EXE="/UnrealEngine/Engine/Binaries/Linux/UnrealEditor"
ENV UNREAL_PROJECT="/app/ProyectoUnreal/UnrealMultiguerras.uproject"
ENV REQUEST_MANAGER_URL="http://localhost:5000"

ENV SAMBA_SERVER="//MI-SERVIDOR-SAMBA/ruta"
ENV SAMBA_USER="usuario_samba"
ENV SAMBA_PASSWORD="contrasena_samba"

ENTRYPOINT ["/app/entrypoint.sh"]