document.addEventListener('DOMContentLoaded', function () {
  const titleElem = document.getElementById('title');
  const bookmarkLink = document.getElementById('bookmarkLink');
  const summaryElem = document.getElementById('summary');
  const bookmarkElem = document.getElementById('bookmark');
  const likeButton = document.getElementById('likeButton');
  const dislikeButton = document.getElementById('dislikeButton');
  const nextButton = document.getElementById('nextButton');
  const loadingIndicator = document.getElementById('loading');
  const bookmarkControls = document.getElementById('bookmarkControls');
  const chatToggleBtn = document.getElementById('chatToggleBtn');
  const chatModal = document.getElementById('chatModal');
  const closeChatBtn = document.getElementById('closeChatBtn');
  const conversationElem = document.getElementById('conversation');
  const chatInput = document.getElementById('chatInput');
  const sendButton = document.getElementById('sendButton');
  const bookmarkSection = document.getElementById('bookmarkSection');
  const chatTitle = document.getElementById('chatTitle');

  let chatOpen = false;

  // Open chat: hide summary and controls, then show the chat modal overlay.
  chatToggleBtn.addEventListener('click', () => {
    chatOpen = true;
    bookmarkSection.classList.add('chat-open');
    chatToggleBtn.style.display = 'none';
    // Update the chat header title and set the title link as the bookmark title.
    chatTitle.innerText = titleElem.innerText;
    chatModal.classList.add('open');
  });

  // Close chat: hide chat modal and restore the bookmark section.
  closeChatBtn.addEventListener('click', () => {
    chatOpen = false;
    chatModal.classList.remove('open');
    bookmarkSection.classList.remove('chat-open');
    chatToggleBtn.style.display = 'inline-block';
  });

  // Utility: Show or hide the loading indicator.
  function setLoading(isLoading) {
    loadingIndicator.style.display = isLoading ? 'block' : 'none';
  }

  // Load one bookmark from the backend using /randomBookmarks.
  function loadBookmark() {
    setLoading(true);
    fetch('http://localhost:3000/randomBookmarks')
      .then(response => response.json())
      .then(data => {
        if (Array.isArray(data) && data.length > 0) {
          const bookmark = data[0];
          // Update title, summary and link.
          titleElem.innerText = bookmark.title || "No Title";
          bookmarkLink.innerText = bookmark.title || "No Title";
          // Set the clickable link to open in a new tab.
          bookmarkLink.href = bookmark.url || "#";
          summaryElem.innerText = bookmark.summary || "Bookmark summary will appear here.";
          bookmarkElem.setAttribute('data-id', bookmark.id);
          conversationElem.innerHTML = "";
          if (!chatOpen) {
            summaryElem.style.display = '';
            bookmarkControls.style.display = 'flex';
            chatToggleBtn.style.display = 'inline-block';
          }
        } else if (data.error) {
          titleElem.innerText = "Error";
          summaryElem.innerText = data.error;
        } else {
          titleElem.innerText = "No bookmark found";
          summaryElem.innerText = "";
        }
      })
      .catch(err => {
        titleElem.innerText = "Error";
        summaryElem.innerText = err.toString();
      })
      .finally(() => setLoading(false));
  }

  // Update feedback for the current bookmark.
  function updateFeedback(feedback) {
    const bookmarkId = bookmarkElem.getAttribute('data-id');
    const userId = localStorage.getItem('userEmail') || "default@example.com";
    setLoading(true);
    fetch('http://localhost:3000/feedback', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ bookmarkId, feedback, userId })
    })
      .then(response => response.json())
      .then(data => {
        console.log("Feedback updated:", data);
        loadBookmark();
      })
      .catch(err => console.error("Feedback error:", err))
      .finally(() => setLoading(false));
  }

  // Append a message to the conversation area.
  function appendMessage(role, text) {
    const messageElem = document.createElement('div');
    messageElem.classList.add('message', role);
    const p = document.createElement('p');
    p.innerText = text;
    messageElem.appendChild(p);
    conversationElem.appendChild(messageElem);
    conversationElem.scrollTop = conversationElem.scrollHeight;
  }

  // Send a chat query.
  function sendChat() {
    const bookmarkId = bookmarkElem.getAttribute('data-id');
    const query = chatInput.value;
    if (!query.trim()) return;
    appendMessage('user', query);
    chatInput.value = "";
    setLoading(true);
    fetch('http://localhost:3000/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ bookmarkId, query })
    })
      .then(response => response.json())
      .then(data => {
        if (data.response) {
          appendMessage('bot', data.response);
        } else {
          appendMessage('bot', data.error || "No response");
        }
      })
      .catch(err => {
        console.error("Chat error:", err);
        appendMessage('bot', "Error in chat request.");
      })
      .finally(() => setLoading(false));
  }

  chatInput.addEventListener('keydown', function (e) {
    if (e.key === 'Enter') {
      e.preventDefault();
      sendChat();
    }
  });
  sendButton.addEventListener('click', sendChat);

  likeButton.addEventListener('click', () => updateFeedback('like'));
  dislikeButton.addEventListener('click', () => updateFeedback('dislike'));
  nextButton.addEventListener('click', loadBookmark);

  loadBookmark();
});
