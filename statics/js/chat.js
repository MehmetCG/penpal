$(document).ready(function(){
    function scrollToBottom (id) {
        var div = document.getElementById(id);
        if (div){
          div.scrollTop = div.scrollHeight - div.clientHeight};
    }

    window.autoGrow = function autoGrow(element) {
        element.style.height = "5px";
        element.style.height = (element.scrollHeight)+"px";
    }
    
    scrollToBottom("messages")
    
    function appendMessage(message, type) {     
        $("#chats").append(
            '<li class="'+ type +'"><div class="img-block"><img src="'
            + message.image +'" alt="" /></div><div class="msgbox"><p>'
            + message.text +'</p><small class="timeBlock">'
            + message.created_at +'</small></div></li>'
        )
    }

    const userID = JSON.parse(document.getElementById('user_id').textContent);
    const toUserID = JSON.parse(document.getElementById('to_user_id').textContent);
    const minID = Math.min(userID,toUserID).toString();
    const maxID = Math.max(userID,toUserID).toString();
    const roomName = minID.concat("-", maxID) // special room name for each chat 8-12

    const chatSocket = new WebSocket(
        'ws://'
        + window.location.host
        + '/ws/chat/'
        + roomName
    );

    chatSocket.onmessage = function(e) {
        const data = JSON.parse(e.data);
        if (data.sender == userID){
            appendMessage(data, "replies");
        }else{
            appendMessage(data, "sent");
        }
        $("#contact"+toUserID).prependTo("#chatedPeople");
        $("#latest"+toUserID).text(data.text);
        scrollToBottom("messages")
    };

    chatSocket.onclose = function(e) {
        console.error('Chat socket closed unexpectedly');
    };

    document.querySelector('#messageText').focus();
    document.querySelector('#messageText').onkeyup = function(e) {
        if (e.keyCode === 13) {  // enter, return
            document.querySelector('#sendButton').click();
        }
    };

    $("#messageBox").submit(function(e) {
        e.preventDefault(); 
        const messageInputDom = document.querySelector('#messageText');
        const text = messageInputDom.value;
        chatSocket.send(JSON.stringify({
            'text': text,
            'sender': userID,
            'recipient': toUserID
        }));
        $("#messageBox").trigger('reset');
    });
})
