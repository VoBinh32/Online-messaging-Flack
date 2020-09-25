document.addEventListener('DOMContentLoaded', () => {
    // Connect to websocket
    var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);
    // When connected, configure button
    socket.on('connect', () => {
        // Notify joined event.
        socket.emit('joined');

        // when user click +channel, remove the local storage
        document.querySelector('#newchannel').addEventListener('click', () => {
            localStorage.removeItem('last_channel');
        });
        // when user leave the channel, then send a notification and remove local storage
        document.querySelector('#leave').addEventListener('click', () => {

            socket.emit('left');

            localStorage.removeItem('last_channel');
            window.location.replace('/');
        });

        // When user logout, also remove local storage
        document.querySelector('#logout').addEventListener('click', () => {
            localStorage.removeItem('last_channel');
        });

        //if the user press 'Enter' = clicking the send button
        document.querySelector('#comment').addEventListener("keydown", event => {
            if (event.key == "Enter") {
                document.getElementById("send-button").click();
            }
        });

        //The send button emits a "send message" event
        document.querySelector('#send-button').addEventListener("click", () => {
            // save the timestamp
            let timestamp = new Date;
            timestamp = timestamp.toLocaleTimeString();
            // save the content of message
            let msg = document.getElementById("comment").value;

            socket.emit('send message', msg, timestamp);
            // after sending a message, clear the message field
            document.getElementById("comment").value = '';
        });
    });

    //  Broadcast the message
    socket.on('status', data => {

        let row = `${data.msg}`
        document.querySelector('#chat').value += row + '\n';
        // Save the user's current channel on localStorage
        localStorage.setItem('last_channel', data.channel)
    });

    socket.on('announce message', data => {

        let row = '<' + `${data.timestamp}` + '> - ' + '[' + `${data.user}` + ']:  ' + `${data.msg}`
        document.querySelector('#chat').value += row + '\n'
    });
});