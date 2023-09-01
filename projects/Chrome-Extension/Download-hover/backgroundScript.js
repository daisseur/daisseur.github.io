// Listen for messages from content script
// TODO : rajouter l'écoute de la touche maj  pour activer  et desactiverl'extension
let urlFetched = [];

function compressImage(imageUrl, qualityFactor) {
  return new Promise((resolve, reject) => {
    // Créez un élément image
    var image = new Image();

    // Attendez que l'image soit chargée
    image.onload = function() {
      // Créez un canevas
      var canvas = document.createElement('canvas');
      var ctx = canvas.getContext('2d');

      // Définissez la taille du canevas en fonction de l'image d'origine
      canvas.width = image.width;
      canvas.height = image.height;

      // Dessinez l'image d'origine sur le canevas
      ctx.drawImage(image, 0, 0);

      // Convertissez le canevas en une image de qualité réduite
      if (qualityFactor < 1) {
        var compressedImage = canvas.toDataURL('image/jpeg', qualityFactor);
        resolve(compressedImage);
      } else {
        // resolve not compressed image
        resolve(imageUrl);
      }

    };

    // Gérer les erreurs de chargement de l'image
    image.onerror = function() {
      reject(new Error('Erreur lors du chargement de l\'image.'));
    };

    // Définissez la source de l'image
    image.src = imageUrl;
  });
}

function calculateCompressionRate(imageSize) {
  const targetSize = 100 * 1024; // Taille cible de 100 Ko en octets
  if (imageSize < targetSize) {
    return 1;
  } else {
    return 1 / (Math.ceil((imageSize / targetSize) * 100) / 100);
  }
  
}

async function getFileSize(fileUrl) {
  const response = await fetch(fileUrl);
  const size = response.headers.get('content-length');
  return parseInt(size, 10);
}

function download(sendResponse, todownload) {
  // Download the last image of the array and del the last element

  let url2download = todownload;
      chrome.downloads.download({ url: url2download, saveAs: false}, (downloadId) => {
      // Handle success or failure of the download
      if (downloadId) {
        sendResponse('Image download started');
      } else {
        sendResponse('Failed to start image download');
      }});
}

chrome.runtime.onMessage.addListener(async (message, sender, sendResponse) => {
  // ...
  if (message.imageURL) {
    let imageSize = await getFileSize(message.imageURL[0]);
    let compressionRate = calculateCompressionRate(imageSize);
    console.log(compressionRate);

    compressImage(message.imageURL[0], compressionRate)
      .then(compressedImage => {
        console.log("urlFetched", [compressedImage, message.imageURL[1]]);
        urlFetched = [compressedImage, message.imageURL[1]];
        chrome.runtime.sendMessage({ urlFetched: urlFetched });
      })
      .catch(error => {
        console.error(`image url ${message.imageURL} error compress: `,error);
      });
  } else if (message.action == 'download') {
    download(sendResponse, urlFetched[1]);
  }
});

