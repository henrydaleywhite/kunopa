from flask import Flask, render_template

from .controllers.controller import controller

UPLOADS_FOLDER = '/mnt/c/Users/Henry/desktop/byte/week6/ipfs_testing/new_test/run/src/static'

app = Flask(__name__, static_folder = 'static')

app.register_blueprint(controller)

app.config['UPLOAD_FOLDER'] = UPLOADS_FOLDER
app.secret_key = 'very secret1'

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html')