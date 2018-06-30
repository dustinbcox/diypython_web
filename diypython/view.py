from . import app
from flask import render_template, redirect, abort, request
from .model import HttpLog, db
from datetime import datetime

def create_http_log(status):
    """Create an HttpLog row"""
    return HttpLog(
        date = datetime.now(),
        ip = request.environ.get('HTTP_X_REAL_IP', request.remote_addr),
        referrer = request.referrer,
        verb = request.method,
        path = request.path,
        status = status)

def log_request(status):
    db.session.add(create_http_log(status))
    db.session.commit()



@app.route('/')
def index():
    log_request(200)
    return render_template("index.html")

@app.route('/class')
@app.route('/class/<date>')
def class_page(date = None):
    log_request(200)
    return render_template("class.html")

@app.route('/page/<name>')
def page(name):
    log_request(200)
    return render_template("page.html")


@app.errorhandler(404)
def error_404(error):
    log_request(404)
    return render_template('404.html'), 404
