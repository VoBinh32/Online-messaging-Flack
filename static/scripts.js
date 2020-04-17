document.addEventListener('DOMContentLoaded', () => {

    var socket = io.connect(location.protocol + '//' + document.domain + ':' + location.port);
    socket.on('connect', () => {

        socket.emit('joined');

        document.querySelector('#newchannel').addEventListener('click', () => {
            localStorage.removeItem('last_channel');
        });

        document.querySelector('#leave').addEventListener('click', () => {
            socket.emit('left');
            localStorage.removeItem('last_channel');
            window.location.replace('/');
        });

        document.querySelector('#logout').addEventListener('click', ( => {
            localStorage.removeItem('last_channel');
        }));

        document.querySelector('#comment').addEventListener("keydown", event => {
            if (event.key == "Enter") {
                document.querySelector('send.button').click();
            }
        });

        document.querySelector('#send-button').addEventListener('click', () => {
            let timestamp = new Date;
            timestamp = timestamp.toLocaleTimeString();

            let msg = document.querySelector('#comment').value;

            socket.emit('send messages', msg, timestamp);

            document.querySelector('#comment').value = '';
        });
    });


}
)