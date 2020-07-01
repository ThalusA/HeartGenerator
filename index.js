const WebSocket = require('ws');

const wss = new WebSocket.Server({ port: 9969 });

wss.on('connection', function connection(ws) {
  console.log('Connected');
  ws.on('message', function incoming(message) {
    console.log('received: %s', message);
  });

  ws.send('something');
});
