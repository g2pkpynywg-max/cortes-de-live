"""Build one vertical clip as a HyperFrames project from a spec.

Usage: python3 scripts/build_clip.py clips/<id>/spec.json [--media]

The spec lists the kept source segments (VOD seconds), the crop per segment,
the PT-BR captions (anchored to VOD times of the English words), the hook and
optional overlays. Writes index.html, compositions/overlays.html and
compositions/captions.html. With --media it also cuts assets/video.mp4,
assets/voice.wav (music-free vocal stem, cut and loudness-normalised) and any
cutaway clips.
"""
import html, json, os, re, subprocess, sys

W, H = 1080, 1920
WIN_TOP, WIN_H = 460, 1215          # foreground window (8:9 crop at 1.125x)
SCALE = WIN_H / 1080                # 1.125
FG_W = round(1920 * SCALE)          # 2160
BG_SCALE = H / 1080
BG_W = round(1920 * BG_SCALE)
FPS = 30
CAPTION_LEAD = 0.15
WORDS = []  # optional word-level transcript on the VOD clock (spec "wordsFile")


def hms(t):
    h, m, s = t.split(":")
    return int(h) * 3600 + int(m) * 60 + float(s)


def vod(x):
    return hms(x) if isinstance(x, str) else float(x)


class Timeline:
    def __init__(self, segments):
        self.segs = []
        t = 0.0
        for s in segments:
            a, b = vod(s["in"]), vod(s["out"])
            self.segs.append({**s, "a": a, "b": b, "t0": t})
            t += b - a
        self.duration = round(t, 3)

    def map(self, v, bias="start"):
        v = vod(v)
        for s in self.segs:
            if s["a"] - 1e-3 <= v <= s["b"] + 1e-3:
                return round(s["t0"] + (v - s["a"]), 3)
        # inside a removed gap: snap to the next segment start (or previous end)
        for s in self.segs:
            if v < s["a"]:
                return round(s["t0"], 3)
        return self.duration


def run(cmd):
    subprocess.run(cmd, check=True)


def sources(spec):
    """Single-window specs keep src/stem/windowStart; multi-window specs list "sources"."""
    if "sources" in spec:
        return {x["id"]: x for x in spec["sources"]}
    return {"video": {"id": "video", "file": spec["src"], "stem": spec["stem"], "start": spec["windowStart"]}}


def seg_src(spec, s):
    srcs = sources(spec)
    return srcs[s.get("src", next(iter(srcs)))]


def build_media_multi(spec, d, tl):
    os.makedirs(f"{d}/assets", exist_ok=True)
    srcs = sources(spec)
    for sid, x in srcs.items():
        run(["ffmpeg", "-v", "error", "-y", "-i", x["file"], "-an", "-c:v", "libx264", "-preset", "medium",
             "-crf", "16", "-pix_fmt", "yuv420p", "-r", str(FPS), "-g", "15", "-movflags", "+faststart",
             f"{d}/assets/{sid}.mp4"])
        run(["ffmpeg", "-v", "error", "-y", "-i", x["file"], "-an", "-vf", "crop=ih*9/16:ih,scale=360:640,gblur=sigma=14:steps=2",
             "-c:v", "libx264", "-preset", "medium", "-crf", "24", "-pix_fmt", "yuv420p", "-r", str(FPS), "-g", "15",
             "-movflags", "+faststart", f"{d}/assets/bg_{sid}.mp4"])
    ins, filt, parts = [], [], []
    order = list(srcs)
    for sid in order:
        x = srcs[sid]
        ins += ["-i", x["stem"]]
        sfx = x.get("sfx")  # optional: list of non-vocal stems to keep (game SFX), with gain in dB
        if sfx:
            for f in sfx["stems"]:
                ins += ["-i", f]
    # build per-source mixed input labels
    k = 0
    labels = {}
    for sid in order:
        x = srcs[sid]
        sfx = x.get("sfx")
        if sfx:
            n = 1 + len(sfx["stems"])
            g = 10 ** (sfx.get("gainDb", -6) / 20)
            mixin = "".join(f"[{k + j}:a]" for j in range(n))
            weights = " ".join(["1"] + [f"{g:.3f}"] * (n - 1))
            filt.append(f"{mixin}amix=inputs={n}:weights={weights}:normalize=0[m_{sid}]")
            labels[sid] = f"m_{sid}"
            k += n
        else:
            labels[sid] = f"{k}:a"
            k += 1
    # each segment may reuse a source label; split them
    uses = {}
    for s in tl.segs:
        sid = seg_src(spec, s)["id"]; uses[sid] = uses.get(sid, 0) + 1
    split = {}
    for sid, n in uses.items():
        outs = "".join(f"[{sid}_{j}]" for j in range(n))
        filt.append(f"[{labels[sid]}]asplit={n}{outs}" if n > 1 else f"[{labels[sid]}]anull{outs}")
        split[sid] = 0
    for i, s in enumerate(tl.segs):
        x = seg_src(spec, s); sid = x["id"]
        a0, b0 = s["a"] - vod(x["start"]), s["b"] - vod(x["start"])
        dur = b0 - a0
        filt.append(f"[{sid}_{split[sid]}]atrim={a0:.3f}:{b0:.3f},asetpts=PTS-STARTPTS,"
                    f"afade=t=in:d=0.02,afade=t=out:st={dur - 0.03:.3f}:d=0.03[s{i}]")
        split[sid] += 1
        parts.append(f"[s{i}]")
    filt.append("".join(parts) + f"concat=n={len(parts)}:v=0:a=1[cat]")
    filt.append("[cat]highpass=f=60,lowpass=f=15000,"
                "acompressor=threshold=-20dB:ratio=3:attack=5:release=120:makeup=2,"
                "loudnorm=I=-14:TP=-1.5:LRA=9,aresample=48000[out]")
    run(["ffmpeg", "-v", "error", "-y"] + ins + ["-filter_complex", ";".join(filt),
         "-map", "[out]", "-ac", "2", "-c:a", "pcm_s16le", f"{d}/assets/voice.wav"])


def build_media(spec, d, tl):
    if "sources" in spec:
        return build_media_multi(spec, d, tl)
    os.makedirs(f"{d}/assets", exist_ok=True)
    w0 = vod(spec["windowStart"])
    run(["ffmpeg", "-v", "error", "-y", "-i", spec["src"], "-an", "-c:v", "libx264", "-preset", "medium",
         "-crf", "16", "-pix_fmt", "yuv420p", "-r", str(FPS), "-g", "15", "-movflags", "+faststart",
         f"{d}/assets/video.mp4"])
    # background plate: centre-cover 9:16 at low resolution (blurred later by media-treatment)
    run(["ffmpeg", "-v", "error", "-y", "-i", spec["src"], "-an", "-vf", "crop=ih*9/16:ih,scale=360:640,gblur=sigma=14:steps=2",
         "-c:v", "libx264", "-preset", "medium", "-crf", "24", "-pix_fmt", "yuv420p", "-r", str(FPS), "-g", "15",
         "-movflags", "+faststart", f"{d}/assets/bg.mp4"])
    for c in spec.get("cutaways", []):
        run(["ffmpeg", "-v", "error", "-y", "-i", c["src"], "-an", "-c:v", "libx264", "-preset", "medium",
             "-crf", "16", "-pix_fmt", "yuv420p", "-r", str(FPS), "-g", "15", "-movflags", "+faststart",
             f"{d}/assets/{c['id']}.mp4"])
    # voice: cut each kept range from the vocal stem, short fades at every cut, then process
    parts, filt = [], []
    for i, s in enumerate(tl.segs):
        a, b = s["a"] - w0, s["b"] - w0
        dur = b - a
        filt.append(f"[0:a]atrim={a:.3f}:{b:.3f},asetpts=PTS-STARTPTS,"
                    f"afade=t=in:d=0.02,afade=t=out:st={dur - 0.03:.3f}:d=0.03[s{i}]")
        parts.append(f"[s{i}]")
    filt.append("".join(parts) + f"concat=n={len(parts)}:v=0:a=1[cat]")
    filt.append("[cat]highpass=f=80,lowpass=f=14000,afftdn=nf=-30,"
                "acompressor=threshold=-20dB:ratio=3:attack=5:release=120:makeup=2,"
                "loudnorm=I=-14:TP=-1.5:LRA=9,aresample=48000[out]")
    run(["ffmpeg", "-v", "error", "-y", "-i", spec["stem"], "-filter_complex", ";".join(filt),
         "-map", "[out]", "-ac", "2", "-c:a", "pcm_s16le", f"{d}/assets/voice.wav"])


def esc(s):
    return html.escape(s, quote=True)


def norm(w):
    return re.sub(r"[^\wÀ-ÿ0-9]", "", w.lower())


def kw_spans(text, kws):
    """Return list of (word, is_kw) for a caption text."""
    keys = {norm(k) for k in kws}
    return [(w, norm(w) in keys) for w in text.split()]


def word_times(words, s, e):
    weights = [max(len(w), 2) for w, _ in words]
    tot = sum(weights)
    out, t = [], s
    for wt in weights:
        dt = (e - s) * wt / tot
        out.append(round(t, 3))
        t += dt
    return out


def align_words(cap_words, cs, ce):
    """VOD start time of each caption word, matched in order to WORDS inside [cs-0.3, ce+0.1]."""
    pool = [w for w in WORDS if cs - 0.3 <= w["s"] <= ce + 0.1]
    out, k = [], 0
    for cw in cap_words:
        hit = None
        for j in range(k, min(k + 3, len(pool))):
            if norm(pool[j]["w"]).rstrip("ô") == norm(cw).rstrip("oô") or norm(pool[j]["w"]) == norm(cw):
                hit = j
                break
        if hit is None:
            out.append(None)
        else:
            out.append(pool[hit]["s"])
            k = hit + 1
    # fill gaps by interpolation between known neighbours
    for i, v in enumerate(out):
        if v is None:
            prev = next((out[j] for j in range(i - 1, -1, -1) if out[j] is not None), cs)
            nxt = next((out[j] for j in range(i + 1, len(out)) if out[j] is not None), ce)
            out[i] = prev + (nxt - prev) * 0.5
    return out


def caption_font(text):
    longest = max(len(w) for w in text.split())
    n = len(text)
    size = 78
    # two lines max at ~900px usable width; Archivo Black averages ~0.66em per uppercase char
    while size > 48 and (n * 0.7 * size > 1180 or longest * 0.82 * size > 580):
        size -= 2
    return size


def build_captions(spec, tl):
    groups, js = [], []
    caps = spec["captions"]
    mapped = []
    for c in caps:
        s, e = tl.map(c["s"]), tl.map(c["e"])
        s = max(0.1, s - CAPTION_LEAD)  # show each group slightly before its first word
        if mapped and s < mapped[-1][1]:
            s = max(mapped[-1][0] + 0.25, s)
        mapped.append([s, e, c])
    for i in range(len(mapped) - 1):  # one group at a time
        if mapped[i][1] > mapped[i + 1][0]:
            mapped[i][1] = mapped[i + 1][0]
    for i, (s, e, c) in enumerate(mapped):
        if e - s < 0.25:
            e = s + 0.25
        words = kw_spans(c["t"], c.get("kw", []))
        times = word_times(words, s, e)
        if WORDS:  # word-by-word sync: align caption words in order to the isolated-voice transcript
            if c.get("wt"):  # manual word onsets when the transcript timing is known to be wrong
                got = [vod(x) for x in c["wt"]] + [None] * (len(words) - len(c["wt"]))
            else:
                got = align_words([w for w, _ in words], vod(c["s"]), vod(c["e"]))
            times = [max(s, min(tl.map(g), e - 0.05)) if g is not None else tt for g, tt in zip(got, times)]
            for j in range(1, len(times)):  # keep word pops in order
                times[j] = max(times[j], times[j - 1] + 0.04)
        size = caption_font(c["t"])
        spans = "".join(
            f'<span class="w{" kw" if k else ""}" id="c{i}w{j}">{esc(w)}</span>'
            for j, (w, k) in enumerate(words))
        groups.append(f'      <div class="grp" id="c{i}" data-layout-allow-overlap style="font-size:{size}px">{spans.strip()}</div>')
        js.append(f'    tl.set("#c{i}", {{ visibility: "visible" }}, {s});')
        js.append(f'    tl.fromTo("#c{i}", {{ opacity: 0, y: 26, scale: 0.92 }}, '
                  f'{{ opacity: 1, y: 0, scale: 1, duration: 0.16, ease: "back.out(2.2)" }}, {s});')
        for j, ((w, k), wt) in enumerate(zip(words, times)):
            peak = 1.15 if k else 1.08
            js.append(f'    tl.fromTo("#c{i}w{j}", {{ scale: 1, color: "{ "#FFD400" if k else "#FFFFFF"}" }}, '
                      f'{{ scale: {peak}, color: "{ "#FFE45C" if k else "#FFFFFF"}", duration: 0.07, ease: "power2.out" }}, {wt});')
            js.append(f'    tl.to("#c{i}w{j}", {{ scale: 1, color: "{ "#FFD400" if k else "#FFFFFF"}", duration: 0.18, ease: "power2.inOut" }}, {round(wt + 0.09, 3)});')
        js.append(f'    tl.to("#c{i}", {{ opacity: 0, duration: 0.1, ease: "power2.in" }}, {round(e - 0.1, 3)});')
        js.append(f'    tl.set("#c{i}", {{ opacity: 0, visibility: "hidden" }}, {round(e, 3)});')
    return f"""<template>
  <style>
    #root {{ position: absolute; inset: 0; width: {W}px; height: {H}px; overflow: visible; pointer-events: none; }}
    .grp {{
      position: absolute; left: 120px; width: 660px; bottom: {H - spec.get('captionBottom', 1240)}px;
      text-align: center; line-height: 1.08;
      font-family: "Archivo Black", sans-serif; text-transform: uppercase; letter-spacing: 0.01em;
      opacity: 0; visibility: hidden; overflow: visible;
    }}
    .w {{
      display: inline-block; color: #FFFFFF; transform-origin: 50% 60%; margin: 0 0.18em;
      -webkit-text-stroke: 10px #000; paint-order: stroke fill;
      text-shadow: 0 6px 0 rgba(0,0,0,0.55), 0 10px 26px rgba(0,0,0,0.6);
    }}
    .w.kw {{ color: #FFD400; }}
  </style>
  <div id="root" data-composition-id="captions" data-width="{W}" data-height="{H}" data-layout-allow-overflow>
{chr(10).join(groups)}
  </div>
  <script>
    const tl = gsap.timeline({{ paused: true }});
{chr(10).join(js)}
    window.__timelines["captions"] = tl;
  </script>
</template>
"""


def hook_html(lines, kws, cls):
    keys = {norm(k) for k in kws}
    out = []
    for li, line in enumerate(lines):
        ws = "".join(
            f'<span class="{cls}w{" kw" if norm(w) in keys else ""}">{esc(w)}</span>' for w in line.split())
        out.append(f'<div class="{cls}line">{ws.strip()}</div>')
    return "".join(out)


def build_overlays(spec, tl):
    D = tl.duration
    hook = spec["hook"]
    js, extra = [], []
    # intro hook 0 -> 2.2 s, then it settles into the persistent title bar
    js.append('    tl.set("#flash", { opacity: 0 }, 0);')
    if not hook.get("noBg"):
        js.append('    tl.fromTo("#hookbg", { opacity: 0 }, { opacity: 1, duration: 0.12 }, 0);')
    js.append('    tl.fromTo(".hkw", { opacity: 0, scale: 1.6, y: 30 }, '
              '{ opacity: 1, scale: 1, y: 0, duration: 0.22, ease: "back.out(2.4)", stagger: 0.07 }, 0.05);')
    js.append('    tl.to("#hook", { opacity: 0, scale: 0.9, y: -120, duration: 0.25, ease: "power3.in" }, 2.05);')
    js.append('    tl.to("#hookbg", { opacity: 0, duration: 0.25 }, 2.05);')
    js.append('    tl.fromTo("#title", { opacity: 0, y: -24 }, { opacity: 1, y: 0, duration: 0.3, ease: "power3.out" }, 2.15);')
    js.append('    tl.fromTo("#credit", { opacity: 0 }, { opacity: 1, duration: 0.3 }, 2.3);')
    js.append(f'    tl.fromTo("#bar", {{ scaleX: 0 }}, {{ scaleX: 1, duration: {D}, ease: "none" }}, 0);')
    # flash at every jump cut
    for s in tl.segs[1:]:
        if s.get("noFlash"):
            continue
        t = s["t0"]
        js.append(f'    tl.fromTo("#flash", {{ opacity: 0.38 }}, {{ opacity: 0, duration: 0.18, ease: "power2.out" }}, {t});')
    for c in spec.get("cutaways", []):
        t = tl.map(c["at"])
        d = c["dur"]
        js.append(f'    tl.fromTo("#cutlabel", {{ opacity: 0, x: -30 }}, {{ opacity: 1, x: 0, duration: 0.2, ease: "power3.out" }}, {t});')
        js.append(f'    tl.to("#cutlabel", {{ opacity: 0, duration: 0.15 }}, {round(t + d - 0.2, 3)});')
        js.append(f'    tl.fromTo("#flash", {{ opacity: 0.45 }}, {{ opacity: 0, duration: 0.2 }}, {t});')
        js.append(f'    tl.fromTo("#flash", {{ opacity: 0.3 }}, {{ opacity: 0, duration: 0.2 }}, {round(t + d, 3)});')
        extra.append(f'      <div id="cutlabel">{esc(c["label"])}</div>')
    for i, n in enumerate(spec.get("numbers", [])):
        t = tl.map(n["s"])
        extra.append(f'      <div class="num" id="n{i}">{esc(n["t"])}</div>')
        nd = n.get("d", 0.7)
        ind, outd = round(min(0.18, nd * 0.4), 3), round(min(0.2, nd * 0.4), 3)
        js.append(f'    tl.fromTo("#n{i}", {{ opacity: 0, scale: 2.2 }}, {{ opacity: 1, scale: 1, duration: {ind}, ease: "back.out(2)" }}, {t});')
        js.append(f'    tl.to("#n{i}", {{ opacity: 0, scale: 0.7, duration: {outd}, ease: "power2.in" }}, {round(t + nd - outd, 3)});')
    for i, st in enumerate(spec.get("stamps", [])):
        t = tl.map(st["s"])
        extra.append(f'      <div class="stamp" id="st{i}" style="font-size:{st.get("size", 120)}px">{esc(st["t"])}</div>')
        js.append(f'    tl.fromTo("#st{i}", {{ opacity: 0, scale: 2.6, rotation: -8 }}, {{ opacity: 1, scale: 1, rotation: -4, duration: 0.25, ease: "back.out(2.2)" }}, {t});')
        js.append(f'    tl.to("#st{i}", {{ scale: 1.06, duration: {round(st["d"] - 0.45, 3)}, ease: "sine.inOut" }}, {round(t + 0.25, 3)});')
        js.append(f'    tl.to("#st{i}", {{ opacity: 0, duration: 0.2 }}, {round(t + st["d"] - 0.2, 3)});')
    for i, lb in enumerate(spec.get("labels", [])):  # chapter tag, e.g. "2H36 DE LIVE"
        t = tl.map(lb["s"])
        extra.append(f'      <div class="lbl" id="lb{i}">{esc(lb["t"])}</div>')
        js.append(f'    tl.fromTo("#lb{i}", {{ opacity: 0, x: -30 }}, {{ opacity: 1, x: 0, duration: 0.2, ease: "power3.out" }}, {t});')
        js.append(f'    tl.to("#lb{i}", {{ opacity: 0, duration: 0.15 }}, {round(t + lb.get("d", 2.0) - 0.15, 3)});')
    for i, h in enumerate(spec.get("highlights", [])):  # pulsing box around a key on-screen detail
        t = tl.map(h["s"]); x, y, w, hh = h["rect"]
        extra.append(f'      <div class="hl" id="hl{i}" data-layout-ignore style="left:{x}px;top:{y}px;width:{w}px;height:{hh}px"></div>')
        js.append(f'    tl.fromTo("#hl{i}", {{ opacity: 0, scale: 1.5 }}, {{ opacity: 1, scale: 1, duration: 0.22, ease: "back.out(2)" }}, {t});')
        js.append(f'    tl.to("#hl{i}", {{ scale: 1.06, duration: 0.3, ease: "sine.inOut", yoyo: true, repeat: {max(1, int(h["d"] / 0.3) - 2)} }}, {round(t + 0.22, 3)});')
        js.append(f'    tl.to("#hl{i}", {{ opacity: 0, duration: 0.2 }}, {round(t + h["d"] - 0.2, 3)});')
    return f"""<template>
  <style>
    #root {{ position: absolute; inset: 0; width: {W}px; height: {H}px; pointer-events: none; }}
    .lbl {{ position: absolute; left: 140px; top: {WIN_TOP + 24}px; padding: 10px 20px; border-radius: 12px;
      background: #FFD400; color: #000; font-family: "Inter", sans-serif; font-weight: 900; font-size: 32px; opacity: 0; }}
    .hl {{ position: absolute; border: 9px solid #FFD400; border-radius: 22px; opacity: 0;
      box-shadow: 0 0 0 4px rgba(0,0,0,0.6), 0 0 30px rgba(255,212,0,0.7); }}
    #flash {{ position: absolute; left: 0; top: {WIN_TOP}px; width: {W}px; height: {WIN_H}px; background: #fff; opacity: 0; }}
    #hookbg {{ position: absolute; left: 0; top: {WIN_TOP}px; width: {W}px; height: {WIN_H}px;
      background: linear-gradient(180deg, rgba(0,0,0,0.72) 0%, rgba(0,0,0,0.35) 55%, rgba(0,0,0,0) 100%); opacity: 0; }}
    #hook {{ position: absolute; left: 120px; width: 768px; top: {hook.get('top', 500)}px; text-align: center; }}
    .hkline {{ font-family: "Archivo Black", sans-serif; font-size: {hook.get('size', 92)}px; line-height: 1.05;
      text-transform: uppercase; color: #fff; }}
    .hkw {{ display: inline-block; margin: 0 0.13em; -webkit-text-stroke: 12px #000; paint-order: stroke fill;
      text-shadow: 0 8px 0 rgba(0,0,0,0.5); }}
    .hkw.kw {{ color: #FFD400; }}
    #title {{ position: absolute; left: 120px; width: 768px; top: 296px; text-align: center; opacity: 0; }}
    .tlline {{ font-family: "Archivo Black", sans-serif; font-size: {hook.get('titleSize', 52)}px; line-height: 1.08;
      text-transform: uppercase; color: #fff; }}
    .tlw {{ display: inline-block; margin: 0 0.12em; }}
    .tlw.kw {{ color: #FFD400; }}
    #credit {{ position: absolute; left: 120px; width: 768px; top: 412px; text-align: center; opacity: 0;
      font-family: "Inter", sans-serif; font-weight: 700; font-size: 28px; letter-spacing: 0.08em;
      color: rgba(255,255,255,0.78); text-transform: uppercase; }}
    #barbase {{ position: absolute; left: 0; top: {WIN_TOP + WIN_H}px; width: {W}px; height: 8px; background: rgba(255,255,255,0.18); }}
    #bar {{ position: absolute; left: 0; top: {WIN_TOP + WIN_H}px; width: {W}px; height: 8px; background: #FFD400; transform-origin: 0 50%; }}
    #cutlabel {{ position: absolute; left: 140px; top: {WIN_TOP + 30}px; padding: 10px 20px; border-radius: 12px;
      background: #FFD400; color: #000; font-family: "Inter", sans-serif; font-weight: 900; font-size: 32px; opacity: 0; }}
    .num {{ position: absolute; left: 120px; width: 768px; top: {spec.get('numTop', 520)}px; text-align: center; opacity: 0;
      font-family: "Archivo Black", sans-serif; font-size: 300px; line-height: 1; color: #FFD400;
      -webkit-text-stroke: 16px #000; paint-order: stroke fill; text-shadow: 0 14px 0 rgba(0,0,0,0.5); }}
    .stamp {{ position: absolute; left: 120px; width: 768px; top: {spec.get('stampTop', 640)}px; text-align: center; opacity: 0;
      font-family: "Archivo Black", sans-serif; font-size: 120px; line-height: 1; color: #FFD400;
      -webkit-text-stroke: 14px #000; paint-order: stroke fill; text-shadow: 0 12px 0 rgba(0,0,0,0.5); }}
  </style>
  <div id="root" data-composition-id="overlays" data-width="{W}" data-height="{H}" data-layout-allow-overflow data-layout-allow-overlap>
      <div id="flash"></div>
      <div id="hookbg"></div>
      <div id="hook">{hook_html(hook['lines'], hook.get('kw', []), 'hk')}</div>
      <div id="title">{hook_html(hook.get('title', hook['lines']), hook.get('kw', []), 'tl')}</div>
      <div id="credit">{esc(spec['credit'])}</div>
      <div id="barbase"></div>
      <div id="bar"></div>
{chr(10).join(extra)}
  </div>
  <script>
    const tl = gsap.timeline({{ paused: true }});
{chr(10).join(js)}
    window.__timelines["overlays"] = tl;
  </script>
</template>
"""


def build_index(spec, tl):
    D = tl.duration
    bg, fg, js = [], [], []
    multi = "sources" in spec
    for i, s in enumerate(tl.segs):
        x = seg_src(spec, s)
        vsrc = f"assets/{x['id']}.mp4" if multi else "assets/video.mp4"
        bsrc = f"assets/bg_{x['id']}.mp4" if multi else "assets/bg.mp4"
        ms = round(s["a"] - vod(x["start"]), 3)
        dur = round(s["b"] - s["a"], 3)
        t0 = round(s["t0"], 3)
        cx = s.get("cropX", 480)
        bg.append(f'      <video id="bg{i}" class="clip bgv" src="{bsrc}" data-start="{t0}" data-duration="{dur}" '
                  f'data-media-start="{ms}" data-track-index="0" muted playsinline></video>')
        if "panels" in s:
            # each panel crops a source rect [x,y,w,h] (1920x1080 px) into a window rect [x,y,w,h]
            inner = []
            for k, pnl in enumerate(s["panels"]):
                sx, sy, sw, sh = pnl["src"]
                dx, dy, dw, dh = pnl["dst"]
                sc = dw / sw
                inner.append(
                    f'<div class="pnl{" " + pnl["cls"] if pnl.get("cls") else ""}" id="p{i}_{k}" data-layout-allow-overflow style="left:{dx}px;top:{dy}px;width:{dw}px;height:{dh}px">'
                    f'<video id="fg{i}_{k}" class="clip" src="{vsrc}" data-start="{t0}" data-duration="{dur}" '
                    f'data-media-start="{ms}" data-track-index="{1 + k}" muted playsinline '
                    f'style="position:absolute;left:{-round(sx * sc, 1)}px;top:{-round(sy * sc, 1)}px;width:{round(1920 * sc, 1)}px;height:{round(1080 * sc, 1)}px"></video></div>')
            fg.append(f'        <div class="seg" id="sw{i}" data-layout-allow-overflow>{"".join(inner)}</div>')
            # panel frames (e.g. the webcam inset border) only show while their segment plays
            js.append(f'    tl.set("#sw{i}", {{ opacity: {1 if i == 0 else 0} }}, 0);')
            if i > 0:
                js.append(f'    tl.set("#sw{i}", {{ opacity: 1 }}, {t0});')
            js.append(f'    tl.set("#sw{i}", {{ opacity: 0 }}, {round(t0 + dur, 3)});')
        else:
            fg.append(f'        <div class="seg" id="sw{i}" data-layout-allow-overflow><div class="pan" id="pan{i}" data-layout-allow-overflow>'
                      f'<video id="fg{i}" class="clip fgv" src="{vsrc}" data-start="{t0}" data-duration="{dur}" '
                      f'data-media-start="{ms}" data-track-index="1" muted playsinline></video></div></div>')
            js.append(f'    tl.set("#pan{i}", {{ x: {-round(cx * SCALE)} }}, 0);')
        for k in s.get("pan", []):  # [{"at": vod, "cropX": px, "dur": s}]
            js.append(f'    tl.to("#pan{i}", {{ x: {-round(k["cropX"] * SCALE)}, duration: {k.get("dur", 0.6)}, ease: "power2.inOut" }}, {tl.map(k["at"])});')
        # punch-in at the start of every segment (bigger one on the opening shot)
        p = 1.14 if i == 0 else 1.06
        pd = 2.0 if i == 0 else 0.4
        if not s.get("noPunch"):
            js.append(f'    tl.fromTo("#sw{i}", {{ scale: {p} }}, {{ scale: 1, duration: {pd}, ease: "power2.out" }}, {t0});')
        for z in s.get("zooms", []):  # emphasis punch-ins: {"at": vod, "scale": 1.12, "hold": 1.0}
            t = tl.map(z["at"])
            js.append(f'    tl.to("#sw{i}", {{ scale: {z.get("scale", 1.1)}, duration: 0.18, ease: "power3.out" }}, {t});')
            js.append(f'    tl.to("#sw{i}", {{ scale: 1, duration: 0.5, ease: "power2.inOut" }}, {round(t + z.get("hold", 1.0), 3)});')
    for c in spec.get("cutaways", []):
        t = tl.map(c["at"])
        fg.append(f'        <div class="seg cut" id="cw-{c["id"]}" data-layout-allow-overflow><div class="pan" id="cp-{c["id"]}" data-layout-allow-overflow>'
                  f'<video id="cv-{c["id"]}" class="clip fgv" src="assets/{c["id"]}.mp4" data-start="{t}" data-duration="{c["dur"]}" '
                  f'data-media-start="{c["mediaStart"]}" data-track-index="2" muted playsinline></video></div></div>')
        js.append(f'    tl.set("#cp-{c["id"]}", {{ x: {-round(c.get("cropX", 480) * SCALE)} }}, 0);')
        js.append(f'    tl.fromTo("#cw-{c["id"]}", {{ scale: 1.12 }}, {{ scale: 1, duration: {c["dur"]}, ease: "power1.out" }}, {t});')
    return f"""<!doctype html>
<html lang="pt-BR" data-resolution="portrait">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width={W}, height={H}" />
    <script src="https://cdn.jsdelivr.net/npm/gsap@3.15.0/dist/gsap.min.js"></script>
    <style>
      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      html, body {{ width: {W}px; height: {H}px; overflow: hidden; background: #000; }}
      #root {{ position: relative; width: {W}px; height: {H}px; overflow: hidden; background: #000; }}
      .bgv {{ position: absolute; top: 0; left: 0; width: {W}px; height: {H}px; }}
      #dim {{ position: absolute; inset: 0; background: rgba(0,0,0,0.5); }}
      #win {{ position: absolute; left: 0; top: {WIN_TOP}px; width: {W}px; height: {WIN_H}px; overflow: hidden; }}
      .seg {{ position: absolute; inset: 0; overflow: hidden; transform-origin: 50% 45%; }}
      .pan {{ position: absolute; top: 0; left: 0; width: {FG_W}px; height: {WIN_H}px; }}
      .fgv {{ position: absolute; top: 0; left: 0; width: {FG_W}px; height: {WIN_H}px; }}
      .pnl {{ position: absolute; overflow: hidden; }}
      .pnl.inset {{ border: 6px solid #FFD400; border-radius: 22px; box-shadow: 0 10px 30px rgba(0,0,0,0.6); }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{D}" data-width="{W}" data-height="{H}" data-fps="{FPS}">
{chr(10).join(bg)}
      <div id="dim"></div>
      <div id="win" data-layout-allow-overflow>
{chr(10).join(fg)}
      </div>
      <div id="overlays" class="clip" data-composition-id="overlays" data-composition-src="compositions/overlays.html"
        data-start="0" data-duration="{D}" data-track-index="3" data-track-kind="graphics" data-width="{W}" data-height="{H}"></div>
      <div id="captions" class="clip" data-composition-id="captions" data-composition-src="compositions/captions.html"
        data-start="0" data-duration="{D}" data-track-index="4" data-track-kind="captions" data-width="{W}" data-height="{H}"></div>
      <audio id="voice" class="clip" src="assets/voice.wav" data-start="0" data-duration="{D}" data-track-index="5" data-volume="1"></audio>
    </div>
    <script>
      const tl = gsap.timeline({{ paused: true }});
{chr(10).join(js)}
      window.__timelines["main"] = tl;
    </script>
  </body>
</html>
"""


def main():
    global WIN_TOP, WIN_H
    spec_path = sys.argv[1]
    d = os.path.dirname(spec_path)
    spec = json.load(open(spec_path))
    if "window" in spec:  # optional per-clip foreground window
        WIN_TOP, WIN_H = spec["window"]["top"], spec["window"]["height"]
    tl = Timeline(spec["segments"])
    if "--media" in sys.argv:
        build_media(spec, d, tl)
    os.makedirs(f"{d}/compositions", exist_ok=True)
    if spec.get("wordsFile"):
        WORDS.extend(json.load(open(spec["wordsFile"])))
    open(f"{d}/index.html", "w").write(build_index(spec, tl))
    open(f"{d}/compositions/overlays.html", "w").write(build_overlays(spec, tl))
    open(f"{d}/compositions/captions.html", "w").write(build_captions(spec, tl))
    # The background plate's blur is baked into assets/bg.mp4 at cut time (gblur): the
    # media-treatment WebGL blur costs ~12 s/frame on a CPU-only renderer. Opt back in with --treatment.
    if "--treatment" in sys.argv:
      subprocess.run(["node", "/root/.claude/skills/hyperframes/scripts/plugin-cli.mjs", "media-treatment",
                    "--project", d, "--selector", ".bgv", "--grading", '{"effects":{"blur":0.7}}',
                    "--apply", "--json"], check=True, capture_output=True)
    print(f"{spec['id']}: duration {tl.duration:.2f}s, {len(tl.segs)} segments, {len(spec['captions'])} captions")


if __name__ == "__main__":
    main()
