let hist = [];

function sendDownload() {
  chrome.runtime.sendMessage({ action: 'download' }, function(response) {
  // Traitez la réponse de backgroundScript.js ici
  console.log(response);
  });
}

chrome.runtime.onMessage.addListener((message, sender) => {
  if (message.urlFetched) {
    let urlFetched = message.urlFetched;
    hist.push(urlFetched);
    if (hist.length > 10) {
      hist.shift();
    } 
    if (urlFetched) {
      console.log("urlFetched", urlFetched);
      let ul = document.getElementById('urls');
      ul.innerHTML = `<li>${urlFetched[1]}<li>`;
      if (urlFetched[0]) {
       ul.innerHTML += `<img src="${urlFetched[0]}" />`;
      }
    }
  }
  
  
});

document.getElementById('download').addEventListener('click', function() {
  // Envoie un message à backgroundScript.js
  sendDownload();
  
});

document.addEventListener('keydown', function(event) {
  if (event.shiftKey && event.ctrlKey) {
    console.log("pressed : ctrl + maj");
    sendDownload();
  }
});
