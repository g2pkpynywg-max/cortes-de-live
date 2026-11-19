"""Per-second contact sheet of a window file. Usage: sheet.py <file.mov> <vod_start_s> <out.jpg> [step] [width]"""
import subprocess, sys, tempfile, glob, os
from PIL import Image, ImageDraw
f, v0, out = sys.argv[1], float(sys.argv[2]), sys.argv[3]
step = float(sys.argv[4]) if len(sys.argv) > 4 else 1
W = int(sys.argv[5]) if len(sys.argv) > 5 else 240
H = W * 9 // 16
tmp = tempfile.mkdtemp()
subprocess.run(["ffmpeg", "-v", "error", "-i", f, "-vf", f"fps=1/{step},scale={W}:{H}", f"{tmp}/%04d.jpg"], check=True)
fs = sorted(glob.glob(f"{tmp}/*.jpg")); cols = max(1, 2400 // W)
sh = Image.new("RGB", (cols * W, ((len(fs) + cols - 1) // cols) * H)); d = ImageDraw.Draw(sh)
for i, x in enumerate(fs):
    X, Y = (i % cols) * W, (i // cols) * H; sh.paste(Image.open(x), (X, Y)); t = v0 + i * step
    d.rectangle([X, Y, X + 62, Y + 12], fill="black"); d.text((X + 2, Y), f"{int(t//3600)}:{int(t%3600//60):02d}:{t%60:04.1f}", fill="yellow")
sh.save(out, quality=82)
