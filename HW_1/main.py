from flask import Flask
from markupsafe import escape
app = Flask(__name__)

@app.route('/')
def index():
    return 'Hello, Flask!'

@app.route('/user/<string:name>')
def user(name):
    return f'Hello, {escape(name)}!'


if __name__ == '__main__':
    app.run()
