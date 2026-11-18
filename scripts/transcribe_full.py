"""Full-stream transcription (PT-BR) with word timestamps, for moment finding.
Usage: python3 scripts/transcribe_full.py work/audio.wav work/transcript_full.json [model] [lang]"""
import json, sys, time, wave
import numpy as np
from faster_whisper import WhisperModel
src, out = sys.argv[1], sys.argv[2]
model_name = sys.argv[3] if len(sys.argv) > 3 else "small"
m = WhisperModel(model_name, device="cpu", compute_type="int8", cpu_threads=4)
with wave.open(src) as wf:
    audio = np.frombuffer(wf.readframes(wf.getnframes()), dtype=np.int16).astype(np.float32) / 32768.0
segs, info = m.transcribe(audio, language=(sys.argv[4] if len(sys.argv) > 4 else "pt"), word_timestamps=True, vad_filter=True,
                          beam_size=1, condition_on_previous_text=False)
res, t0 = [], time.time()
with open(out + ".partial.txt", "w") as log:
    for s in segs:
        res.append({"start": round(s.start, 2), "end": round(s.end, 2), "text": s.text.strip(),
                    "words": [{"w": w.word.strip(), "s": round(w.start, 2), "e": round(w.end, 2), "p": round(w.probability, 2)} for w in (s.words or [])]})
        log.write(f"[{int(s.start//3600):d}:{int(s.start%3600//60):02d}:{int(s.start%60):02d}] {s.text.strip()}\n"); log.flush()
json.dump(res, open(out, "w"), ensure_ascii=False)
print(f"done {len(res)} segments in {time.time()-t0:.0f}s")
