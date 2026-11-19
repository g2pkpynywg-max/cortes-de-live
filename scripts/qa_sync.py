"""QA: re-transcribe the clip's final voice track and compare word onsets with caption windows.
Usage: qa_sync.py clips/<id>/spec.json"""
import json, sys, re, subprocess, numpy as np
sys.path.insert(0, 'scripts')
from build_clip import Timeline
from faster_whisper import WhisperModel
spec = json.load(open(sys.argv[1])); d = sys.argv[1].rsplit('/', 1)[0]
tl = Timeline(spec['segments'])
pcm = subprocess.run(["ffmpeg","-v","error","-i",f"{d}/assets/voice.wav","-ac","1","-ar","16000","-f","s16le","-"],capture_output=True,check=True).stdout
a = np.frombuffer(pcm, dtype=np.int16).astype(np.float32)/32768
m = WhisperModel("small", device="cpu", compute_type="int8")
segs, _ = m.transcribe(a, language=spec.get("language", "en"), word_timestamps=True, beam_size=5)
words = [(w.start, w.end, w.word.strip()) for s in segs for w in s.words]
dur = len(a)/16000
caps = [(tl.map(c['s']), tl.map(c['e']), c['t']) for c in spec['captions']]
offs, uncovered = [], []
for s, e, t in caps:
    inside = [w for w in words if w[0] >= s - 0.6 and w[0] < e]
    if inside: offs.append(inside[0][0] - s)
for w in words:  # speech with no caption on screen (numbers handled as overlay)
    if not any(s - 0.25 <= w[0] <= e + 0.1 for s, e, _ in caps) and not re.fullmatch(r"\d+[,.]?|one|two|three|four|five|six|seven|eight|play|the|game\.?", w[2].lower()) and not spec.get("ignoreUncaptioned"):
        uncovered.append(f"{w[0]:.2f}s '{w[2]}'")
offs = np.array(offs)
print(f"{spec['id']}: audio {dur:.2f}s vs timeline {tl.duration:.2f}s | captions {len(caps)} | "
      f"onset offset mean {offs.mean()*1000:+.0f} ms, max |{np.abs(offs).max()*1000:.0f}| ms")
print("  speech without caption:", uncovered or "none")
