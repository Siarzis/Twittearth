from flask import Flask, render_template
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

# The routes are the different URLs that the application implements
# In Flask, handlers for the application routes are
# written as Python functions, called view functions
# View functions are mapped to one or more route URLs
# so that Flask knows what logic to execute when a client requests a given URL

# The operation that converts a template into a complete HTML page is called rendering
# render_template() takes a template filename
# and a variable list of template arguments and returns the same template,
# but with all the placeholders in it replaced with actual values

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('connect')
def on_connect():
    print('Client connected')
    emit('show', {'data': 'Siarzis has joined'})

if __name__ == '__main__':
    socketio.run(app, debug=True)