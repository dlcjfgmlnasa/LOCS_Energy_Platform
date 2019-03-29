# -*- coding:utf-8 -*-
# http://i5on9i.blogspot.com/2015/09/flask-blueprint.html
import os
from flask import Flask
from dotenv import load_dotenv
import app.module.power as power_module


APP_ROOT = os.path.join(os.path.dirname(__file__), '..')
env_path = os.path.join(APP_ROOT, '.env')
load_dotenv(env_path)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
app.register_blueprint(power_module.blueprint, url_prefix='/test')


@app.route('/')
def hello_world():
    return 'Hello World!'


if __name__ == '__main__':
    app.run(debug=True)
