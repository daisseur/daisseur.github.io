// listen to contentScript.js
var pageURl = window.location.href.toString();
const body = document.body.getElementsByTagName('ul')[0];
const fullPagebutton = document.getElementById('fullPage');
const clearButton = document.getElementById('clear');
const removeLast = document.getElementById('removeLast');

//to list
let list;

function sendAction(action) {
  return chrome.runtime.sendMessage({ action: action }, function(response) {
    console.log("response", response);
    if (action === "list") {
      list = response;
      console.log(list, typeof(list));
      for (let i = 0; i < list.length; i++) {
        addPageMedia(list[i]);
}
    }
    return response;
  });
}

function removeElement(element) {
  let url = element.getElementsByTagName('a')[0].href
  sendAction(["removeElement", url]);
  element.remove();
}

function addPageMedia(url) {
  // send url to background script
  console.log("addPageMedia", url)

  let date = new Date();

  let newDiv = document.createElement('li');
  newDiv.classList.add('element')
  
  let a = document.createElement('a')
  a.href = url
  a.textContent = getTitle(url)
  newDiv.appendChild(a)
  

  if (url.includes("mp4") || url.includes("webm")) {
    let video = document.createElement('video')
    video.classList.add('video')
    video.src = url
    video.controls = true
    newDiv.appendChild(video)
  } else {
    let image = document.createElement('img')
    image.classList.add('image')
    image.src = url
    newDiv.appendChild(image)
  }

  let span = document.createElement('span')
  span.classList.add('timestamp')
  span.textContent = date.toLocaleString()
  newDiv.appendChild(span)


  let downDiv = document.createElement('div')
  downDiv.classList.add('downContainer')

  let download = document.createElement('a')
  download.classList.add('download-button')
  download.href = url
  download.textContent = 'Télécharger'

  let delButton = document.createElement('button')
  delButton.textContent = '🗑️'
  delButton.id = "removeButton"
  delButton.addEventListener('click', () => {
    removeElement(newDiv)
  })

  downDiv.appendChild(download)
  downDiv.appendChild(delButton)
  newDiv.appendChild(downDiv)

  body.appendChild(newDiv)
  
}

sendAction("list");

chrome.runtime.onMessage.addListener(
  (request, sender, sendResponse) => {
    if (request.addNewUrl) {
      addPageMedia(request.addNewUrl);
      sendResponse('added');
      console.log("added")
    }
  }
)

function getTitle(url) {
  let split = url.split('/');
  return split[split.length - 1];
}

function clear() {
  list = [];
  sendAction("clear");
  body.getElementsByTagName('ul')[0].innerHTML = '';
}

function removeLastElement() {
  sendAction("removeLast");
  list.pop();
  let lis = document.getElementsByTagName('ul');
  let size = lis[0].getElementsByTagName('li').length;
  lis[0].getElementsByTagName('li')[size - 1].remove();
}

fullPagebutton.addEventListener('click', () => {
  //open the page of popup
  chrome.tabs.create({ url: pageURl })
})

clearButton.addEventListener('click', () => {
  console.log("clear")
  clear();
})

removeLast.addEventListener('click', () => {
  console.log("removeLast")
  removeLastElement();  
})

