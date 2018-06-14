from flask import Flask, render_template
from flask_socketio import SocketIO, emit

# from .tweetstream import listener
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy.streaming import StreamListener

from threading import Thread

import time, json

# elements required for Twitter API usage
# consumer key, consumer secret, access token, access secret.
ckey = "Es3lDZ9L6ukHRUl1ya5uOTPtx"
csecret = "4UmLc6z65P9Z7nveZnBKssKEnPV71svogCwvhnKaIvM44syi5B"
atoken = "370737927-rr0xbO21qRS92QgCLqvU9qg1FDqic6vuWTlncT0x"
asecret = "ql8fXdZ4acRTDNAi4aZHq1OefpIz6qt8eTXQdj0s79IWK"

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
			socketio.emit('show', {'username': username, 'text': text})
		except KeyError:
			pass
	
	def on_error(self, status):
		print (status)

def background_thread():

	print ('Background stuff activated!')

	twitterStream = Stream(auth, listener())
	twitterStream.filter(track=['και'])
	#while True:
	#	time.sleep(1)
	#	twitterStream = Stream(auth, listener())
	#	twitterStream.filter(track=['και'])

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
	print ('Client connected!')

@socketio.on('enable stream', namespace='/')
def enable():
	global tweetThread
	if tweetThread is None:
		# Some threads do background tasks, like sending keepalive packets, or performing periodic garbage collection
		# or whatever. These are only useful when the main program is running
		# and it's okay to kill them off once the other, non-daemon, threads have exited.
		tweetThread = Thread(target=background_thread, daemon=True)
		tweetThread.start()

if __name__ == '__main__':
	socketio.run(app, debug=True)