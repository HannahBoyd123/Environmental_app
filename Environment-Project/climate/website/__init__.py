from flask import Flask, Blueprint

from login_sign_up import login_sign_up
from index import index
from pollution_and_weather_links import pollution_and_weather_links


def create_app():
    app = Flask(__name__)
    app.secret_key = '&Potato98&'
    app.register_blueprint(login_sign_up)
    app.register_blueprint(index)
    app.register_blueprint(pollution_and_weather_links)
    return app


if __name__ == '__main__':
    create_app().run(debug=True)