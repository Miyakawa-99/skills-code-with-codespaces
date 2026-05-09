"""4音声サンプルを1本のmp4に連結。各セクションにキャラ名テロップ。"""

import subprocess
import tempfile
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

W, H = 1080, 1920
FONT = "/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc"

VOICES = [
    ("voice_samples/01_default_male.wav", "① デフォルト", "Open JTalk\nナレーター系男性"),
    ("voice_samples/02_zundamon_fu.wav", "② ずんだもん風", "ピッチ +55%\n速度 +5%"),
    ("voice_samples/03_metan_fu.wav", "③ 四国めたん風", "ピッチ +40%\n速度 -5%"),
    ("voice_samples/04_himari_fu.wav", "④ 冥鳴ひまり風", "ピッチ +20%\n速度 +0%"),
]


def make_card(title: str, sub: str, out: Path) -> None:
    img = Image.new("RGB", (W, H), (24, 28, 38))
    draw = ImageDraw.Draw(img)
    for y in range(H):
        t = y / H
        r = int(24 + (60 - 24) * t)
        g = int(28 + (40 - 28) * t)
        b = int(38 + (80 - 38) * t)
        draw.line([(0, y), (W, y)], fill=(r, g, b))

    title_font = ImageFont.truetype(FONT, 110)
    sub_font = ImageFont.truetype(FONT, 56)
    label_font = ImageFont.truetype(FONT, 44)

    bbox = draw.textbbox((0, 0), title, font=title_font)
    tw = bbox[2] - bbox[0]
    draw.text(((W - tw) // 2, 700), title, fill=(255, 255, 255),
              font=title_font, stroke_width=4, stroke_fill=(0, 0, 0))

    y = 900
    for sub_line in sub.split("\n"):
        bbox = draw.textbbox((0, 0), sub_line, font=sub_font)
        tw = bbox[2] - bbox[0]
        draw.text(((W - tw) // 2, y), sub_line, fill=(220, 220, 240), font=sub_font)
        y += 90

    label = "音声比較デモ"
    bbox = draw.textbbox((0, 0), label, font=label_font)
    tw = bbox[2] - bbox[0]
    draw.text(((W - tw) // 2, 200), label, fill=(180, 180, 200), font=label_font)

    img.save(out, "PNG")


def get_duration(path: Path) -> float:
    out = subprocess.check_output(
        ["ffprobe", "-v", "error", "-show_entries", "format=duration",
         "-of", "default=nw=1:nk=1", str(path)],
        text=True,
    )
    return float(out.strip())


def make_segment(wav: Path, card: Path, out: Path) -> None:
    dur = get_duration(wav) + 0.4
    subprocess.run(
        [
            "ffmpeg", "-y",
            "-loop", "1", "-t", f"{dur:.2f}", "-i", str(card),
            "-i", str(wav),
            "-c:v", "libx264", "-pix_fmt", "yuv420p", "-r", "30",
            "-c:a", "aac", "-b:a", "192k",
            "-shortest", str(out),
        ],
        check=True, capture_output=True,
    )


def main() -> None:
    with tempfile.TemporaryDirectory() as td:
        td = Path(td)
        segs = []
        for i, (wav_path, title, sub) in enumerate(VOICES):
            card = td / f"card_{i}.png"
            seg = td / f"seg_{i}.mp4"
            make_card(title, sub, card)
            make_segment(Path(wav_path), card, seg)
            segs.append(seg)

        list_file = td / "list.txt"
        list_file.write_text("".join(f"file '{s}'\n" for s in segs), encoding="utf-8")

        subprocess.run(
            ["ffmpeg", "-y", "-f", "concat", "-safe", "0", "-i", str(list_file),
             "-c", "copy", "voice_compare.mp4"],
            check=True, capture_output=True,
        )

    out = Path("voice_compare.mp4")
    print(f"[done] {out} ({out.stat().st_size / 1024:.0f} KB, "
          f"{get_duration(out):.1f}s)")


if __name__ == "__main__":
    main()
