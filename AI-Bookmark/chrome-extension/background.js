// Create a user node when the extension is installed using the user's Google email
chrome.runtime.onInstalled.addListener(() => {
  chrome.identity.getProfileUserInfo((userInfo) => {
    console.log('User info:', userInfo);
    if (userInfo.email) {
      fetch('http://localhost:3000/createUser', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ userId: userInfo.email })
      })
      .then(response => response.json())
      .then(data => console.log('User created:', data))
      .catch(err => console.error('Error creating user:', err));
    } else {
      console.error('Unable to retrieve user email.');
    }
  });
});

// Function to recursively traverse the bookmark tree and collect bookmark items.
function traverseBookmarks(nodes, result = []) {
  nodes.forEach(node => {
    if (node.url) {
      result.push({ id: node.id, title: node.title, url: node.url });
    }
    if (node.children) {
      traverseBookmarks(node.children, result);
    }
  });
  return result;
}

// Function to extract all saved bookmarks using the Chrome bookmarks API.
function extractBookmarks() {
  chrome.bookmarks.getTree((bookmarkTreeNodes) => {
    const bookmarks = traverseBookmarks(bookmarkTreeNodes);
    console.log("Extracted bookmarks:", bookmarks);
    
    // For each bookmark, send the data to your backend for processing.
    bookmarks.forEach(bm => {
      fetch('http://localhost:3000/summarizeAndStore', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(bm)
      })
      .then(response => response.json())
      .then(data => console.log('Processed bookmark:', data))
      .catch(err => console.error('Error processing bookmark:', err));
    });
  });
}

// Listen for messages from the popup (or other parts of the extension)
chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
  if (message.action === 'extractBookmarks') {
    extractBookmarks();
    sendResponse({ status: 'Bookmarks processing started' });
  }
});
