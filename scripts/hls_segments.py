"""List/download HLS fMP4 segments covering VOD windows. Usage:
hls_segments.py <index.m3u8> <base_url> <out_dir> <name>=H:MM:SS-H:MM:SS ... [--download]"""
import os, subprocess, sys
def p(t): h, m, s = t.split(':'); return int(h)*3600 + int(m)*60 + float(s)
idx, base, out = sys.argv[1], sys.argv[2], sys.argv[3]
segs, t, dur, init = [], 0.0, None, None
for line in open(idx):
    line = line.strip()
    if line.startswith('#EXT-X-MAP'): init = line.split('"')[1]
    elif line.startswith('#EXTINF'): dur = float(line.split(':')[1].rstrip(','))
    elif line and not line.startswith('#'):
        segs.append((t, dur, line)); t += dur
os.makedirs(out, exist_ok=True)
for arg in sys.argv[4:]:
    if arg.startswith('--'): continue
    name, rng = arg.split('='); a, b = map(p, rng.split('-'))
    sel = [s for s in segs if s[0] + s[1] > a and s[0] < b]
    muted = [s[2] for s in sel if 'muted' in s[2]]
    print(f"{name}: {len(sel)} segs from {sel[0][0]:.1f}s, muted={len(muted)} {muted[:4]}")
    if '--download' in sys.argv:
        d = f"{out}/{name}"; os.makedirs(d, exist_ok=True)
        files = [init] + [s[2] for s in sel]
        for f in files:
            if not os.path.exists(f"{d}/{f}"):
                subprocess.run(["curl", "-sS", "--retry", "4", "-o", f"{d}/{f}", f"{base}/{f}"], check=True)
        with open(f"{out}/{name}.mp4", "wb") as o:
            for f in files: o.write(open(f"{d}/{f}", "rb").read())
        open(f"{out}/{name}.start", "w").write(str(sel[0][0]))
