$(document).ready(function(){

	// start up the SocketIO connection to the server - the namespace 'test' is also included here if necessary
	var socket = io.connect('http://' + document.domain + ':' + location.port + '/');
	var userArray = [];
	var tweetArray = [];
	// user must firstly train the model; use flag instead of local storage so every time user
	// refreshes the page training session has to be repeated
	var flag = false;

	$("#1").on("click", function() {
		if (flag == true) {
			socket.emit('enable stream')
		}
	});

	$("#3").on("click", function() {
		socket.emit('train classifier');
		flag = true
	});

	socket.on('tweet display', function(msg) {
		// length is defined for better code performance. Check 'https://www.w3schools.com/js/js_performance.asp'
		var length = tweetArray.length;

		if (length >= 10) {
			userArray.shift();
			tweetArray.shift();
		}

		userArray.push(msg.username);
		tweetArray.push(msg.text);

		var tweetsHTMLTable = '';

		for (var i = 0; i < length; i++) {
			tweetsHTMLTable += '<tr><td>' + userArray[i] + '</td><td>'  + tweetArray[i] + '</td></tr>'
		}
		$('#2').html(tweetsHTMLTable);
	});
});