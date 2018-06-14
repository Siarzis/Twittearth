$(document).ready(function(){

	// start up the SocketIO connection to the server - the namespace 'test' is also included here if necessary
	var socket = io.connect('http://' + document.domain + ':' + location.port + '/');

	$("#1").on("click", function() {
	    socket.emit('enable stream');
	});

	socket.on('show', function(msg) {
		console.log('Hello world!');
		// $('#2').append('<li class="list-group-item">User: ' + msg.username + ',' + 'Tweet: ' + msg.text + '</li>');
		$('#2').append('<tr><td>' + msg.username + '</td><td>'  + msg.text + '</td></tr>');
	});
});