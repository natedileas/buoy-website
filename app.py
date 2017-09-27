import pickle
import json

from celery import Celery
from flask import Flask, request, render_template, redirect, \
    url_for, jsonify, send_file
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
import calib_task

@app.route('/')
@app.route('/index')
def index():
    return redirect('http://{0}:{1}'.format(settings.APP_HOST, settings.APP_PORT), code=302)


@app.route('/new_task', methods=['POST'])
def new_task():
    print('newtask request.data: ', request.data)

    info = json.loads(request.data.decode('UTF-8'))
    calib_task.calib_task.apply_async((info, ))

    return 'OK'   # fixes ValueError: View function did not return a response


@app.route('/buoys', methods=['GET'])
def buoys():
    """ get buoys in WRS2 path and row """
    scene_id = request.args['id']
    path = int(scene_id[3:6])
    row = int(scene_id[6:9])

    corners = buoycalib.wrs2.wrs2_to_corners(path, row)
    buoys = buoycalib.buoy.datasets_in_corners(corners)
    buoy_ids = list(buoys.keys())

    return jsonify(buoys=buoy_ids)


@app.route('/preview', methods=['POST'])
def preview():
    print('request.data: ', request.data)
    info = json.loads(request.data.decode('UTF-8'))
    image = info['thumbnail_url']

    scene_id = info['scene_id']
    path = int(scene_id[3:6])
    row = int(scene_id[6:9])

    corners = buoycalib.wrs2.wrs2_to_corners(path, row)
    buoys = buoycalib.buoy.datasets_in_corners(corners)
    buoy_ids = list(buoys.keys())

    if buoy_ids:

        ds = buoycalib.buoy.all_datasets()
        loc = [ds[b][1:3] for b in buoy_ids]

        image_str = buoycalib.display.draw_latlon(image, corners, text=buoy_ids, loc=loc)

        return jsonify(preview_image=image_str)

    else:
        return jsonify(preview_image=image)


@app.route('/enum_tasks', methods=['GET'])
def enum_tasks():
    task_keys = _redis.keys('celery-task-meta-*')
    task_ids = [{"id": t.decode("UTF-8").replace('celery-task-meta-','')} for t in task_keys]

    return jsonify(jobs=task_ids)


@app.route('/images/<img_file>')
def images(img_file):
    print(img_file)
    return send_file('.\\images\\'+img_file, attachment_filename=img_file,
                     mimetype='image/png')


@app.route('/status/<task_id>', methods=['GET'])
def taskstatus(task_id):

    task = calib_task.calib_task.AsyncResult(task_id)
    #print (dir(task))
    response = {'state': task.state}

    if type(task.info) is dict:
        response.update({
                'config': task.info.get('config', {}),
                'message': task.info.get('message', ''),
                'return': task.info.get('return', {})
                })
    else:
        response['message'] = str(task.info)

    return jsonify(response)


if __name__ == '__main__':
    app.run(host=settings.APP_HOST, port=settings.APP_PORT, debug=True)
