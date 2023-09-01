let internList = [];

function backgroundLog(...args) {
    let date = new Date();
    console.log(`${date.toLocaleString()} [LOG] ${args.join(' ')}`);
}

chrome.runtime.onMessage.addListener(
    (request, sender, sendResponse) => {
      if (request.NewUrl) {
        internList.push(request.NewUrl);
        backgroundLog("ADDED:", request.NewUrl, "LIST:", internList);
        sendResponse('added');
        chrome.runtime.sendMessage({ addNewUrl: request.NewUrl }, function(response) {
          backgroundLog("RESPONSE of add in popup:", response);
        })
      } else if (request.action === 'removeLast') {
        internList.pop();
        sendResponse('removed last item');
        backgroundLog("REMOVED LAST");
      } else if (request.action == 'clear') {
        internList = [];
        sendResponse('cleared');
        backgroundLog("CLEARED");
      } else if (request.action === 'list') {
        sendResponse(internList);
        backgroundLog("LIST", internList);
      } else if (typeof(request.action === Array)) {
        if (request.action[0] === "removeElement") {
          internList.splice(request.action[1], 1);
          sendResponse('removed element');
          backgroundLog("REMOVED ELEMENT:", request.action[1]);
        }
      }
    }
  )


