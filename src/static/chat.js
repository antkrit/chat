$(document).ready(function(){

    const socket = new WebSocket(wsUri);

    function scrollToBottom() {
        const msgContainer = $("#msg-container");
        msgContainer.scrollTop(msgContainer.prop("scrollHeight"));
    };

    scrollToBottom();

    function showMsg(msg, author = null) {
        const msgContainer = $("#msg-container");
        const msgElem = $("<div/>")
            .addClass("d-flex justify-content-start mb-4")
            .appendTo(msgContainer);
        const msgTextDiv = $("<div/>")
            .addClass("msg_cotainer_send")
            .appendTo(msgElem);
        const msgText = $("<p/>")
            .addClass("msg_body")
            .html(msg)
            .appendTo(msgTextDiv);

        console.log(msg);

        if(author) {
            const msgAuthor = $("<span/>")
                .addClass("author")
                .html(author)
                .appendTo(msgTextDiv);
            scrollToBottom();
        } else {
            msgTextDiv.addClass("system_msg");
        };
    };

    function sendMsg() {
        const msg = $("#msg-text");
        const msgTxt = msg.val().replace(/\s*$/,"");

        if ($.trim(msgTxt)) {
            socket.send(msgTxt);
        }

        msg.val("").focus();
    };

    socket.onopen = function() {
        showMsg("Connected.")
    };

    $("#send-btn").click(function() {
        sendMsg()
    });

    $("#msg-text").keypress(function(e) {
        if(!e.shiftKey && event.code === 'Enter') {
            sendMsg();
            e.preventDefault();
        }
    });

    socket.onmessage = function(e) {
        const data = JSON.parse(e.data);
        showMsg(data.body, data.author)
    };

    socket.onclose = function(event) {
        if(event.wasClean) {
            showMsg('Clean connection end.')
        } else {
            showMsg('Connection broken.')
        }
    };

    socket.onerror = function(error){
        showMsg(error)
    };
})