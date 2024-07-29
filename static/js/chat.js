function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
const csrftoken = getCookie('csrftoken');

function deleteMessage(messageId) {
    fetch(`/delete_message/${messageId}/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrftoken,
        },
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            location.reload();
        } else {
            alert('Failed to delete messages');
        }
    });
}

function deleteChatRoom(roomId) {
    fetch(`/delete_chat_room/${roomId}/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrftoken,
        },
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            location.reload();
        } else {
            alert('Failed to delete chat room');
        }
    });
}

function sendMessage(roomId, content, file) {
    const formData = new FormData();
    formData.append('action', 'send_message');
    formData.append('content', content);
    if (file) {
        formData.append('file', file);
    }

    fetch(`/chat_room/${roomId}/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrftoken,
        },
        body: formData,
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            location.reload();
        } else {
            alert('Failed to send message');
        }
    });
}
