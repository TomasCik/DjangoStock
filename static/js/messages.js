// /static/js/messages.js
document.addEventListener("DOMContentLoaded", function() {
    setTimeout(function() {
        var messageContainer = document.getElementById("message-container");
        if (messageContainer) {
            messageContainer.innerHTML = "";
        }
    }, 2000);
});
