"""
Client to work/process render request, which launches executor locally and
updates status to the server
"""


import logging
import os
import subprocess
import time

from util import client
from util import renderRequest


# Cambiar el nivel de logging a DEBUG para ver mensajes detallados
logging.basicConfig(level=logging.DEBUG)
LOGGER = logging.getLogger(__name__)

MODULE_PATH = os.path.dirname(os.path.abspath(__file__))

# render worker specific configuration
WORKER_NAME = 'RENDER_MACHINE_01'
UNREAL_EXE = r'C:\Program Files\Epic Games\UE_5.5\Engine\Binaries\Win64\UnrealEditor.exe'
UNREAL_PROJECT = r"D:\Documentos publicos\Unreal Projects\MeerkatDemo\MeerkatDemo.uproject"


def render(uid, umap_path, useq_path, uconfig_path):
    """
    Render a job locally using the custom executor (myExecutor.py)

    Note:
    I only listed the necessary arguments here,
    we can easily add custom commandline flags like '-StartFrame', '-FrameRate' etc.
    but we also need to implement in the MyExecutor class as well

    :param uid: str. render request uid
    :param umap_path: str. Unreal path to the map/level asset
    :param useq_path: str. Unreal path to the sequence asset
    :param uconfig_path: str. Unreal path to the preset/config asset
    :return: (str. str). output and error messages
    """
    command = [
        UNREAL_EXE,
        UNREAL_PROJECT,

        umap_path,
        "-JobId={}".format(uid),
        "-LevelSequence={}".format(useq_path),
        "-MoviePipelineConfig={}".format(uconfig_path),

        # required
        "-game",
        "-MoviePipelineLocalExecutorClass=/Script/MovieRenderPipelineCore.MoviePipelinePythonHostExecutor",
        "-ExecutorPythonClass=/Engine/PythonTypes.MoviePipelineExampleRuntimeExecutor",

        # render preview
        "-windowed",
        "-resX=1280",
        "-resY=720",

        # logging
        "-StdOut",
        "-FullStdOutLogOutput"
    ]
    env = os.environ.copy()
    env["UE_PYTHONPATH"] = MODULE_PATH
    proc = subprocess.Popen(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        env=env
    )
    stdout, stderr = proc.communicate()
    return proc.returncode, stdout, stderr  # Retornar el código de retorno y las salidas


if __name__ == '__main__':
    LOGGER.info('Starting render worker %s', WORKER_NAME)
    while True:
        rrequests = client.get_all_requests()
        LOGGER.info('Retrieved %d render requests', len(rrequests))
        
        # Mostrar detalles de cada solicitud para depuración
        for req in rrequests:
            LOGGER.debug('Request UID: %s, Worker: %s, Status: %s', req.uid, req.worker, req.status)
        
        uids = [rrequest.uid for rrequest in rrequests
                if rrequest.status == renderRequest.RenderStatus.ready_to_start]
        uids = uids[:1]  # limit to 1 job at a time
        
        LOGGER.info('Found %d ready_to_start jobs for worker %s', len(uids), WORKER_NAME)
    
        # render blocks main loop
        for uid in uids:
            LOGGER.info('rendering job %s', uid)
    
            rrequest = renderRequest.RenderRequest.from_db(uid)
            try:
                # Actualizar estado a 'in progress' antes de comenzar el renderizado
                rrequest.update(
                    progress=0,
                    status=renderRequest.RenderStatus.in_progress,
                    time_estimate='Calculando...'
                )
                LOGGER.info("Started rendering job %s", uid)
    
                returncode, stdout, stderr = render(
                    uid,
                    rrequest.umap_path,
                    rrequest.useq_path,
                    rrequest.uconfig_path
                )
                
                if returncode != 0:
                    raise subprocess.CalledProcessError(returncode, 'Unreal Engine render process failed', stderr.decode())

                # Actualizar estado a 'finished'
                rrequest.update(
                    progress=100,
                    status=renderRequest.RenderStatus.finished,
                    time_estimate='N/A'
                )
                LOGGER.info("Finished rendering job %s", uid)

                # Volver a consultar la lista de trabajos para evitar re-render
                rrequests = client.get_all_requests()
                LOGGER.debug('Refreshed request list after finishing job %s', uid)
            except subprocess.CalledProcessError as e:
                LOGGER.error("Error rendering job %s: %s", uid, e)
                # Actualizar estado a 'errored'
                rrequest.update(
                    progress=0,
                    status=renderRequest.RenderStatus.errored,
                    time_estimate='0'
                )
            except Exception as e:
                LOGGER.error("Unexpected error rendering job %s: %s", uid, e)
                # Actualizar estado a 'errored'
                rrequest.update(
                    progress=0,
                    status=renderRequest.RenderStatus.errored,
                    time_estimate='0'
                )
    
        # check assigned job every 10 sec after previous job has finished
        time.sleep(10)
        LOGGER.info('current job(s) finished, searching for new job(s)')
