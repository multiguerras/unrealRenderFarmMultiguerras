import sys
import os
import logging
import unreal # type: ignore

# Directorio donde se encuentran las colas de render
renderqueuespath = "/Game/Cinematics/GruposEscenas"

# Agrega el directorio del script al sys.path
script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(script_dir)

from util import client

logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)

def send(d):
    """
    Envía/Registra una nueva solicitud de render

    :param d: dict con la información de la solicitud de render
    """
    rrequest = client.add_request(d)
    if rrequest:
        LOGGER.info('La solicitud %s se envió correctamente al servidor', rrequest.uid)

def gather_render_jobs_from_queues(folder_path):
    """
    1. Recorre la carpeta 'folder_path' buscando assets de tipo MoviePipelineQueue.
    2. Para cada cola encontrada, itera sobre los trabajos (jobs) internos.
    3. Utiliza la lógica de "job.sequence" para obtener la referencia al Level Sequence.
    4. Utiliza 'job.map' para obtener la referencia a un mapa (a menudo devuelto como un objeto 'World').
    5. Extrae la información deseada y construye un diccionario con los datos de cada toma.
    """
    # Obtiene una instancia del Asset Registry para trabajar con referencias de assets.
    asset_registry = unreal.AssetRegistryHelpers.get_asset_registry()
    
    assets = unreal.EditorAssetLibrary.list_assets(folder_path, recursive=True)
    render_jobs = []

    for asset_path in assets:
        asset = unreal.EditorAssetLibrary.load_asset(asset_path)
        # Comprueba si el asset es una MoviePipelineQueue
        if isinstance(asset, unreal.MoviePipelineQueue):
            # Por cada job presente en la cola, extrae la información asociada
            for job in asset.get_jobs():
                job_name = job.get_editor_property("job_name") or job.get_name()
                
                seq_soft_obj_reference = job.sequence
                map_soft_obj_reference = job.map  # Esto suele ser un objeto 'World' en Unreal

                umap_path = ""
                useq_path = ""
                uconfig_path = ""

                if seq_soft_obj_reference:
                    seq_object_path = seq_soft_obj_reference.to_tuple()[0]
                    seq_asset_data = asset_registry.get_asset_by_object_path(
                        unreal.Name(str(seq_object_path))
                    )
                    seq_asset = seq_asset_data.get_asset()
                    
                    # Convierte a LevelSequence para obtener nombre/rutas
                    seq = unreal.LevelSequence.cast(seq_asset)
                    if seq:
                        useq_path = seq.get_path_name()

                # Para la referencia al mapa, se trata a menudo de un World (no un Level)
                if map_soft_obj_reference:
                    map_object_path = map_soft_obj_reference.to_tuple()[0]
                    map_asset_data = asset_registry.get_asset_by_object_path(
                        unreal.Name(str(map_object_path))
                    )
                    map_asset = map_asset_data.get_asset()
                    # Dado que es un World, simplemente obtenemos la ruta para el umap
                    if map_asset:
                        umap_path = map_asset.get_path_name()
                
                # Obtener el path de la configuración del job
                config = job.get_configuration()
                if config:
                    uconfig_path = config.get_path_name()

                job_entry = {
                    'name': job_name,
                    'owner': 'TEST_SUBMITTER_01',
                    'umap_path': umap_path,
                    'useq_path': useq_path,
                    'uconfig_path': uconfig_path
                }

                render_jobs.append(job_entry)

    return render_jobs

if __name__ == '__main__':
    jobs = gather_render_jobs_from_queues(renderqueuespath)

    for job in jobs:
        print(job)
        # send(job)