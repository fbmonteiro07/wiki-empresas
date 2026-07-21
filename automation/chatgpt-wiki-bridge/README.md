# ChatGPT -> Wiki inbox bridge

This bridge turns an explicit ChatGPT command such as `manda pra wiki` or `/wiki`
into a Markdown file in `E:\Wiki Felipe empresas\_inbox`.

## Design

1. ChatGPT Project instructions append a structured `[[WIKI_INBOX]]` block only
   when the user explicitly requests a wiki save.
2. The Chrome helper sees the completed block and sends it to a loopback-only
   HTTP service.
3. The service validates and deduplicates the payload, then writes an attributed
   `.md` file into `_inbox`.
4. The existing wiki routing-plan -> review -> patch -> archive workflow remains
   unchanged.

The bridge never listens on the LAN and refuses non-loopback binding. The Chrome
helper only has access to `chatgpt.com` and `127.0.0.1:8765`.

## One-time setup

1. Run `start-bridge.ps1 -Install`. This starts the bridge and registers it under
   the current user's Windows `Run` key so it starts after sign-in.
2. In Chrome, open `chrome://extensions`, enable Developer mode, choose **Load
   unpacked**, and select the `extension` folder next to this README.
3. In ChatGPT, create or open a research Project. Paste the contents of
   `chatgpt-project-instructions.txt` into **Project settings -> Instructions**.

## Daily use

Ask for the summary and add one of these phrases:

- `manda pra wiki`
- `salva na wiki`
- `joga no inbox da wiki`
- `/wiki`

When the save succeeds, a green confirmation appears at the bottom-right of the
ChatGPT page. The new Markdown file is immediately visible in `_inbox` and will be
handled by the existing inbox process.

## Checks and troubleshooting

Run:

```powershell
py -3 bridge.py --check
Invoke-RestMethod http://127.0.0.1:8765/health
```

Logs and the local deduplication ledger are stored under `state/` and ignored by
Git. If a red error appears in ChatGPT, start `start-bridge.ps1` and repeat the
wiki command.

## Removal

Disable or remove the Chrome extension, then remove the `ChatGPTWikiBridge` value
from `HKCU\Software\Microsoft\Windows\CurrentVersion\Run`. Stop the running
`bridge.py` process if immediate shutdown is required.
