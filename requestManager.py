"""
Remote Render HTTP Server with REST API

Also manages render request (which currently only involves assigning
jobs to worker)
"""

import logging
import time
import os

from flask import Flask
from flask import request
from flask import render_template

from util import renderRequest


MODULE_PATH = os.path.dirname(os.path.abspath(__file__))
HTML_FOLDER = os.path.join(MODULE_PATH, 'html')

LOGGER = logging.getLogger(__name__)

# region HTTP REST API
app = Flask(__name__)
FLASK_EXE = r'flask'


@app.route('/')
def index_page():
    """
    Server landing page
    """
    rrequests = renderRequest.read_all()
    if not rrequests:
        return 'Welcome!'

    jsons = [rrequest.to_dict() for rrequest in rrequests]

    return render_template('index.html', requests=jsons)


@app.get('/api/get')
def get_all_requests():
    """
    Server GET api response, query database

    :return: dict. an encapsulated dictionary with all render request serialized
    """
    rrequests = renderRequest.read_all()
    jsons = [rrequest.to_dict() for rrequest in rrequests]

    return {"results": jsons}


@app.get('/api/get/<uid>')
def get_request(uid):
    """
    Server GET api response for a specific uid request, query database

    :param uid: str. render request uid
    :return: dict. a render request serialized as dictionary
    """
    rr = renderRequest.RenderRequest.from_db(uid)
    return rr.to_dict()


@app.delete('/api/delete/<uid>')
def delete_request(uid):
    """
    Server DELETE api response, delete render request from database

    :param uid: str. render request uid
    """
    renderRequest.remove_db(uid)
    return {"deleted": uid}


@app.post('/api/post')
def create_request():
    """
    Server POST api response handling, with json data attached, creates
    a render request in database

    :return: dict. newly created render request serialized as dictionary
    """
    data = request.get_json(force=True)
    rrequest = renderRequest.RenderRequest.from_dict(data)
    rrequest.write_json()
    new_request_trigger(rrequest)

    return rrequest.to_dict()


@app.put('/api/put/<uid>')
def update_request(uid):
    """
    Server PUT api response handling, update render request in database

    :param uid: str. uid of render request to update
    :return: dict. updated render request serialized as dictionary
    """
    # unreal sends plain text
    content = request.data.decode('utf-8')
    LOGGER.debug('Received PUT update for UID %s with content: %s', uid, content)
    
    try:
        progress, time_estimate, status = content.split(';')
        progress = int(progress)
    except ValueError:
        LOGGER.error('Invalid update format for UID %s: %s', uid, content)
        return {"error": "Invalid format"}, 400

    rr = renderRequest.RenderRequest.from_db(uid)
    if not rr:
        LOGGER.error('RenderRequest UID %s not found for update', uid)
        return {"error": "RenderRequest not found"}, 404

    rr.update(
        progress=progress,
        time_estimate=time_estimate,
        status=status
    )
    LOGGER.debug('Updated RenderRequest UID %s to progress=%d, status=%s, time_estimate=%s',
                 uid, rr.progress, rr.status, rr.time_estimate)
    return rr.to_dict(), 200


# endregion


def new_request_trigger(rrequest):
    """
    Triggers when a client posts a new render request to the server
    """
    if rrequest.worker:
        LOGGER.debug('Request UID: %s already assigned to worker: %s', rrequest.uid, rrequest.worker)
        return

    # currently, as a test, assigns all job to one worker
    worker = 'RENDER_MACHINE_01'
    assign_request(rrequest, worker)

    LOGGER.info('Assigned job %s to %s', rrequest.uid, worker)
    
    # if multiple jobs came in at once, interval between each assignment
    time.sleep(4)
    LOGGER.info('assigned job %s to %s', rrequest.uid, worker)


def assign_request(rrequest, worker):
    """
    Assign render request to worker

    :param rrequest: renderRequest.RenderRequest. a render request object
    :param worker: str. worker name
    """
    rrequest.assign(worker)
    rrequest.update(status=renderRequest.RenderStatus.ready_to_start)


if __name__ == '__main__':
    import subprocess
    import os

    env = os.environ.copy()
    env['PYTHONPATH'] += os.pathsep + MODULE_PATH

    command = [
        FLASK_EXE,
        '--app',
        'requestManager.py',
        '--debug',  # debug mode to auto reload script changes
        'run',
        '-h',
        'localhost',
        '-p',
        '5000'
    ]

    proc = subprocess.Popen(command, env=env)
    LOGGER.info(proc.communicate())
