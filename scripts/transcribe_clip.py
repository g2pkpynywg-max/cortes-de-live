"""Word-level transcript of a clip's vocal stem with times on the VOD clock.
Usage: transcribe_clip.py <vocals.wav> <window_start H:MM:SS> <out.json>"""
import json, sys, subprocess, numpy as np
from faster_whisper import WhisperModel
src, w0, out = sys.argv[1], sys.argv[2], sys.argv[3]
h, m, s = w0.split(':'); w0 = int(h)*3600+int(m)*60+float(s)
pcm = subprocess.run(["ffmpeg","-v","error","-i",src,"-ac","1","-ar","16000","-f","s16le","-"],capture_output=True,check=True).stdout
a = np.frombuffer(pcm, dtype=np.int16).astype(np.float32)/32768
m = WhisperModel("medium", device="cpu", compute_type="int8", cpu_threads=4)
segs, _ = m.transcribe(a, language="en", word_timestamps=True, vad_filter=False, beam_size=5)
words = [{"w": w.word.strip(), "s": round(w0+w.start,2), "e": round(w0+w.end,2), "p": round(w.probability,2)} for sg in segs for w in sg.words]
json.dump(words, open(out,"w"), ensure_ascii=False, indent=0)
def f(x): return f"{int(x//3600)}:{int(x%3600//60):02d}:{x%60:05.2f}"
print(" | ".join(f"{f(w['s'])} {w['w']}" for w in words))
