from flask import Flask

from .controllers.controller import controller


app = Flask(__name__)

app.register_blueprint(controller)

app.secret_key = 'very secret1'

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html')