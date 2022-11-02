$(document).ready(function() {
    var socket = io();

    socket.on('connect', function() {
        socket.emit('my_event', {data: 'I\'m connected!'});
    });

    socket.on('my_response', function(msg, cb) {
        $('#log').append('<br>' + $('<div/>').text('Received #' + msg.count + ': ' + msg.data).html());
        if (cb)
            cb();
    });

    socket.on('test_response', function(msg) {
        $('#log').append('<br>' + $('<div/>').text(msg.data).html());
    })

    socket.on('broadcast_response', function(msg) {
        $('#log').append('<br>' + $('<div/>').text(msg.data).html());
    })

    $('form#test').submit(function(event) {
        socket.emit('test_message', {data: 'Test message sent'});
        return false;
    });
    $('form#broadcast').submit(function(event) {
        socket.emit('broadcast_message', {data: 'broadcast triggered'});
        return false;
    });
});