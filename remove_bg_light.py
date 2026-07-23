#!/usr/bin/env python3
"""
remove_bg_light.py — PIL 亮度閾值去背腳本（淺色背景版）
用法：python remove_bg_light.py [--dir <目錄>] [<檔案> ...]

與 remove_bg.py 相反：移除「亮」的像素（近白/米白背景），保留暗部圖案。
"""
import sys
import argparse
from pathlib import Path
from PIL import Image

LIGHT_THRESHOLD = 225  # 亮度 > 此值 → 完全透明
FADE_THRESHOLD = 195   # 亮度介於 FADE~LIGHT → 漸變透明


def remove_bg(path: Path) -> None:
    img = Image.open(path).convert("RGBA")
    data = img.load()
    w, h = img.size

    for y in range(h):
        for x in range(w):
            r, g, b, a = data[x, y]
            lum = r * 0.299 + g * 0.587 + b * 0.114
            if lum > LIGHT_THRESHOLD:
                data[x, y] = (r, g, b, 0)
            elif lum > FADE_THRESHOLD:
                ratio = (LIGHT_THRESHOLD - lum) / (LIGHT_THRESHOLD - FADE_THRESHOLD)
                data[x, y] = (r, g, b, int(255 * ratio))

    img.save(path)
    print(f"  去背完成：{path.name}")


def main():
    parser = argparse.ArgumentParser(description="PNG 圖示去背（淺色背景，亮度閾值）")
    parser.add_argument("files", nargs="*", help="指定要處理的 PNG 檔案")
    parser.add_argument("--dir", default=None, help="批次處理該目錄下的 icon_*.png")
    args = parser.parse_args()

    targets = []
    if args.files:
        targets = [Path(f) for f in args.files]
    elif args.dir:
        targets = sorted(Path(args.dir).glob("icon_*.png"))
    else:
        targets = sorted(Path("images").glob("icon_*.png"))

    if not targets:
        print("找不到符合條件的 PNG 檔案。")
        sys.exit(0)

    print(f"共 {len(targets)} 個檔案待處理…")
    for p in targets:
        if p.exists():
            remove_bg(p)
        else:
            print(f"  跳過（找不到）：{p}")

    print("全部完成。")


if __name__ == "__main__":
    main()
