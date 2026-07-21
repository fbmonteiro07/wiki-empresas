(() => {
  const START = "[[WIKI_INBOX]]";
  const SUMMARY = "---SUMMARY---";
  const END = "[[/WIKI_INBOX]]";

  function parsePayload(text) {
    const start = text.lastIndexOf(START);
    if (start < 0) return null;
    const end = text.indexOf(END, start + START.length);
    if (end < 0) return null;

    const block = text.slice(start + START.length, end).trim();
    const summaryAt = block.indexOf(SUMMARY);
    if (summaryAt < 0) return null;

    const header = block.slice(0, summaryAt).trim();
    const summary = block.slice(summaryAt + SUMMARY.length).trim();
    const payload = { summary };

    for (const line of header.split(/\r?\n/)) {
      const colon = line.indexOf(":");
      if (colon < 1) continue;
      const key = line.slice(0, colon).trim().toLowerCase();
      const value = line.slice(colon + 1).trim();
      payload[key] = value;
    }

    payload.tickers = (payload.tickers || "")
      .split(/[,;]/)
      .map((value) => value.trim())
      .filter(Boolean);
    payload.themes = (payload.themes || "")
      .split(/[,;]/)
      .map((value) => value.trim())
      .filter(Boolean);
    return payload;
  }

  function toast(message, ok) {
    const old = document.getElementById("chatgpt-wiki-inbox-toast");
    if (old) old.remove();
    const node = document.createElement("div");
    node.id = "chatgpt-wiki-inbox-toast";
    node.textContent = message;
    Object.assign(node.style, {
      position: "fixed",
      right: "20px",
      bottom: "20px",
      zIndex: "2147483647",
      padding: "12px 16px",
      borderRadius: "8px",
      color: "white",
      background: ok ? "#16794b" : "#a83232",
      boxShadow: "0 4px 16px rgba(0,0,0,.3)",
      font: "13px/1.4 system-ui, sans-serif",
      maxWidth: "420px"
    });
    document.documentElement.appendChild(node);
    setTimeout(() => node.remove(), 7000);
  }

  function processMessages() {
    const messages = document.querySelectorAll('[data-message-author-role="assistant"]');
    for (const message of messages) {
      if (message.dataset.wikiInboxStatus) continue;
      const payload = parsePayload(message.textContent || "");
      if (!payload) continue;

      message.dataset.wikiInboxStatus = "sending";
      chrome.runtime.sendMessage(
        { type: "wiki-inbox-ingest", payload },
        (response) => {
          if (chrome.runtime.lastError) {
            message.dataset.wikiInboxStatus = "error";
            toast("Wiki inbox: Chrome helper error.", false);
            return;
          }
          if (response && response.ok) {
            message.dataset.wikiInboxStatus = "sent";
            toast(
              response.duplicate
                ? "Wiki inbox: this summary was already saved."
                : "Wiki inbox: summary saved successfully.",
              true
            );
          } else {
            message.dataset.wikiInboxStatus = "error";
            toast(`Wiki inbox: ${response?.error || "unknown error"}`, false);
          }
        }
      );
    }
  }

  let timer = null;
  const observer = new MutationObserver(() => {
    clearTimeout(timer);
    timer = setTimeout(processMessages, 350);
  });
  observer.observe(document.documentElement, { childList: true, subtree: true });
  processMessages();
})();
