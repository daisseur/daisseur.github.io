function alphacoders(element) {
  let url = element.src;
  if (url) {
    // https://images8.alphacoders.com/125/1253331.jpg
    // https://initiate.alphacoders.com/download/images/281858/jpg
    previewUrl = url;
    let partsSlash = url.split('/');
    let partsPoints = url.split('.');
    let imagesn = partsPoints[0].split('/')[2];
    let number = partsSlash[partsSlash.length - 1].replace('.' + partsPoints[partsPoints.length - 1], '');
    let downloadUrl = `https://initiate.alphacoders.com/download/${imagesn}/${number}/jpg`;
    // console.log(downloadUrl);
    return [previewUrl, downloadUrl];
  } else {
    return null;
    }
};

// Function to handle mouse hover events
function handleMouseHover(event) {
  // Check if the target element is an image
  let element = event.target;
  let url = [element.src, element.src];
  pageUrl = window.location.href.toString();
  if (pageUrl.includes("https://images") && pageUrl.includes(".alphacoders.com/")) {
    url = alphacoders(element);
  }
  if (event.target.tagName === 'IMG') {
    // Send message to background script with the URL of the hovered image
    chrome.runtime.sendMessage({ imageURL: url });
    
  }
  }

function sendDownload() {
  chrome.runtime.sendMessage({ action: 'download' }, function(response) {
  // Traitez la réponse de backgroundScript.js ici
  console.log(response);
  });
}

// Listen for mouse hover events
document.addEventListener('mouseover', handleMouseHover);
document.addEventListener('keydown', function(event) {
  if (event.shiftKey && event.ctrlKey) {
    console.log("pressed : ctrl + maj");
    sendDownload();
    // window.open(chrome.extension.getURL('popup.html'), "Image Downloader", "width=500,height=300,toolbar=no,location=no,resizable=yes")
  }
});

