from flask import Flask

flask_application = Flask(__name__)

@flask_application.route("/")
def index():
    return "Hello world!"
