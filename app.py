from flask import Flask, request, render_template, redirect, \
    url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from celery import Celery


app = Flask(__name__)
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
    form = request.form
    print(form)

    _task = background_task.apply_async((form, ))
    task = Task(_task)
    db.session.add(task)
    db.session.commit()


@app.route('/buoy_ids', methods=['GET'])
def buoy_ids():
    # print request.data
    # TODO make a real call: e.g.
    # metadata = buoycalib.landsat.parse_metadata(directory)
    # _ids = buoycalib.buoy.datasets_in_corners(metadata)
    # then do some display processing and serve that image

    _ids = [('buoy1', '45012'), ('buoy2', '45002')]   # FIXME dummy data
    return jsonify(ids=_ids)


@app.route('/enum_tasks', methods=['GET'])
def enum_tasks():
    tasks = Task.query.all()
    task_list = [{'task_id': str(t.task_id), 'scene_id': str(t.scene_id)} for t in tasks]

    return jsonify(tasks=task_list)


@app.route('/status/<task_id>')
def taskstatus(task_id):
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


if __name__ == '__main__':
    app.run(host='localhost', port=5000, debug=True)
