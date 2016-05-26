  function init()
  {
    document.myform.url.value = "ws://trioelm.com:4248/"
    document.myform.inputtext.value = "1"
    document.myform.disconnectButton.disabled = true;
  }

  function doConnect()
  {
    websocket = new WebSocket(document.myform.url.value, ['vote']);
    websocket.onopen = function(evt) { onOpen(evt) };
    websocket.onclose = function(evt) { onClose(evt) };
    websocket.onmessage = function(evt) { onMessage(evt) };
    websocket.onerror = function(evt) { onError(evt) };
  }

  function onOpen(evt)
  {
    writeToScreen("connected\n");
    document.myform.connectButton.disabled = true;
    document.myform.disconnectButton.disabled = false;
  }

  function onClose(evt)
  {
    writeToScreen("disconnected\n");
    document.myform.connectButton.disabled = false;
    document.myform.disconnectButton.disabled = true;
  }

  function onMessage(evt)
  {
    writeToScreen("response: " + evt.data + '\n');
    evt.data.split(',').forEach(function(v, i) {
      document.getElementById('v' + i).innerText = v;
    });
    rerank();
  }

  function onError(evt)
  {
    writeToScreen('error: ' + evt.data + '\n');

    websocket.close();

    document.myform.connectButton.disabled = false;
    document.myform.disconnectButton.disabled = true;

  }

  function doSend(message)
  {
    writeToScreen("sent: " + message + '\n'); 
    websocket.send(message);
  }

  function writeToScreen(message)
  {
    console.log(message);
    document.myform.outputtext.value += message
    document.myform.outputtext.scrollTop = document.myform.outputtext.scrollHeight;

  }

  window.addEventListener("load", init, false);


   function sendText() {
        doSend( document.myform.inputtext.value );
   }

  function clearText() {
        document.myform.outputtext.value = "";
   }

   function doDisconnect() {
        websocket.close();
   }
