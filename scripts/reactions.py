"""Print streamer reaction lines from chunk files. Usage: reactions.py <chunks_dir> <first> <last>"""
import json, re, sys
d, a, b = sys.argv[1], int(sys.argv[2]), int(sys.argv[3])
f = lambda s: f"{int(s//3600)}:{int(s%3600//60):02d}:{int(s%60):02d}"
pat = re.compile(r"mano|caralho|porra|meu deus|que isso|kkk|puta|nossa|velho|socorro|olha|filho|mds|rapaz|cacete|bicho|não acredito|mentira|jesus|chat|vei|véi|ódio|morri|morreu|atropel|polícia|explod", re.I)
for k in range(a, b + 1):
    try: segs = json.load(open(f"{d}/{k:03d}.json"))
    except FileNotFoundError: break
    for s in segs:
        if len(s["text"]) > 16 and pat.search(s["text"]): print(f(s["start"]), s["text"][:150])
