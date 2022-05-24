$(document).ready(function(){
    
    function increaseAlert(sender){
        var counter = parseInt($("#alert"+sender).text());
        $("#alert"+sender).html(counter + 1);
        $("#alert"+sender).show();
    }

    const userID = JSON.parse(document.getElementById('user_id').textContent);

    const chatSocket = new WebSocket(
        'ws://'
        + window.location.host
        + '/ws/public/'
        + user
    );

    chatSocket.onmessage = function(e) {
        const data = JSON.parse(e.data);
        if (data.sender == userID){
            appendMessage(data, "replies");
        }else{
            appendMessage(data, "sent");
            increaseAlert(data.sender);
        }
        $("#contact"+toUserID).prependTo("#chatedPeople");
        $("#latest"+toUserID).text(data.text);
    };

    chatSocket.onclose = function(e) {
        console.error('Chat socket closed unexpectedly');
    };

})
