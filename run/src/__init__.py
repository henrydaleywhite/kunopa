from flask import Flask,render_template,request

from .controllers import controller


app = Flask(__name__)

middleware.register_blueprint(controller)


@middleware.errorhandler(404)
def not_found(error):
    return render_template('404.html')