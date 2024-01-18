<header>

<!--
  <<< Author notes: Course header >>>
  Read <https://skills.github.com/quickstart> for more information about how to build courses using this template.
  Include a 1280×640 image, course name in sentence case, and a concise description in emphasis.
  In your repository settings: enable template repository, add your 1280×640 social image, auto delete head branches.
  Next to "About", add description & tags; disable releases, packages, & environments.
  Add your open source license, GitHub uses the MIT license.
-->

# GitHub CodespacesとVisual Studio Codeでコーディング

GitHub CodespacesとVisual Studio Codeを使用してコーディングしましょう！

</header>

<!--
  <<< Author notes: Step 3 >>>
  Start this step by acknowledging the previous step.
  Define terms and link to docs.github.com.
-->

## ステップ3: あなたのcodespaceをカスタマイズしましょう！

_素晴らしい仕事です！ 🎉 カスタムイメージを使用したcodespaceを作成しました！_

VS Codeの拡張機能の追加、機能の追加、ホスト要件の設定などによって、codespaceをカスタマイズできます。

`devcontainer.json`ファイルの設定をカスタマイズしてみましょう！

### :keyboard: アクティビティ: `devcontainer.json`ファイルにカスタマイズを追加する

1. `.devcontainer/devcontainer.json`ファイルに移動します。
1. 最後の`}`の前に、ファイルの本文に以下のカスタマイズを追加します。

   ```jsonc
    ,
    // コンテナが作成されたときにインストールしたい拡張機能のIDを追加します。
    "customizations": {
        "vscode": {
            "extensions": [
                "GitHub.copilot"
            ]
        },
        "codespaces": {
            "openFiles": [
                "codespace.md"
            ]
        }
    }
   ```

1. **Commit changes**をクリックし、その後**Commit changes directly to the `main` branch**を選択します。
1. リポジトリのトップページに移動して新しいcodespaceを作成します。
1. ページの中央にある**Code**ボタンをクリックします。
1. ポップアップされるボックスの**Codespaces**タブをクリックします。
1. タブ上の`+`記号をクリックします。

   > codespaceが起動されるまで約2分待ちます。

1. 前回と同様に、codespaceが実行されていることを確認します。
1. `codespace.md`ファイルがVS Codeエディターに表示されるはずです。
1. `copilot`拡張機能がVS Codeの拡張機能リストに表示されるはずです。

   これにより、VS Code拡張機能が追加され、codespaceの起動時にファイルが開かれます。

次に、codespaceの作成時に実行するコードを追加しましょう！

### :keyboard: アクティビティ: codespaceの作成時にコードを実行する

1. ``.devcontainer/devcontainer.json`ファイルを編集します。
1. 最後の`}`の前に、ファイルの本文に以下のpostCreateCommandを追加します。

   ```jsonc
    ,
    "postCreateCommand": "echo '# Writing code upon codespace creation!'  >> codespace.md"
   ```

1. **Commit changes**をクリックし、その後**Commit changes directly to the `main` branch**を選択します。
1. リポジトリのトップページに移動して新しいcodespaceを作成します。
1. ページの中央にある**Code**ボタンをクリックします。
1. ポップアップされるボックスの**Codespaces**タブをクリックします。
1. タブ上の`+`記号をクリックします。

   > codespaceが起動されるまで約2分待ちます。

1. 前回と同様に、codespaceが実行されていることを確認します。
1. `codespace.md`ファイルに`Writing code upon codespace creation!`というテキストが追加されていることを確認します。
1. このページ（指示に従っているページ）を約20秒待ってからリフレッシュします。GitHub Actionsが自動的に次のステップに更新されます。

<footer>

<!--
  <<< Author notes: Footer >>>
  Add a link to get support, GitHub status page, code of conduct, license link.
-->

---

Get help: [Post in our discussion board](https://github.com/orgs/skills/discussions/categories/code-with-codespaces) &bull; [Review the GitHub status page](https://www.githubstatus.com/)

&copy; 2023 GitHub &bull; [Code of Conduct](https://www.contributor-covenant.org/version/2/1/code_of_conduct/code_of_conduct.md) &bull; [MIT License](https://gh.io/mit)

</footer>
