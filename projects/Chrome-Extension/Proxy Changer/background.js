// Listen for the button click event from the popup.html
chrome.browserAction.onClicked.addListener(function(tab) {
    // Load the proxy list from storage or use the default list
    chrome.storage.local.get({ proxyList: [] }, function(result) {
      const proxyList = result.proxyList;
      
      // Select a random proxy from the list
      const randomProxy = getRandomProxy(proxyList);
      
      // Update the proxy settings for the current tab
      updateProxySettings(tab.id, randomProxy);
    });
  });
  
  // Function to select a random proxy from the list
  function getRandomProxy(proxyList) {
    const randomIndex = Math.floor(Math.random() * proxyList.length);
    return proxyList[randomIndex];
  }
  
  // Function to update the proxy settings for the tab
  function updateProxySettings(tabId, proxy) {
    chrome.proxy.settings.set({
      value: {
        mode: "fixed_servers",
        rules: {
          singleProxy: {
            scheme: "http",
            host: proxy.split(":")[0],
            port: parseInt(proxy.split(":")[1])
          },
        },
      },
      scope: "regular"
    }, function() {
      // Reload the tab to apply the new proxy settings
      chrome.tabs.reload(tabId);
    });
  }
  