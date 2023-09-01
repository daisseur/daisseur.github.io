// contentScript.js
let overedUrls = [];
const pageURl = window.location.href.toString();

function addMedia(url) {
  // send url to background scrit and show response
  chrome.runtime.sendMessage({ NewUrl: url }, function(response) {
    console.log(`response of ${url}:`, response);
  });

}

function checkMediaUrl(url) {
  if (url && url.includes) {
    let base = url;
    if (url.includes("?")) {
      base = url.split("?")[0];
    }
    ext = base.split('.').pop();
    imagesExt = ['png', 'jpg', 'jpeg', 'gif', 'webp'];
    videoExt = ['mp4', 'webm'];
    if (imagesExt.includes(ext.toLowerCase()) || videoExt.includes(ext.toLowerCase())) {
      return base;
    } else {
      return false;
    }
  }
}

function handleMouseHover(event) {
  let element = event.target;
  let select_url;
  if (pageURl.includes('discord')) {
    // check if src
    if ( element.src ) {
      select_url = element.src;
    } else {
      select_url = element.href;
    }
  } else {
    select_url = element.src;
  }

  let check = checkMediaUrl(select_url);
  if (select_url !== overedUrls[overedUrls.length - 1] && check) {
    overedUrls.push(check);
  }
  
  if (overedUrls.length > 10)
    overedUrls.shift();
  for (let i = 0; i < overedUrls.length; i++) {
    if (overedUrls[i] === undefined) {
      // remove element
      overedUrls.splice(i, 1);
    }
  }
  //console.log(overedUrls);
}

document.addEventListener('mouseover', handleMouseHover);
document.addEventListener('keydown', function(event) {
  if (event.key === 'a') {
    console.log("pressed a, sending", overedUrls)
    addMedia(overedUrls[overedUrls.length - 1]);
  }
});
