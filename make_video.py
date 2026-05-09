"""
Shortsスクリプト(JSON) -> 縦9:16のmp4動画

依存:
  apt: ffmpeg, open-jtalk, open-jtalk-mecab-naist-jdic,
       hts-voice-nitech-jp-atr503-m001, fonts-noto-cjk
  pip: pillow

Usage:
  python make_video.py shorts_input.json output.mp4
"""

import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

from PIL import Image, ImageDraw

DICT_PATH = "/var/lib/mecab/dic/open-jtalk/naist-jdic"
VOICE_PATH = "/usr/share/hts-voice/nitech-jp-atr503-m001/nitech_jp_atr503_m001.htsvoice"
FONT_PATH = "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"

WIDTH, HEIGHT = 1080, 1920


def split_lines(text: str) -> list[str]:
    parts = re.split(r"[。、!?\n]", text)
    return [p.strip() for p in parts if p.strip()]


def synth_line(text: str, out_wav: Path) -> float:
    subprocess.run(
        [
            "open_jtalk",
            "-x", DICT_PATH,
            "-m", VOICE_PATH,
            "-r", "1.0",
            "-ow", str(out_wav),
        ],
        input=text.encode("utf-8"),
        check=True,
        capture_output=True,
    )
    out = subprocess.check_output(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=nw=1:nk=1", str(out_wav)],
        text=True,
    )
    return float(out.strip())


def make_background(out_path: Path) -> None:
    img = Image.new("RGB", (WIDTH, HEIGHT), (24, 28, 38))
    draw = ImageDraw.Draw(img)
    for y in range(HEIGHT):
        t = y / HEIGHT
        r = int(24 + (60 - 24) * t)
        g = int(28 + (40 - 28) * t)
        b = int(38 + (80 - 38) * t)
        draw.line([(0, y), (WIDTH, y)], fill=(r, g, b))
    img.save(out_path, "PNG")


def fmt_time(sec: float) -> str:
    h = int(sec // 3600)
    m = int((sec % 3600) // 60)
    s = sec - h * 3600 - m * 60
    cs = int((s - int(s)) * 100)
    return f"{h:01d}:{m:02d}:{int(s):02d}.{cs:02d}"


def ass_escape(text: str) -> str:
    return text.replace("\\", "\\\\").replace("{", "\\{").replace("}", "\\}")


def wrap(text: str, n: int = 14) -> str:
    return "\\N".join(text[i:i + n] for i in range(0, len(text), n))


def build_ass(timed_lines: list[tuple[float, float, str]], out_path: Path) -> None:
    header = f"""[Script Info]
ScriptType: v4.00+
PlayResX: {WIDTH}
PlayResY: {HEIGHT}
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, OutlineColour, BackColour, Bold, Italic, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,Noto Sans CJK JP,72,&H00FFFFFF,&H00000000,&H00000000,1,0,1,6,2,5,80,80,0,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
    events = []
    for start, end, text in timed_lines:
        wrapped = wrap(ass_escape(text), 14)
        events.append(
            f"Dialogue: 0,{fmt_time(start)},{fmt_time(end)},Default,,0,0,0,,{wrapped}"
        )
    out_path.write_text(header + "\n".join(events) + "\n", encoding="utf-8")


def main() -> None:
    if len(sys.argv) != 3:
        print("usage: python make_video.py <input.json> <output.mp4>", file=sys.stderr)
        sys.exit(1)

    in_path = Path(sys.argv[1])
    out_path = Path(sys.argv[2])
    data = json.loads(in_path.read_text(encoding="utf-8"))
    s = data["shorts_script"]
    raw = "。".join([s["hook_3sec"], s["body"], s["outro"]])
    lines = split_lines(raw)
    print(f"[info] {len(lines)} subtitle lines")

    with tempfile.TemporaryDirectory() as td:
        td = Path(td)
        wavs: list[Path] = []
        timed: list[tuple[float, float, str]] = []
        cur = 0.0

        for i, line in enumerate(lines):
            wav = td / f"line_{i:03d}.wav"
            dur = synth_line(line, wav)
            wavs.append(wav)
            timed.append((cur, cur + dur, line))
            cur += dur

        concat_list = td / "concat.txt"
        concat_list.write_text(
            "".join(f"file '{w}'\n" for w in wavs), encoding="utf-8"
        )
        merged = td / "voice.wav"
        subprocess.run(
            ["ffmpeg", "-y", "-f", "concat", "-safe", "0",
             "-i", str(concat_list), "-c", "copy", str(merged)],
            check=True, capture_output=True,
        )

        bg = td / "bg.png"
        make_background(bg)

        ass = td / "subs.ass"
        build_ass(timed, ass)

        total = cur + 0.5
        print(f"[info] total duration: {total:.2f}s")
        subprocess.run(
            [
                "ffmpeg", "-y",
                "-loop", "1", "-t", f"{total:.2f}", "-i", str(bg),
                "-i", str(merged),
                "-vf", f"ass={ass}",
                "-c:v", "libx264", "-pix_fmt", "yuv420p",
                "-c:a", "aac", "-b:a", "192k",
                "-shortest",
                str(out_path),
            ],
            check=True, capture_output=True,
        )

    print(f"[done] {out_path} ({out_path.stat().st_size / 1024:.1f} KB)")


if __name__ == "__main__":
    main()
