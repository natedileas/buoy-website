from flask import Flask, request, render_template, redirect, \
    url_for, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from celery import Celery
import json

app = Flask(__name__)
CORS(app)
app.config.from_object('settings')

# Initialize Celery
celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf['CELERY_ACCEPT_CONTENT'] = ['json', 'pickle']
celery.conf.update(app.config)

db = SQLAlchemy(app)

# these are down here to avoid circular imports
import Task
import background_task


@app.route('/')
@app.route('/index')
def index():
    return redirect('http://localhost:3000', code=302)


@app.route('/new_task', methods=['POST'])
def new_task():
    print('request.data: ', request.data)
    info = json.loads(request.data.decode('UTF-8'))

    _task = background_task.apply_async((form, ))
    task = Task(_task)
    db.session.add(task)
    db.session.commit()


@app.route('/buoys', methods=['GET'])
def buoys():
    # print request.data
    # TODO make a real call: e.g.
    # metadata = buoycalib.landsat.parse_metadata(directory)
    # _ids = buoycalib.buoy.datasets_in_corners(metadata)
    # then do some display processing and serve that image
    print(request.args)
    scene_id = request.args['id']

    buoy_ids = ['45012', '45002']   # FIXME dummy data
    return jsonify(buoys=buoy_ids)


@app.route('/preview', methods=['POST'])
def preview():
    print('request.data: ', request.data)
    info = json.loads(request.data.decode('UTF-8'))
    image = info['thumbnail_url']   # i.e. keep it the same for now
    return jsonify(preview_image=image)


@app.route('/enum_tasks', methods=['GET'])
def enum_tasks():
    # FIXME dummy data
    return jsonify(jobs=[{"id": "job1"}, {"id": "job2"}, {"id": "job3"}])
    """
    tasks = Task.query.all()
    task_list = [{'task_id': str(t.task_id), 'scene_id': str(t.scene_id)} for t in tasks]

    return jsonify(tasks=task_list)
    """

@app.route('/status/<task_id>', methods=['GET'])
def taskstatus(task_id):
    # FIXME dummy data
    return jsonify(job_status=task_id+"1")
    """
    task = download.AsyncResult(task_id)
    if task.state == 'PENDING':
        response = {
            'state': task.state,
            'current': 0,
            'total': 1,
            'status': 'Pending...'
        }
    elif task.state != 'FAILURE':
        response = {
            'state': task.state,
            'current': task.info.get('current'),
            'total': task.info.get('total'),
            'status': task.info.get('status')
        }
        if 'result' in task.info:
            response['result'] = task.info['result']
    else:
        # something went wrong in the background job
        response = {
            'state': task.state,
            'current': 1,
            'total': 1,
            'status': str(task.info),  # this is the exception raised
        }
    return jsonify(response)
    """


if __name__ == '__main__':
    app.run(host='localhost', port=5000, debug=True)
