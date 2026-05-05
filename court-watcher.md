# court-watcher

都立公園テニスコートのキャンセル枠を検知して LINE で通知する Cloudflare Worker です。

## 仕組み

- Cloudflare Workers の Cron で 15 分おきに予約サイトを巡回
- KV に直前のスナップショットを保存し「不可 → 空き」になった枠だけを抽出
- 登録ユーザー全員に LINE Messaging API でプッシュ通知
- LINE Webhook で友だち追加 / メッセージから自動登録・解除

## サイトに対する配慮

`scraper.ts` と `wrangler.toml` には以下の設定が入っています。負荷をかけないでください。

- リクエスト間隔: 2.5 秒（環境変数 `REQUEST_DELAY_MS`）
- スキャン間隔: 15 分
- JST 0:00–5:59 はスキャンしない
- 登録ユーザーが 0 人なら HTTP リクエストを一切発生させない
- User-Agent に連絡先を明記
- 並列リクエストなし（逐次）

## セットアップ

### 1. LINE Messaging API チャネルを作成

1. https://developers.line.biz/console/ にログイン
2. 「新規プロバイダー」→「Messaging API」チャネル作成
3. Basic settings 画面で **Channel secret** を控える
4. Messaging API 画面で **Channel access token (long-lived)** を発行して控える
5. 同画面の「Auto-reply messages」を **Disabled**、「Greeting messages」も任意で **Disabled**
6. 「Allow bot to join group chats」は不要

### 2. Cloudflare に KV と Worker を用意

```bash
npm install
npx wrangler login

# KV namespace を作成
npx wrangler kv namespace create STATE
# 表示された id を wrangler.toml の REPLACE_WITH_KV_NAMESPACE_ID に貼り付け

# Secrets
npx wrangler secret put LINE_CHANNEL_ACCESS_TOKEN
npx wrangler secret put LINE_CHANNEL_SECRET

# デプロイ
npx wrangler deploy
```

### 3. LINE Webhook を設定

1. デプロイ後に表示される URL（例: `https://court-watcher.<account>.workers.dev`）の末尾に `/webhook` を付けて、LINE Developers Console の **Webhook URL** に設定
2. **Use webhook** を ON
3. 「Verify」を押して `200 OK` が返ることを確認

### 4. ボットを友だち追加してテスト

1. LINE Developers Console の Messaging API 画面にある QR コードを自分の LINE で読み取る
2. 友だち追加 → 自動的に登録される
3. 何かメッセージを送ると登録確認の返信が届く
4. 「停止」と送ると解除、「状態」で現在の状態確認

## スクレイパー実装ガイド

`src/scraper.ts` の `fetchParkDay` と `parseAvailability` は **TODO のスタブ** です。実サイトのリクエスト構造を観察して実装する必要があります（外部からの調査では取得できなかったため）。

### 調査手順

1. ブラウザ DevTools の Network タブを開いた状態で https://kouen.sports.metro.tokyo.lg.jp/web/ を開く
2. 「空き状況確認」→ 公園 → テニス → 日付 と進む
3. 各遷移で送られているリクエスト（メソッド・パス・フォームパラメータ）を控える
4. 最終ページの HTML を保存し、コート × 時間帯 × 状態 を表す DOM 構造を特定する

### 実装すべきもの

- `fetchParkDay`: 観察したフォーム遷移をそのまま `fetch` で再現。`Cookie` に `JSESSIONID` を保持
- `parseAvailability`: HTMLRewriter または正規表現で `Slot[]` を組み立てる
- `src/parks.ts`: `id` を実サイトの公園コードに置き換える

### 状態の表記例

サイト上では「○ = 空き」「×= 予約済」「-= 受付外」が一般的です。`available` は `○` のときだけ true、それ以外は false にしてください。「-」「×」を区別する必要はありません（差分検知では「不可 → ○ になった」だけ検出するため）。

## 運用メモ

- **抽選確定漏れ枠**（前月 20 日深夜〜21 日朝）と **4 日前キャンセル枠** が主な狙い目です
- LINE Messaging API の無料枠は月 200 通の push 上限あり。通知が多すぎる場合は `formatNotification` を 1 通にまとめる現状実装で問題なし
- ログは `npx wrangler tail` で確認できます
- KV 使用量は微々たるもの（1 スナップショット数百 KB）
