#!/bin/bash
set -e

# Para montar CIFS dentro del contenedor, es probable que necesites:
#   --cap-add=SYS_ADMIN
# cuando ejecutes 'docker run'.

# Crea la carpeta "Render" en caso de que no exista (ya debe estar en tu proyecto)
mkdir -p /app/ProyectoUnreal/Render

# Si las variables para Samba están definidas, monta
if [ -n "$SAMBA_SERVER" ] && [ -n "$SAMBA_USER" ] && [ -n "$SAMBA_PASSWORD" ]; then
    echo "Montando recurso Samba en /app/ProyectoUnreal/Render..."
    mount -t cifs "$SAMBA_SERVER" /app/ProyectoUnreal/Render \
        -o username="$SAMBA_USER",password="$SAMBA_PASSWORD",vers=3.0
else
    echo "Variables para Samba no definidas o incompletas. No se montará la carpeta."
fi

# Ejecuta el worker
exec python3 /app/requestWorker.py