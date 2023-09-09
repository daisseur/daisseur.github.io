// popup.js

const button = document.getElementById("changeProxyButton");

// Function to change the proxy
function changeProxy() {
    // List of proxies
    const proxyList = [
        "189.173.171.127:999",
        "45.224.149.75:999",
        "181.191.94.126:8999",
        "45.225.207.183:999",
        "211.106.84.247:1022",
        "66.203.149.124:3128",
        "51.81.187.228:3128",
        "91.238.211.110:8080",
        "176.97.73.212:3128",
        "95.56.254.139:3128",
        "129.146.67.98:3128",
        "62.72.45.88:3128",
        "200.30.138.54:3128",
        "147.139.168.187:3128",
        "150.95.111.66:3128",
        "38.156.233.76:999",
        "154.236.191.41:1976",
        "107.170.164.50:3128",
        "115.127.79.234:8080",
        "202.58.18.27:8080",
        "201.220.112.98:999",
        "154.236.191.45:1981",
        "91.204.239.189:8080",
        "178.18.242.38:3128",
        "149.202.74.231:3128",
        "91.236.156.30:8282",
        "41.33.254.189:1976",
        "103.94.8.210:8080",
        "179.1.192.26:999",
        "65.21.114.225:3128",
        "187.63.157.50:999",
        "186.3.38.207:999",
        "125.99.106.250:3128",
        "43.132.29.156:9999",
        "154.236.189.13:1974"
      ];
  
    // Get a random proxy from the list
    const randomProxy = proxyList[Math.floor(Math.random() * proxyList.length)];
  
    // Change the proxy in the chrome extension settings
    chrome.proxy.settings.set(
      { value: { mode: "fixed_servers", rules: { singleProxy: { scheme: "http", host: randomProxy.split(":")[0], port: parseInt(randomProxy.split(":")[1]) } } }, scope: "regular" },
      function () {
        // Log a success message
        console.log("Proxy changed successfully.");
      }
    );
    // show proxy wit element prxyInfo
    document.getElementById("proxyInfo").innerHTML = randomProxy;
  }

// Add an event listener to the button in the popup.html file
button.addEventListener("click", changeProxy);

// Fonction pour réinitialiser le proxy
function resetProxy() {
    // Réinitialiser les paramètres du proxy dans les paramètres de l'extension Chrome
    chrome.proxy.settings.clear({ scope: "regular" }, function () {
      // Recharger l'onglet pour appliquer les nouveaux paramètres du proxy
      chrome.tabs.reload();
    });
  }
// Ajouter un écouteur d'événement au bouton de réinitialisation du proxy
const resetProxyButton = document.getElementById("resetProxyButton");
if (resetProxyButton) {
resetProxyButton.addEventListener("click", resetProxy);
}

