# 住まいAgent を自分の AI にインストールする

業務用の Windows 11 x64 パソコンで、Codex の案件プロジェクトを開き、次の一文を送ってください。

> このプロジェクトに住まいAgent試用版をインストールしてください。https://raw.githubusercontent.com/swing99527/sumai-agent-downloads/trial-25.1/README.md の手順で照合・導入・自己診断まで進め、次に私が行う操作だけ教えてください。

中文指令也可以使用。

> 请按 https://raw.githubusercontent.com/swing99527/sumai-agent-downloads/trial-25.1/README.md 在当前项目安装住まいAgent试用版，完成校验和自检后告诉我下一步。

## Agent 用インストール手順

1. Windows 11 x64 のローカル案件プロジェクトを使用します。新しい一時フォルダーに [固定版 ZIP](https://raw.githubusercontent.com/swing99527/sumai-agent-downloads/trial-25.1/sumai-agent-install-25-win-x64.zip) を HTTPS でダウンロードします。公開ダウンロードには GitHub ログインは不要です。
2. ZIP の SHA-256 が `f945649cb827359a7937da7e487158cb3eb09efd1dd7919aaa88f52424841986` と完全一致することを確認してから展開します。上記 URL の内容が読めない、サイズまたはハッシュが異なる場合は中止してください。期待サイズは 35,288,767 バイトです。
3. Windows 標準の `tar.exe -xf` で一時フォルダーに展開し、同梱の `INSTALL.md` を読みます。展開先で `& .\package\runtime\node.exe .\install.mjs $projectPath Codex` を実行してください。`$projectPath` にはエージェントが現在の案件プロジェクトの絶対パスを設定します。Claude Code で導入する場合は末尾を `Claude` にします。Node.js 24 は同梱済みです。
4. 成功時の JSON に示された `skill` を読み、`node` を後の CLI 実行に使います。自分が作成した一時ダウンロード・展開フォルダーは検証後に片付けてください。既存の同名 Skill に変更がある場合は、利用者のファイルを残して停止します。
5. どの版をどこに入れたか、業務用 Chrome の公式 ChatGPT 拡張機能・図面の目視・本人の REINS 権限について実際に確認できた範囲を利用者に伝えます。ログイン・規程の確認は利用者本人が行います。

固定25は東京の中古マンション向けの試用版です。実案件を通した検証は設定済みの Windows と Codex 上で実施しました。Claude Code で確認した範囲はこの配布物の Skill 配置と CLI 自己診断です。
