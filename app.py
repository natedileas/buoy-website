import pickle
import json

from celery import Celery
from flask import Flask, request, render_template, redirect, \
    url_for, jsonify
from flask_cors import CORS
import redis

import settings
import buoycalib

app = Flask(__name__)
app.config.from_object('settings')
CORS(app)   # something something cross-origin request security

# get database reference
_redis = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT,
                           db=settings.REDIS_DB)

# Initialize Celery
celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf['CELERY_ACCEPT_CONTENT'] = ['pickle']
celery.conf['CELERY_TASK_SERIALIZER'] = 'pickle'
celery.conf.update(app.config)

# these are down here to avoid circular imports, TODO fix
import background_task


@app.route('/')
@app.route('/index')
def index():
    return redirect('http://{0}:{1}'.format(settings.APP_HOST, settings.APP_PORT), code=302)


@app.route('/new_task', methods=['POST'])
def new_task():
    print('newtask request.data: ', request.data)
    info = json.loads(request.data.decode('UTF-8'))

    _task = background_task.background_task.apply_async((info, ))

    return 'OK'   # fixes ValueError: View function did not return a response


@app.route('/buoys', methods=['GET'])
def buoys():
    """ get buoys in WRS2 path and row """
    scene_id = request.args['id']
    path = int(scene_id[3:6])
    row = int(scene_id[6:9])

    corners = buoycalib.wrs2.wrs2_to_corners(path, row)
    buoys = buoycalib.buoy.datasets_in_corners(corners)
    buoy_ids = buoys.keys()
    
    return jsonify(buoys=buoy_ids)


@app.route('/preview', methods=['POST'])
def preview():
    # FIXME dummy data
    print('request.data: ', request.data)
    info = json.loads(request.data.decode('UTF-8'))
    image = info['thumbnail_url']   # i.e. keep it the same for now
    return jsonify(preview_image=image)


@app.route('/enum_tasks', methods=['GET'])
def enum_tasks():
    # FIXME dummy data
    #return jsonify(jobs=[{"id": "job1"}, {"id": "job2"}, {"id": "job3"}])
    print(_redis.keys())

    task_keys = _redis.keys('celery-task-meta-*')
    task_ids = [{"id": t.decode("UTF-8").replace('celery-task-meta-','')} for t in task_keys]

    return jsonify(jobs=task_ids)


@app.route('/status/<task_id>', methods=['GET'])
def taskstatus(task_id):
    # FIXME dummy data
    #return jsonify(job_status=task_id+"1")

    task = background_task.background_task.AsyncResult(task_id)
    response = {'state': task.state}

    if task.state == 'DONE':
        response.update({
            'return': task.info.get('return')
        })
    elif task.state == 'INPROGRESS':
        response.update({
            'message': task.info.get('message', '')
        })
    else:
        # something went wrong in the background job
        response.update({
            'message': str(task.info),  # this is the exception raised
        })
    return jsonify(response)


if __name__ == '__main__':
    app.run(host=settings.APP_HOST, port=settings.APP_PORT, debug=True)
