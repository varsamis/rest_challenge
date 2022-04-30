"""
Chalenge restfull API
"""

from bottle import Bottle, abort, run, request
from db_wrapper import Model, Report
import helpers
from threading import Thread
from datetime import datetime, timezone
from uuid import uuid4
import os
import json


DB_NAME = 'db/rest_challenge.db'

app = Bottle()
Model.init_db(DB_NAME)

@app.route('/')
def report():
    return 'hi there'

@app.route('/report')
def report():
    pass


@app.get('/report/new')
def get_new_report():
    return '''<form action="/report/new" method="post" enctype="multipart/form-data">
            Category:      <input type="text" name="category" />
            Select a file: <input type="file" name="upload" />
            <input type="submit" value="Start upload" />
            </form>
            '''

@app.post('/report/new')
def post_new_report():
    category   = request.forms.get('category')
    upload     = request.files.get('upload')
    file_name, ext = os.path.splitext(upload.filename)
    if ext not in ('.json','.csv'):
        abort(415, 'Unsupported Media Type')

    new_report = Report(path=f'{file_name}{ext}', name=file_name)
    new_report.save()
    new_thread = Thread(target=helpers.process_file, args=[file_name, ext])
    new_thread.start() 


### Collections ##

@app.route('/reports')
def reports():
    cur =  db.connection.cursor()
    cur.execute('SELECT * FROM reports')
    return json.dumps(cur.fetchall())
    
    

run(app, host='localhost', port=8000)
