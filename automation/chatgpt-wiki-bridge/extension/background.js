const BRIDGE_URL = "http://127.0.0.1:8765/ingest";

chrome.runtime.onMessage.addListener((message, _sender, sendResponse) => {
  if (!message || message.type !== "wiki-inbox-ingest") {
    return false;
  }

  fetch(BRIDGE_URL, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "X-Wiki-Bridge": "chatgpt-chrome-extension"
    },
    body: JSON.stringify(message.payload)
  })
    .then(async (response) => {
      const data = await response.json().catch(() => ({
        ok: false,
        error: `Bridge returned HTTP ${response.status}`
      }));
      sendResponse(data);
    })
    .catch((error) => {
      sendResponse({
        ok: false,
        error: "Local wiki bridge is not running. Start it and repeat the wiki command."
      });
    });

  return true;
});
