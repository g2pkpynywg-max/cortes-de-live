"""Chunked full-stream transcription for very long VODs (keeps VAD fast and memory low).
Usage: transcribe_chunked.py <audio16k.wav> <out.json> [model] [lang] [chunk_s]
Writes <out.json>.partial.txt as it goes and resumes from finished chunks in <out.json>.chunks/."""
import json, os, sys, time, wave
import numpy as np
from faster_whisper import WhisperModel
src, out = sys.argv[1], sys.argv[2]
model = sys.argv[3] if len(sys.argv) > 3 else "small"
lang = sys.argv[4] if len(sys.argv) > 4 else "pt"
chunk = int(sys.argv[5]) if len(sys.argv) > 5 else 1800
cdir = out + ".chunks"; os.makedirs(cdir, exist_ok=True)
m = WhisperModel(model, device="cpu", compute_type="int8", cpu_threads=4)
wf = wave.open(src); sr = wf.getframerate(); total = wf.getnframes() / sr
fmt = lambda s: f"[{int(s//3600)}:{int(s%3600//60):02d}:{int(s%60):02d}]"
t0 = time.time(); allseg = []
for k, off in enumerate(range(0, int(total) + 1, chunk)):
    cf = f"{cdir}/{k:03d}.json"
    if not os.path.exists(cf):
        wf.setpos(int(off * sr))
        a = np.frombuffer(wf.readframes(int(chunk * sr)), dtype=np.int16).astype(np.float32) / 32768.0
        segs, _ = m.transcribe(a, language=lang, word_timestamps=True, vad_filter=True,
                               beam_size=1, condition_on_previous_text=False)
        res = [{"start": round(off + s.start, 2), "end": round(off + s.end, 2), "text": s.text.strip(),
                "words": [{"w": w.word.strip(), "s": round(off + w.start, 2), "e": round(off + w.end, 2)} for w in (s.words or [])]}
               for s in segs]
        json.dump(res, open(cf, "w"), ensure_ascii=False)
        with open(out + ".partial.txt", "a") as log:
            for s in res: log.write(f"{fmt(s['start'])} {s['text']}\n")
        print(f"chunk {k} @{off}s done ({len(res)} segs, {time.time()-t0:.0f}s elapsed)", flush=True)
    allseg += json.load(open(cf))
json.dump(allseg, open(out, "w"), ensure_ascii=False)
print(f"done {len(allseg)} segments in {time.time()-t0:.0f}s")
