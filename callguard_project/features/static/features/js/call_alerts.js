const socket = new WebSocket('ws://' + window.location.host + '/ws/call/');

socket.onmessage = function(e) {
    const data = JSON.parse(e.data);
    if (data.type === 'alert') {
        alert('Spam Alert: ' + data.message);
    } else {
        console.log('Message: ', data.message, 'Is Spam: ', data.is_spam);
    }
};

socket.onopen = function(e) {
    console.log('Connection established');
};

socket.onclose = function(e) {
    console.error('Chat socket closed unexpectedly');
};
