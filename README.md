# Unreal Render Farm

![IMG_4595](https://github.com/user-attachments/assets/5a40a70e-d72c-4991-a0be-3437832d4f6e)

[@leixingyu](https://github.com/leixingyu) programó [la base del código](https://github.com/leixingyu/unrealRenderFarm).

## Características

Las modificaciones que he hecho a partir del [repositorio original](https://github.com/leixingyu/unrealRenderFarm) son:

- Quitar la asignación automática del worker
  - Ahora el worker no está limitado a renderizar un trabajo determinado.
- Manager adaptado para Windows
- Script “renderRequest.py” separado
  - Ahora el worker utiliza “renderRequestWorker.py” para que edite la database desde HTTP.
- Preparado para escalarse
  - Al hacer independiente el worker y el Manager. Ambos se pueden ejecutar en dos máquinas diferentes.
- Configuración de workers movida a config.json
- Protegido con Cloudflare
- Con el script “requestSubmitter-desdeunreal.py” se pueden [enviar trabajos desde el render queue de Unreal](./requestSubimitter-desdeunreal.md).

## Por mejorar

- [ ] Hacer documentación para enseñar cómo configurar la versión modificada
- [ ] Enseñar el porcentaje del progreso en la web
- [ ] Compartir pantalla al servidor para enseñar

## Comenzando

### Prerrequisitos

- [Flask](https://pypi.org/project/Flask/): un microframework web para crear APIs en Python

    ```python
    pip install -U Flask
    ```

  La ruta a `flask.exe` debe ser especificada en `requestManager.py` (por defecto se usa la de "PATH").

- Un proyecto Unreal con el plugin Movie Render Queue habilitado con un Sequencer Level, un Config Preset y un asset de nivel.
  - Todas las configuraciones de rutas del proyecto y de unreal.exe tienen que estar especificadas en config.json
  - Si quieres mandar trabajos puedes editar la variable y ejecutar `requestSubmitter.py`.

### Iniciar

1. Ejecute primero `requestManager.py`, lo cual lanza el servidor en `http://localhost:5000/`.
2. Envíe trabajos de renderizado usando `requestSubmitter.py`.
3. (Opcional) Navegue por los estados de los trabajos de renderizado en el navegador en la URL del servidor.
4. Ejecute trabajos de renderizado mediante la ejecución de `requestWorker.py`.
