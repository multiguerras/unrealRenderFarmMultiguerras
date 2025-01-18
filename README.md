# Unreal Render Farm

![IMG_4595](https://github.com/user-attachments/assets/5a40a70e-d72c-4991-a0be-3437832d4f6e)

Gracias a [@leixingyu](https://github.com/leixingyu) por la base del código.

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
- Con el script “requestSubmitter-desdeunreal.py” se pueden [enviar trabajos desde el render queue de Unreal](#request-subimitter-desde-render-queue).

## Por mejorar:

- [ ] Hacer documentación para enseñar cómo configurar la versión modificada
- [ ] Enseñar el porcentaje del progreso en la web
- [ ] Compartir pantalla al servidor para enseñar   

## Getting Started

### Prerequisites


- [Flask](https://pypi.org/project/Flask/): a micro web framework for creating APIs in Python
    ```
    pip install -U Flask
    ```
  the path to `flask.exe` needs to be specified in `requestManager.py`


- An Unreal Project with Movie Render Queue plugin enabled and at least one sequencer properly set up. 
The render farm needs at least
on render job to run, which requires a map/level, a level sequence and a master config.
  - the unreal executable and project path needs to be specified in `requestWorker.py`
  - the test job needs to be specified in `requestSubmitter.py`

### Launch

1. Run the `requestManager.py` first, which launches the server on `http://localhost:5000/`
2. Submit render jobs using `requestSubmitter.py`
3. (Optional) Browse render jobs statues in browser at server url
4. Render jobs by running `requestWorker.py`

### Request Subimitter desde render queue

Desde el script `requestSubmitter-desdeunreal.py` se pueden enviar todos los trabajos de varias colas de renderizado que hay en una carpeta dentro del proyecto.
Solo hay que especificar la carpeta donde están en la variable `renderqueuespath`