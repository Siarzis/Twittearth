// Basic syntax is: $(selector).action()
// A $ sign to define/access jQuery
// A (selector) to "query (or find)" HTML elements
// A jQuery action() to be performed on the element(s)

// "$(document).ready" is to prevent any jQuery code from running before the document is finished loading (is ready).
// It is good practice to wait for the document to be fully loaded and ready before working with it.
// This also allows you to have your JavaScript code before the body of your document, in the head section.

// Here are some examples of actions that can fail if methods are run before the document is fully loaded:
// 1. Trying to hide an element that is not created yet
// 2. Trying to get the size of an image that is not loaded yet
$(document).ready(function(){

    // start up the SocketIO connection to the server - the namespace 'test' is also included here if necessary
    var socket = io.connect('http://' + document.domain + ':' + location.port + '/');
    
    // this is a callback that triggers when the "my response" event is emitted by the server.

    // The on() method attaches one or more event handlers for the selected elements.
    // For example, attach a click event to a <p> element:
    // $("p").on("click", function(){
    //     $(this).hide();
    // });
    socket.on('show', function(msg) {
        console.log('Hello world!');
        // The jQuery #id selector uses the id attribute of an HTML tag to find the specific element.
        // An id should be unique within a page, so you should use the #id selector when you want to find a single, unique element.
        // To find an element with a specific id, write a hash character, followed by the id of the HTML element:
        //$('#log').append('&lt;p&gt;Received: ' + msg.data + '&lt;/p&gt;');
        $('#2').append('<p>Received: ' + msg.data + '</p>');
    });
});