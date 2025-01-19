# Request Subimitter desde render queue

Desde el script `requestSubmitter-desdeunreal.py` se pueden enviar todos los trabajos de varias colas de renderizado que hay en una carpeta dentro del proyecto.
Solo hay que especificar la carpeta donde están en la variable `renderqueuespath`

Para ejecutar el script se puede hacer desde la terminal de Windows de esta manera:

```bash

"c:\Program Files\Epic Games\UE_5.4\Engine\Binaries\Win64\UnrealEditor-Cmd.exe" "Proyecto\Proyecto.uproject" -ExecutePythonScript="(ruta a .py)" -log

```

<!--

"c:\Program Files\Epic Games\UE_5.5\Engine\Binaries\Win64\UnrealEditor-Cmd.exe" "c:\Documentos publicos\Unreal Projects\UnrealMultiguerras\UnrealMultiguerras.uproject" -ExecutePythonScript="c:\Users\pablo\Documents\Github\unrealRenderFarmMultiguerras\requestSubmitter-desdeunreal.py" -log

-->