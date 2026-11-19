"""Word-level PT transcription of isolated vocals for each window, VOD clock. Usage: transcribe_windows.py <stems_dir> <src_dir> <out_dir> name..."""
import json, subprocess, sys, os, numpy as np
from faster_whisper import WhisperModel
stems, srcd, out = sys.argv[1], sys.argv[2], sys.argv[3]
os.makedirs(out, exist_ok=True)
m = WhisperModel("medium", device="cpu", compute_type="int8", cpu_threads=4)
f = lambda x: f"{int(x//3600)}:{int(x%3600//60):02d}:{x%60:05.2f}"
for n in sys.argv[4:]:
    if os.path.exists(f"{out}/{n}.json"): continue
    v0 = float(open(f"{srcd}/{n}.start").read())
    pcm = subprocess.run(["ffmpeg", "-v", "error", "-i", f"{stems}/{n}/vocals.wav", "-ac", "1", "-ar", "16000", "-f", "s16le", "-"], capture_output=True, check=True).stdout
    a = np.frombuffer(pcm, dtype=np.int16).astype(np.float32) / 32768
    segs, _ = m.transcribe(a, language="pt", word_timestamps=True, vad_filter=True, beam_size=5)
    W = [{"w": w.word.strip(), "s": round(v0 + w.start, 2), "e": round(v0 + w.end, 2)} for s in segs for w in s.words]
    json.dump(W, open(f"{out}/{n}.json", "w"), ensure_ascii=False)
    print(f"== {n}\n" + " | ".join(f"{f(w['s'])} {w['w']}" for w in W), flush=True)
