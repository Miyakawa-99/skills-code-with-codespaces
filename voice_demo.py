"""
Open JTalk + ピッチシフトで「キャラ風」音声を作るデモ。
本物のVOICEVOXじゃないが、声の幅を確認するのに使える。

各プリセットは asetrate (高さ+速度同時) と atempo (速度のみ) の組み合わせで作る。
"""

import subprocess
from pathlib import Path

DICT = "/var/lib/mecab/dic/open-jtalk/naist-jdic"
VOICE = "/usr/share/hts-voice/nitech-jp-atr503-m001/nitech_jp_atr503_m001.htsvoice"
SAMPLE_RATE = 48000

PRESETS = {
    "01_default_male": {
        "label": "デフォルト(ナレーター系男性)",
        "rate": 1.0,
        "pitch_factor": 1.0,
    },
    "02_zundamon_fu": {
        "label": "ずんだもん風(高め女子)",
        "rate": 1.05,
        "pitch_factor": 1.55,
    },
    "03_metan_fu": {
        "label": "四国めたん風(お嬢様風)",
        "rate": 0.95,
        "pitch_factor": 1.40,
    },
    "04_himari_fu": {
        "label": "冥鳴ひまり風(落ち着いた女性)",
        "rate": 1.0,
        "pitch_factor": 1.20,
    },
}

LINE = "お母さんが、君は嫁に向かないって言うんだ。付き合って4年、急に彼に言われた。"


def synth_base(text: str, rate: float, out: Path) -> None:
    subprocess.run(
        ["open_jtalk", "-x", DICT, "-m", VOICE, "-r", f"{rate}", "-ow", str(out)],
        input=text.encode("utf-8"), check=True, capture_output=True,
    )


def pitch_shift(in_wav: Path, factor: float, out_wav: Path) -> None:
    """asetrate を上げると音が高く+速くなる -> atempo で速度だけ戻す"""
    if abs(factor - 1.0) < 0.01:
        subprocess.run(["cp", str(in_wav), str(out_wav)], check=True)
        return
    new_sr = int(SAMPLE_RATE * factor)
    subprocess.run(
        [
            "ffmpeg", "-y", "-i", str(in_wav),
            "-af", f"asetrate={new_sr},aresample={SAMPLE_RATE},atempo={1/factor:.4f}",
            str(out_wav),
        ],
        check=True, capture_output=True,
    )


def main() -> None:
    out_dir = Path("voice_samples")
    out_dir.mkdir(exist_ok=True)

    for name, p in PRESETS.items():
        base = out_dir / f"{name}_base.wav"
        final = out_dir / f"{name}.wav"
        synth_base(LINE, p["rate"], base)
        pitch_shift(base, p["pitch_factor"], final)
        base.unlink()
        size_kb = final.stat().st_size / 1024
        print(f"[ok] {name}.wav  ({p['label']})  {size_kb:.0f}KB")


if __name__ == "__main__":
    main()
