# 住まいAgent 27 · Windows / Codex / Chrome

[官网 · インストール](https://sumai-agent-install.pages.dev/)

Windows 11 x64 の空プロジェクトで Codex に以下を送ってください。

> PowerShell で https://sumai-agent-install.pages.dev/install.md を読み、手順に従ってこのプロジェクトに住まいAgent試用版をインストールし、照合と接続確認をしてください。

> 请用 PowerShell 读取 https://sumai-agent-install.pages.dev/install.md，按说明在当前项目安装住まいAgent试用版，完成校验和连接自检。

Codex installs the local project tools and opens the official Chrome Web Store. Confirm Chrome's final extension permission dialog once. Complete REINS authentication and its rules confirmation yourself. Keep the connection tab open. Then provide the complete client requirements and authorize one station/line batch. The agent screens the list, reads remaining details and original drawings, and saves the report and sources locally. Each project handles one batch; use another project for another station scope.

Requires Windows 11 x64, Chrome, Codex with local execution and image reading, and the broker's REINS permission. PDF previews use the Codex Desktop PDF runtime or pdftoppm. No API key or REINS credential is included. Installation and model processing use your authorized host permissions.

2026-11-18 trial on an existing Windows development machine with an empty project, new Codex chat and fresh Chrome profile: one extension confirmation; 29 results, 26 excluded from the list, 3 details and original drawings reviewed, 1 recommendation and 2 further exclusions. 8m59s from post-login continuation to final answer, excluding installation and authentication waiting. This is one development case. Fresh OS, independent broker review time, business accuracy on unseen cases and commercial value remain unverified. Current availability and introduction/viewing arrangements still need broker confirmation.

[Official extension](https://chromewebstore.google.com/detail/hoadgoaopafcjbgabnlbannhnfoghbld) · version 0.4.53.1

[Mac Apple Silicon preview](https://mac-27-qa.sumai-agent-install.pages.dev/install.md) — installation and sample PDF tested on arm64; live REINS validation pending.

## Fixed Windows package and agent instructions

# 住まいAgent 27 · Windows 11 x64 / Codex

请在经纪人指定的当前本机项目安装。下载 [27 版固定安装包](https://raw.githubusercontent.com/swing99527/sumai-agent-downloads/b5e25fd7e55bea1ddd0f278c0a1b32c3b396c502/sumai-agent-install-27-win-x64.zip) 到新建的临时目录。核对大小 35,546,181 字节和 SHA-256 `c6deb66c13769aa7d9b219cfafbeabff11830dd8be7ac35805aa0d7a7edefa3c`。不匹配即停止。

用 Windows 自带的 tar.exe 解压。将当前项目的绝对路径赋给 $projectPath。阅读包内 INSTALL.md，在解压目录执行：

```powershell
$installed = & .\package\runtime\node.exe .\install.mjs $projectPath Codex | ConvertFrom-Json
$node = $installed.node
$client = $installed.client
& $node $client $projectPath status
```

若尚未连接，执行 `& $node $client $projectPath open-store`。在刚打开的案件专用 Chrome 内使用原公开条目「住まいAgent / Sumai Agent」（扩展 ID hoadgoaopafcjbgabnlbannhnfoghbld）。商店需下发 0.4.53.1。已安装则直接连接。首次安装由 Codex 点击「添加至 Chrome」，Chrome 最终显示的权限由本人确认。若无法从官方商店安装或宿主无法操作商店，说明卡点，保留实际状态。

随后执行 `& $node $client $projectPath connect`。保持连接标签开启，并在连接阶段轮询 `& $node $client $projectPath status`。只有已获得本案 `connected=true` 且扩展 ID 相符才报告就绪。读取安装器返回的项目 SKILL.md，在同一对话接受找房需求。REINS 账号登录、验证码及规程确认由本人处理。只清理本次临时安装文件。


## Previous versions

[26.1](https://github.com/swing99527/sumai-agent-downloads/tree/trial-26.1) · [25.1](https://github.com/swing99527/sumai-agent-downloads/tree/trial-25.1)

For rollback, use the previous fixed package in a new project and preserve existing cases. The official Chrome extension is managed by the Chrome Web Store; a local package rollback does not downgrade it.
