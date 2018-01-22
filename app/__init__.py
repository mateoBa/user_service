from flask import Flask

app = Flask(__name__)
app.config['MONGOALCHEMY_DATABASE'] = 'users'
app.config['MONGOALCHEMY_CONNECTION_STRING'] = 'mongodb://127.0.0.1:27017/users'

from app import api
