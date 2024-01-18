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
  <<< Author notes: Step 4 >>>
  Start this step by acknowledging the previous step.
  Define terms and link to docs.github.com.
-->

## ステップ4: あなたのcodespaceをパーソナライズしましょう！

_codespaceのカスタマイズ、お疲れさまでした！_ 🥳

どんな開発環境を使用する場合でも、設定やツールを自分の好みやワークフローに合わせてカスタマイズすることは重要なステップです。GitHub Codespacesでは、VS Codeの`Settings Sync`と`dotfiles`の2つの主要な方法でcodespaceをパーソナライズできます。

このアクティビティでは`dotfiles`に焦点を当てます。

**`dotfiles`とは何ですか？** Dotfilesは、Unix系システムで.で始まるファイルやフォルダで、システム上のアプリケーションやシェルの設定を制御します。GitHub上のリポジトリにdotfilesを保存して管理することができます。

これがどのように機能するか見てみましょう！

### :keyboard: アクティビティ: あなたのcodespaceに`dotfile`を有効にする

1. リポジトリのランディングページから始めます。
1. github.com上の任意のページの右上隅にあるご自身のプロフィール写真をクリックし、**Settings**をクリックします。
1. サイドバーの**Code, planning, and automation**セクションで、**Codespaces**をクリックします。
1. **Dotfiles**の下で、**Automatically install dotfiles**を選択して、GitHub Codespacesが新しく作成されたすべてのcodespaceに自動的にdotfilesをインストールするようにします。
1. **Select repository**をクリックし、その後dotfilesをインストールするリポジトリとして今回の研修で使用しているリポジトリを選択します。

### :keyboard: アクティビティ: リポジトリに`dotfile`を追加し、codespaceを実行する

1. リポジトリのトップページから始めます。
1. ページの中央にある**Code**ボタンをクリックします。
1. ポップアップされるボックスの**Codespaces**タブをクリックします。
1. **Create codespace on main**ボタンをクリックします。

   > codespaceが起動するまで約**2分**待ちます。

1. 前回と同様に、codespaceが実行されていることを確認します。ブラウザにはVS Codeのウェブベースエディターが表示され、以下のようなターミナルが存在するはずです：

   ![codespace1](https://user-images.githubusercontent.com/26442605/207355196-71aab43f-35a9-495b-bcfe-bf3773c2f1b3.png)

1. VS Codeのエクスプローラウィンドウ内のcodespaceで新しいファイル `setup.sh` を作成します。
1. 以下のコードをファイル内に追加します：

   ```bash
   #!/bin/bash

   sudo apt-get update
   sudo apt-get install sl
   ```

1. ファイルを保存します。
   > **注**: ファイルは自動保存されるはずです。
1. ファイルの変更をコミットします。VS Codeのターミナルで次を入力します：

   ```shell
   git add setup.sh --chmod=+x
   git commit -m "Adding setup.sh from the codespace!"
   ```


1. リポジトリに変更をプッシュします。VS Codeのターミナルで次を入力します：


   ```shell
   git push
   ```
1. リポジトリのホームページに戻り、`setup.sh`を確認して新しいコードがリポジトリにプッシュされたことを確認します。
1. codespaceのウェブブラウザタブを閉じます。
1. タブ上の`+`記号をクリックします。

   > codespaceが起動するまで約**2分**待ちます。

1. 前回と同様に、codespaceが実行されていることを確認します。
1. `setup.sh`ファイルがVS Codeエディターに存在することを確認します。
1. VS Codeのターミナルで、次を入力または貼り付けます：

   ```shell
   /usr/games/sl
   ```

1. ショーを楽しんでください！
1. このページ（指示に従っているページ）を約20秒待ってからリフレッシュします。[GitHub Actions](https://docs.github.com/en/actions)が自動的に次のステップに更新されます。

<footer>

<!--
  <<< Author notes: Footer >>>
  Add a link to get support, GitHub status page, code of conduct, license link.
-->

---

Get help: [Post in our discussion board](https://github.com/orgs/skills/discussions/categories/code-with-codespaces) &bull; [Review the GitHub status page](https://www.githubstatus.com/)

&copy; 2023 GitHub &bull; [Code of Conduct](https://www.contributor-covenant.org/version/2/1/code_of_conduct/code_of_conduct.md) &bull; [MIT License](https://gh.io/mit)

</footer>
