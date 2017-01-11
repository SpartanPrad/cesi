from flask import Flask, render_template, url_for, redirect, jsonify, request, g, session, flash
from cesi import Config, Connection, Node, CONFIG_FILE, ProcessInfo, JsonValue
import sqlite3
import interceptor

app = Flask(__name__)
app.wsgi_app = interceptor.Interceptor(app.wsgi_app)
app.config.from_object(__name__)
app.secret_key= '42'


DATABASE = Config(CONFIG_FILE).getDatabase()
ACTIVITY_LOG = Config(CONFIG_FILE).getActivityLog()
HOST = Config(CONFIG_FILE).getHost()


# Database connection
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db


# Close database connection
@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404


@app.route("/denial")
def denial():
    res=jsonify(error_message="token_invalid")
    res._status='403'
    res._status_code = 403
    return res

@app.route("/token_expire")
def token_expire():
    res=jsonify(error_message="token_expire")
    res._status='401'
    res._status_code = 401
    return res

