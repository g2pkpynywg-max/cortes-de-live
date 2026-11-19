"""Frame sheet from a rendered MP4 at given times. Usage: preview_sheet.py <mp4> <out.jpg> t1,t2,..."""
import subprocess, sys, tempfile
from PIL import Image, ImageDraw
f, out, ts = sys.argv[1], sys.argv[2], [float(x) for x in sys.argv[3].split(",")]
W, H = 216, 384; cols = min(len(ts), 8)
sh = Image.new("RGB", (W * cols, H * ((len(ts) + cols - 1) // cols))); d = ImageDraw.Draw(sh)
tmp = tempfile.mkdtemp()
for i, t in enumerate(ts):
    p = f"{tmp}/{i}.png"
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-ss", str(t), "-i", f, "-frames:v", "1", "-vf", f"scale={W}:{H}", p], check=True)
    x, y = (i % cols) * W, (i // cols) * H; sh.paste(Image.open(p), (x, y)); d.text((x + 4, y + 4), f"{t}s", fill="yellow")
sh.save(out, quality=88)
