from flask import Flask, render_template
from flask_socketio import SocketIO, emit

from tweepy import OAuthHandler
from tweepy import Stream
from tweepy.streaming import StreamListener

from .classifier import Classifier

from threading import Thread

import json

# elements required for Twitter API usage
# consumer key, consumer secret, access token, access secret.
ckey = ""
csecret = ""
atoken = ""
asecret = ""

auth = OAuthHandler(ckey, csecret)
auth.set_access_token(atoken, asecret)

# Set this variable to "threading", "eventlet" or "gevent" to test the
# different async modes, or leave it set to None for the application to choose
# the best option based on installed packages.
async_mode = None

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, async_mode=async_mode)

tweetThread = None

class Listener(StreamListener):

	def on_data(self, data):

		# transforms string to dictionary
		tweet_dict = json.loads(data)
		# we use the exception utility because of the occasional tweet that fails in the stream
		try:
			# store tweet's user
			username = tweet_dict["user"]["screen_name"]
			# store tweet's text
			text = tweet_dict["text"]
			# removes all newline characters from tweet's text
			text = text.replace('\n', '')
			socketio.emit('tweet display', {'username': username, 'text': text})
		except KeyError:
			pass
	
	def on_error(self, status):
		print (status)

def background_thread():

	print ('Background stuff activated!')

	twitterStream = Stream(auth, listener())
	twitterStream.filter(track=['nba'])

@app.route('/')
def index():
	return render_template('index.html')

@socketio.on('connect', namespace='/')
def on_connect():
	print ('Client connected!')

@socketio.on('enable stream', namespace='/')
def on_enable():
	global tweetThread
	if tweetThread is None:
		# Some threads do background tasks, like sending keepalive packets, or performing periodic garbage collection
		# or whatever. These are only useful when the main program is running
		# and it's okay to kill them off once the other, non-daemon, threads have exited.
		tweetThread = Thread(target=background_thread, daemon=True)
		tweetThread.start()

@socketio.on('train classifier', namespace='/')
def on_train():
	c = Classifier()
	c.train()
	print (c.train_attributes['features'][725])
	print (c.train_attributes['target'][725])

@socketio.on('disconnect', namespace='/')
def on_disconnect():
	print('Client disconnected')

if __name__ == '__main__':
	socketio.run(app, debug=True)