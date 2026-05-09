# 使い方

## 1. セットアップ

```bash
pip install -r requirements.txt
export ANTHROPIC_API_KEY=sk-ant-...
```

## 2. 試す

```bash
python generate.py sample_post.txt
```

→ ターミナルに5形式まとめて出力されます。

## 3. JSONで保存(動画化パイプライン用)

```bash
python generate.py sample_post.txt --out output.json
```

## 4. 別の投稿を試す

`sample_post.txt` を別のRedditコピペに差し替えるだけ。

## 構成

| ファイル | 役割 |
| --- | --- |
| `prompt.md` | システムプロンプト(編集方針・文体・NG)。ここを書き換えるとトーン全体が変わる |
| `generate.py` | Claude API呼び出し本体。スキーマ定義もここ |
| `sample_post.txt` | テスト用の元投稿 |

## 次のステップ候補

- Reddit API (PRAW) で `r/relationship_advice` 等から自動取得
- 出力JSONをVOICEVOX + FFmpegに流して動画化
- n8n / GitHub Actions で定期実行
