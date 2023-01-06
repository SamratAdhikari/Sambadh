document.addEventListener('DOMContentLoaded', ()=>{


    // ---------------Connect to websocket-----------------
    var socket = io.connect('http://' + document.domain + ':' + location.port);


    // Variable
    let room = 'Global';
    joinRoom(room);


    // ------------------Event Bucket Listeners--------------------

    // Display incoming messages
    socket.on('message', data=>{

        if (data.msg){
            
            const p = document.createElement('p');
            const span_username = document.createElement('span');
            const span_timestamp = document.createElement('span');
            const br = document.createElement('br');
            
            if (data.username == username){
                // p.setAttribute('class', 'my-msg');
                p.classList.add("my-input");
                p.setAttribute('id', 'input-background');

                span_username.classList.add('username');
                span_username.innerText = data.username;

                span_timestamp.classList.add('timestamp');
                span_timestamp.innerText = data.time_stamp;

                p.innerHTML += span_username.outerHTML + br.outerHTML + data.msg + br.outerHTML + span_timestamp.outerHTML;
                document.querySelector('.display-message-section').append(p);
            }

            else if (typeof data.username !== 'undefined'){
                p.classList.add("other-input");

                span_username.classList.add('username');
                span_username.innerText = data.username;

                span_timestamp.classList.add('timestamp');
                span_timestamp.innerText = data.time_stamp;

                p.innerHTML += span_username.outerHTML + br.outerHTML + data.msg + br.outerHTML + span_timestamp.outerHTML;

                document.querySelector('.display-message-section').append(p);

            }

            else{
                printSysMsg(data.msg);
            }

            scrollDownChatWindow();
        
    }

    });


    // ----------------Evenet bucket for SEND------------------------
    document.querySelector('#send-message').onclick = ()=>{
        let msg = document.querySelector('#user-message').value;

        socket.send({'msg': msg, 'username': username, 'room': room});
        // Clear input area
        document.querySelector('#user-message').value = '';
    }


    // ------------------Room Selection---------------------------
    document.querySelectorAll('.select-room').forEach(p => {
        p.onclick = () => {
            let newRoom = p.innerHTML;

            if (newRoom == room){
                msg = `You are already in ${room} room.`;
                printSysMsg(msg);
            }

            else if (newRoom != room){
                leaveRoom(room);
                joinRoom(newRoom);
                room = newRoom;
            }
        }
    });


    // ---------------Logout-------------
    // Logout from chat
    document.querySelector("#logout-btn").onclick = () => {
        leaveRoom(room);
    };


    // ---------------Functions----------------------------
    // Leave Room
    function leaveRoom(room){
        socket.emit('leave', {'username': username, 'room': room});
    }


    // Join Room
    function joinRoom(room){
        socket.emit('join', {'username': username, 'room': room});
        // Clear message area
        document.querySelector('.display-message-section').innerHTML = '';
        // Auto focus on input box
        // document.querySelector('#user-message').focus();
    }


    // Print System Messages
    function printSysMsg(msg){
        const div = document.createElement('p');
        div.classList.add("system-msg");
        div.innerHTML = msg;
        document.querySelector('.display-message-section').append(div);
        scrollDownChatWindow()

    }

    // Scroll chat window down
    function scrollDownChatWindow() {
        const chatWindow = document.querySelector(".display-message-section");
        chatWindow.scrollTop = chatWindow.scrollHeight;
    }



});