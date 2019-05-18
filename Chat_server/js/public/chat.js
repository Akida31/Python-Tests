//Make connection
var socket = io.connect('http://192.168.2.106:4000');

//Query DOM
var message = document.getElementById('message');
    handle = document.getElementById('handle');
    btn = document.getElementById('send');
    output = document.getElementById('output');
    feedback = document.getElementById('feedback');


function emit(){
  if (message.value.length > 0){
  socket.emit('chat',{
    message: message.value,
    handle: handle.value
  });
  message.value = '';}
}

//emit Events
btn.addEventListener('click', function(){
  emit();
});


message.addEventListener('keypress', function(){
  if (event.which == 13 || event.keyCode == 13) {
    emit();
  }
  else {
  socket.emit('typing', handle.value);
}
});

//Listen for Events
socket.on('chat',function(data){
  feedback.innerHTML = ''
  output.innerHTML += '<p><strong>' + data.handle + ': </strong>' + data.message + '</p>';
});

socket.on('typing', function(data){
  feedback.innerHTML = '<p><em>' + data + ' is typing a message...</em></p>';
});
