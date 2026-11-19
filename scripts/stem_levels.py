"""Loudness of each Demucs stem per window + rough 'musicness' (bass+drums steadiness). Usage: stem_levels.py name..."""
import subprocess, sys, re, numpy as np
def lufs(f):
    o = subprocess.run(["ffmpeg", "-i", f, "-af", "ebur128", "-f", "null", "-"], capture_output=True, text=True).stderr
    m = re.findall(r"I:\s+(-?[\d.]+) LUFS", o); return float(m[-1]) if m else -99
def env(f):
    pcm = subprocess.run(["ffmpeg", "-v", "error", "-i", f, "-ac", "1", "-ar", "8000", "-f", "s16le", "-"], capture_output=True).stdout
    a = np.frombuffer(pcm, dtype=np.int16).astype(float) / 32768
    r = np.array([np.sqrt(np.mean(a[i:i+4000]**2)) + 1e-6 for i in range(0, len(a) - 4000, 4000)])
    db = 20 * np.log10(r); return (db > -45).mean()   # share of half-seconds with sustained energy
for n in sys.argv[1:]:
    d = f"work/alan/stems/htdemucs/{n}"
    print(n, " ".join(f"{k}={lufs(f'{d}/{k}.wav'):.1f}" for k in ("vocals", "drums", "bass", "other")),
          f"| bass active {env(f'{d}/bass.wav'):.0%} drums active {env(f'{d}/drums.wav'):.0%}")
