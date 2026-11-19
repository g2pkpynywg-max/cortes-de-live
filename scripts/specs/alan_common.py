"""Shared layouts/helpers for the Alanzoka batch (VOD 2932200023). Window: 1080x900 at y=430."""
import json, os

CAM = [1490, 274, 416, 262]          # webcam box in the 1080p stream (above the sub bar)
SRC = "work/alan/src"
STEMS = "work/alan/stems/htdemucs"


def G(x=194, cam=True):
    """Gameplay 8:9 crop (x..x+1296, full height) + webcam inset top-right. x<=194 keeps the stream's own webcam box out."""
    x = min(x, 194)
    p = [{"src": [x, 0, 1296, 1080], "dst": [0, 0, 1080, 900]}]
    if cam:
        p.append({"src": CAM, "dst": [650, 16, 414, 261], "cls": "inset"})
    return p


def GLOW(x=480, y=420, cam=True):
    """Gameplay lower band only (keeps elevated background out of frame) + webcam inset."""
    h = 1080 - y; w = round(h * 1.2)
    p = [{"src": [x, y, w, h], "dst": [0, 0, 1080, 900]}]
    if cam:
        p.append({"src": CAM, "dst": [650, 16, 414, 261], "cls": "inset"})
    return p


def R(gx=420, gy=300):
    """Reaction: webcam big on top, gameplay strip below."""
    return [{"src": [1490, 274, 416, 216], "dst": [0, 0, 1080, 561]},
            {"src": [gx, gy, 1080, 339], "dst": [0, 561, 1080, 339]}]


def source(n, sfx=None):
    s = {"id": n, "file": f"{SRC}/{n}.mov", "stem": f"{STEMS}/{n}/vocals.wav",
         "start": float(open(f"{SRC}/{n}.start").read())}
    if sfx is not None:
        s["sfx"] = {"stems": [f"{STEMS}/{n}/{k}.wav" for k in ("drums", "other", "bass")], "gainDb": sfx}
    return s


def words(*names):
    W = []
    for n in names:
        for f in (f"work/alan/words/{n}.json", f"work/alan/words/{n}_fix.json"):
            if os.path.exists(f):
                W += json.load(open(f))
    W.sort(key=lambda w: w["s"])
    out = "work/alan/words/_merged.json"
    return W


def C(s, e, t, kw=()):
    return {"s": s, "e": e, "t": t, "kw": list(kw)}


def write(clip_id, spec, word_names):
    d = f"clips/{clip_id}"
    os.makedirs(d, exist_ok=True)
    wf = f"{d}/words.json"
    json.dump(words(*word_names), open(wf, "w"), ensure_ascii=False)
    base = {"id": clip_id, "language": "pt", "wordsFile": wf, "credit": "alanzoka • live de GTA 6 na Twitch",
            "window": {"top": 430, "height": 900}, "captionBottom": 1170, "stampTop": 760, "numTop": 760}
    base.update(spec)
    json.dump(base, open(f"{d}/spec.json", "w"), ensure_ascii=False, indent=1)
    print(clip_id, "spec written")
