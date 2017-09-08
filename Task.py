from app import db

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task_id = db.Column(db.String(120), unique=True)
    email = db.Column(db.String(120))
    scene_id = db.Column(db.String(120))
    buoy_id = db.Column(db.String(120))
    atmo_source = db.Column(db.String(12))

    def __init__(self, form):
        self.email = form['email']
        self.task_id = form['task_id']
        self.scene_id = form['scene_id']
        self.buoy_id = form['buoy_id']
        self.atmo_source = form['atmo_source']

    def __repr__(self):
        return '<Scene ID: {0} Buoy ID: {1}>'.format(self.scene_id, self.buoy_id)
