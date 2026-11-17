# 住まいAgent ブラウザー試用版 26

Windows 11 x64 の空の案件プロジェクトを Codex で開き、下の一文を送ってください。

> https://raw.githubusercontent.com/swing99527/sumai-agent-downloads/trial-26.1/README.md の手順で住まいAgent試用版をこのプロジェクトにインストールし、照合と接続確認を済ませて、次に私が行う操作を教えてください。

> 请按 https://raw.githubusercontent.com/swing99527/sumai-agent-downloads/trial-26.1/README.md 在当前项目安装住まいAgent试用版，完成校验和连接自检后告诉我下一步。

每个项目处理一批中古公寓站线。Agent 先用 REINS 列表排除明确不符的挂牌，再为其余挂牌核对详情与图纸。首次在专用 Chrome 加载本地扩展时，可能需要你打开开发者模式、选择扩展文件夹、确认启用。REINS 登录和规程确认由本人完成。适用环境为允许本地加载扩展的 Windows 11 x64、Google Chrome，以及能执行本机命令、读取图像的 Codex。图纸预览使用 Codex Desktop 的 PDF 运行时或可用的 pdftoppm。

## Agent 安装步骤

1. 从[固定版 ZIP](https://raw.githubusercontent.com/swing99527/sumai-agent-downloads/trial-26.1/sumai-agent-install-26-win-x64.zip) 下载至新的临时目录。校验 SHA-256 `2676dd9112fed4195d65057733990935b1d175d943124cbe060ae7f55f3fdeb8` 和大小 35,547,278 字节，完全匹配后再用 Windows 自带 tar.exe 展开。
2. 在解压目录执行 `& .\package\runtime\node.exe .\install.mjs $projectPath Codex`，其中 `$projectPath` 为当前空项目的绝对路径。Node 24 随包提供。阅读随包 INSTALL.md，使用安装结果中的本机路径启用专用 Chrome 的扩展并执行连接自检。
3. 在 connected=true 后读取项目内 SKILL.md，等待用户授权的站线与完整需求。案件范围在第一次检索时绑定，查询另一批时另建项目。
4. 初次启用需要使用者确认权限时，给出应确认的项目和本次实际扩展目录。REINS 登录、验证码和业务决定交给用户。连接状态与当次查询结果分别核对。

[固定 25 版](https://github.com/swing99527/sumai-agent-downloads/tree/trial-25.1)
