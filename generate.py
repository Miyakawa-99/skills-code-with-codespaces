"""
海外掲示板の投稿を日本向けSNSコンテンツに再編集する。

Usage:
    export ANTHROPIC_API_KEY=sk-ant-...
    python generate.py sample_post.txt
    python generate.py sample_post.txt --out output.json
"""

import argparse
import json
import sys
from pathlib import Path

import anthropic

MODEL = "claude-sonnet-4-6"

SCHEMA = {
    "type": "object",
    "properties": {
        "title": {
            "type": "string",
            "description": "日本人が思わずタップしたくなるタイトル(30字程度)",
        },
        "summary_3_lines": {
            "type": "array",
            "items": {"type": "string"},
            "minItems": 3,
            "maxItems": 3,
            "description": "3行要約。各行は短く、感情が伝わるように",
        },
        "x_post": {
            "type": "string",
            "description": "140〜220文字程度の共感型X投稿文",
        },
        "shorts_script": {
            "type": "object",
            "properties": {
                "hook_3sec": {"type": "string", "description": "冒頭3秒のセリフ"},
                "body": {"type": "string", "description": "本編(1分以内)"},
                "outro": {"type": "string", "description": "締め"},
            },
            "required": ["hook_3sec", "body", "outro"],
            "additionalProperties": False,
        },
        "note_intro": {
            "type": "string",
            "description": "noteの自然な導入文",
        },
    },
    "required": ["title", "summary_3_lines", "x_post", "shorts_script", "note_intro"],
    "additionalProperties": False,
}


def load_system_prompt() -> str:
    return Path(__file__).parent.joinpath("prompt.md").read_text(encoding="utf-8")


def generate(source_post: str) -> dict:
    client = anthropic.Anthropic()
    system_prompt = load_system_prompt()

    response = client.messages.create(
        model=MODEL,
        max_tokens=4096,
        system=[
            {
                "type": "text",
                "text": system_prompt,
                "cache_control": {"type": "ephemeral"},
            }
        ],
        output_config={"format": {"type": "json_schema", "schema": SCHEMA}},
        messages=[
            {
                "role": "user",
                "content": (
                    "以下の海外投稿を、ルールに従って日本向けSNSコンテンツに再編集してください。\n\n"
                    "----- 元投稿 -----\n"
                    f"{source_post}\n"
                    "----- ここまで -----"
                ),
            }
        ],
    )

    text = next(b.text for b in response.content if b.type == "text")
    result = json.loads(text)

    usage = response.usage
    print(
        f"[usage] input={usage.input_tokens} output={usage.output_tokens} "
        f"cache_write={usage.cache_creation_input_tokens} "
        f"cache_read={usage.cache_read_input_tokens}",
        file=sys.stderr,
    )

    return result


def pretty_print(data: dict) -> None:
    print(f"\n━━━ ① タイトル ━━━\n{data['title']}")
    print("\n━━━ ② 3行要約 ━━━")
    for line in data["summary_3_lines"]:
        print(f"・{line}")
    print(f"\n━━━ ③ X投稿文 ({len(data['x_post'])}字) ━━━\n{data['x_post']}")
    s = data["shorts_script"]
    print("\n━━━ ④ Shorts/TikTok台本 ━━━")
    print(f"[Hook] {s['hook_3sec']}")
    print(f"[Body] {s['body']}")
    print(f"[Outro] {s['outro']}")
    print(f"\n━━━ ⑤ note導入 ━━━\n{data['note_intro']}\n")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("input", help="元投稿のテキストファイル")
    parser.add_argument("--out", help="JSON出力先(省略時はpretty printのみ)")
    args = parser.parse_args()

    source = Path(args.input).read_text(encoding="utf-8")
    result = generate(source)

    pretty_print(result)

    if args.out:
        Path(args.out).write_text(
            json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8"
        )
        print(f"[saved] {args.out}", file=sys.stderr)


if __name__ == "__main__":
    main()
