const ws = new WebSocket('ws://localhost:8080');
const formChat = document.getElementById('formChat');
const textField = document.getElementById('textField');
const subscribe = document.getElementById('subscribe');

formChat.addEventListener('submit', (e) => {
    e.preventDefault();
    ws.send(textField.value);
    textField.value = '';
});

ws.onopen = (e) => {
    console.log('WebSocket connection is open!');
};

ws.onmessage = (e) => {
    console.log(e.data);
    const elMsg = document.createElement('div');
    elMsg.innerHTML = e.data.replace(/\n/g, '<br>');
    subscribe.appendChild(elMsg);
};

ws.onclose = (e) => {
    console.log('WebSocket connection closed!');
};
