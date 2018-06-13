from flask import Flask, render_template
from flask_socketio import SocketIO, emit

# from .tweetstream import listener
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy.streaming import StreamListener

from threading import Thread

import time
import json

# elements required for Twitter API usage
# consumer key, consumer secret, access token, access secret.
ckey = ""
csecret = ""
atoken = ""
asecret = ""

auth = OAuthHandler(ckey, csecret)
auth.set_access_token(atoken, asecret)

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

tweetThread = None

class listener(StreamListener):

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
			print ('karana')
			socketio.emit('show', {'username': username, 'text': text})
			print ('gemen')
		except KeyError:
			pass
	
	def on_error(self, status):
		print (status)

def background_thread():

	print ('Background Stuff')
	while True:
		time.sleep(1)
		t = str(time.clock())
		twitterStream = Stream(auth, listener())
		twitterStream.filter(track=['και'])

# The routes are the different URLs that the application implements
# In Flask, handlers for the application routes are written as Python functions, called view functions
# View functions are mapped to one or more route URLs
# so that Flask knows what logic to execute when a client requests a given URL

# The operation that converts a template into a complete HTML page is called rendering
# render_template() takes a template filename
# and a variable list of template arguments and returns the same template,
# but with all the placeholders in it replaced with actual values

@app.route('/')
def index():
	return render_template('index.html')

@socketio.on('connect', namespace='/')
def on_connect():
	global tweetThread
	print ('Client connected!')
	# emit('show', {'data': 'Siarzis has joined'})
	#username = 'Siarzis'
	#text = 'Flask Socket Project'
	#emit('show', {'username': username, 'text': text})
	#twitterStream = Stream(auth, listener())
	#twitterStream.filter(track=['και'])
	if tweetThread is None:
		tweetThread = Thread(target=background_thread)
		tweetThread.start()

if __name__ == '__main__':
	socketio.run(app, debug=True)