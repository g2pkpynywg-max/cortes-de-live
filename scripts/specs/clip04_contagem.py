"""Writes clips/clip-04-contagem/spec.json (Bisteconee VOD 2932201544, countdown moment)."""
import json

FACE = {"src": [1260, 240, 660, 318], "dst": [0, 0, 1080, 520]}     # webcam box -> top panel
CD = {"src": [960, 700, 950, 334], "dst": [0, 520, 1080, 380]}      # PS5 countdown timer
STORE = {"src": [140, 550, 1060, 373], "dst": [0, 520, 1080, 380]}  # "Comprar na pré-venda" + R$549,90
DLG = {"src": [400, 180, 1120, 394], "dst": [0, 520, 1080, 380]}    # "Alternar usuário" dialog
ART = {"src": [380, 300, 1120, 394], "dst": [0, 520, 1080, 380]}    # game boot art
FULL = [{"src": [590, 390, 816, 680], "dst": [0, 0, 1080, 900]}]    # full-screen webcam, seated (below the chat overlay)
FULL_STAND = [{"src": [430, 0, 1296, 1080], "dst": [0, 0, 1080, 900]}]  # full-screen webcam, standing
FACE_HI = {"src": [1260, 158, 660, 318], "dst": [0, 0, 1080, 520]}  # he is standing: keep his head in frame
CAM = [{"src": [1350, 158, 510, 425], "dst": [0, 0, 1080, 900]}]    # webcam box only, enlarged

segs = [
    {"in": "0:31:54.30", "out": "0:32:05.30", "panels": [FACE, CD]},
    {"in": "0:32:05.30", "out": "0:32:12.70", "panels": [FACE, STORE], "noFlash": True, "noPunch": True,
     "zooms": [{"at": "0:32:08.18", "scale": 1.06, "hold": 1.6}]},
    {"in": "0:32:41.10", "out": "0:32:45.00", "panels": [FACE, STORE]},
    {"in": "0:32:47.95", "out": "0:32:55.70", "panels": [FACE_HI, STORE],
     "zooms": [{"at": "0:32:50.28", "scale": 1.07, "hold": 1.2}]},
    {"in": "0:32:55.70", "out": "0:32:56.40", "panels": [FACE_HI, DLG], "noFlash": True, "noPunch": True},
    {"in": "0:32:56.40", "out": "0:32:57.20", "panels": FULL_STAND, "noFlash": True, "noPunch": True},
    {"in": "0:33:03.00", "out": "0:33:03.75", "panels": FULL_STAND},
    {"in": "0:33:03.75", "out": "0:33:05.70", "panels": [FACE, ART], "noFlash": True, "noPunch": True},
    {"in": "0:33:13.80", "out": "0:33:20.10", "panels": CAM, "zooms": [{"at": "0:33:15.22", "scale": 1.08, "hold": 1.4}]},
    {"in": "0:33:25.55", "out": "0:33:28.95", "panels": CAM},
    {"in": "0:33:30.80", "out": "0:33:38.70", "panels": FULL, "noFlash": True, "noPunch": True,
     "zooms": [{"at": "0:33:37.48", "scale": 1.1, "hold": 1.2}]},
]


def C(s, e, t, kw=()):
    return {"s": s, "e": e, "t": t, "kw": list(kw)}


caps = [
    C("0:31:54.46", "0:31:55.30", "Meu Deus!", ["Deus"]),
    C("0:32:04.95", "0:32:07.80", "Meu Deus…"),
    C("0:32:07.88", "0:32:09.70", "E… não comprei o jogo.", ["comprei"]),
    C("0:32:09.78", "0:32:11.80", "Fudeu.", ["Fudeu"]),
    C("0:32:11.86", "0:32:12.70", "Puta que pariu!", ["pariu"]),
    C("0:32:41.28", "0:32:42.28", "Guilherme,"),
    C("0:32:42.30", "0:32:43.42", "vou ter que comprar o jogo,", ["comprar"]),
    C("0:32:43.46", "0:32:45.00", "vou baixar o jogo…", ["baixar"]),
    C("0:32:48.16", "0:32:49.45", "Cadê o jogo, mano?", ["jogo"]),
    C("0:32:49.50", "0:32:52.90", "Eu paguei o jogo, caralho!", ["paguei", "caralho"]),
    C("0:32:53.16", "0:32:55.30", "Ai, caralho… o quê, mano?"),
    C("0:32:55.36", "0:32:57.20", "Troquei… como, mano?", ["troquei"]),
    C("0:33:03.28", "0:33:04.50", "Foi!", ["Foi"]),
    C("0:33:04.54", "0:33:05.70", "Jesus amado, mano!", ["Jesus", "amado"]),
    C("0:33:13.94", "0:33:14.90", "Pô, cê tá louco,"),
    C("0:33:14.92", "0:33:16.45", "que susto, mano!", ["susto"]),
    C("0:33:16.50", "0:33:17.24", "Nossa Senhora,"),
    C("0:33:17.26", "0:33:20.10", "meu coração chegou a bater!", ["coração"]),
    C("0:33:25.68", "0:33:26.36", "Mano, não acredito,", ["acredito"]),
    C("0:33:26.38", "0:33:27.75", "eu vou chorar, mano.", ["chorar"]),
    C("0:33:27.80", "0:33:28.95", "Cara, vou chorar…", ["chorar"]),
    C("0:33:32.08", "0:33:34.30", "Cara, eu vou chorar.", ["chorar"]),
    C("0:33:34.40", "0:33:35.64", "Não… agora que eu dei"),
    C("0:33:35.66", "0:33:36.44", "essa piscada forte,", ["piscada"]),
    C("0:33:36.46", "0:33:37.46", "já senti que não vai"),
    C("0:33:37.48", "0:33:38.70", "sair um choro natural.", ["choro", "natural"]),
]


def sec(x):
    h, m, s = x.split(":")
    return int(h) * 3600 + int(m) * 60 + float(s)


said = [("0:31:55.40", "10"), ("0:31:56.36", "9"), ("0:31:57.54", "8"), ("0:31:58.06", "7"), ("0:31:59.32", "6"),
        ("0:32:00.84", "5"), ("0:32:01.98", "4"), ("0:32:02.84", "3"), ("0:32:03.82", "2")]
numbers = []
for i, (t, n) in enumerate(said):
    nxt = sec(said[i + 1][0]) if i + 1 < len(said) else sec("0:32:04.85")
    numbers.append({"s": t, "t": n, "d": round(nxt - sec(t), 2)})

spec = {
    "id": "clip-04-contagem", "language": "pt",
    "src": "work/b2/src/contagem.mov", "windowStart": "0:30:50",
    "stem": "work/b2/stems/htdemucs/contagem/vocals.wav", "wordsFile": "work/b2/words.json",
    "credit": "bisteconee • live de GTA 6 na Twitch",
    "window": {"top": 430, "height": 900}, "captionBottom": 1065, "numTop": 850, "stampTop": 455,
    "hook": {"lines": ["Zerou o GTA 6…", "e pediu pra COMPRAR?!"],
             "title": ["O GTA 6 liberou… e pediu pra COMPRAR?!"],
             "kw": ["COMPRAR"], "size": 66, "titleSize": 46, "top": 188, "noBg": True},
    "segments": segs, "numbers": numbers,
    "stamps": [{"s": "0:32:05.40", "d": 1.9, "t": "COMPRAR?!", "size": 110},
               {"s": "0:33:03.80", "d": 1.8, "t": "ABRIU!", "size": 120}],
    "highlights": [{"s": "0:32:06.60", "d": 2.6, "rect": [18, 1232, 372, 108]}],
    "captions": caps,
}
json.dump(spec, open("clips/clip-04-contagem/spec.json", "w"), ensure_ascii=False, indent=1)
print("spec written")
