import sys; sys.path.insert(0, "scripts/specs")
from alan_common import *

# Lower-band crop only (y>=420): NPCs dancing topless on the tables stay above the frame.
P = GLOW(500, 420)
segs = [
    {"src": "c3", "in": "9:53:44.90", "out": "9:54:08.60", "panels": P,
     "zooms": [{"at": "9:54:00.89", "scale": 1.07, "hold": 1.4}]},
    {"src": "c3", "in": "9:54:13.40", "out": "9:54:22.60", "panels": P,
     "zooms": [{"at": "9:54:16.44", "scale": 1.07, "hold": 1.2}]},
    {"src": "c3", "in": "9:54:29.00", "out": "9:54:41.00", "panels": P},
    {"src": "c3", "in": "9:54:49.20", "out": "9:54:51.30", "panels": P},
]
caps = [
    C("9:53:45.53", "9:53:46.90", "Caralho!", ["Caralho"]),
    C("9:53:46.97", "9:53:49.10", "Não, aí você viajou, aí você viajou pra caralho.", ["viajou"]),
    C("9:53:50.47", "9:53:52.80", "Vai pra casa do caralho, porra, aí você viajou, aí você viajou.", ["viajou"]),
    C("9:53:52.85", "9:53:54.15", "Você é o outro, você é o…"),
    C("9:53:54.19", "9:53:56.80", "Não, não, não, você viajou, você viajou…", ["viajou"]),
    C("9:53:56.85", "9:53:58.80", "Você viajou, cara, você viajou!", ["viajou"]),
    C("9:53:59.39", "9:54:00.85", "Mano, o cara é bom, esse cara é o quê?", ["bom"]),
    C("9:54:00.89", "9:54:03.60", "Acelino Popó Freitas, mano!", ["Popó", "Freitas"]),
    C("9:54:03.67", "9:54:05.60", "O que é isso, mano? É o Popó!", ["Popó"]),
    C("9:54:05.67", "9:54:08.60", "O que é isso? É o Popó!", ["Popó"]),
    C("9:54:13.62", "9:54:16.40", "Boa, boa, nossa, que é o doido na piscina, mano!", ["piscina"]),
    C("9:54:16.44", "9:54:19.50", "Mano, o cara voltou da piscina!", ["voltou"]),
    C("9:54:21.59", "9:54:22.60", "Mano, eu tô sendo arregaçado!", ["arregaçado"]),
    C("9:54:29.21", "9:54:31.90", "O outro vai também. Vem, vem, vem, vem!", ["vem"]),
    C("9:54:31.93", "9:54:33.95", "Toma, toma, toma, toma, toma!", ["toma"]),
    C("9:54:34.01", "9:54:36.10", "Vai pra porra da piscina de novo, seu filho da puta!", ["piscina"]),
    C("9:54:36.15", "9:54:37.40", "Você é o outro, você é o outro, vai!"),
    C("9:54:37.43", "9:54:39.45", "Larga meu parceiro, larga meu parceiro, toma!", ["parceiro"]),
    C("9:54:39.53", "9:54:41.00", "Toma, larga meu parceiro, toma!", ["parceiro"]),
    C("9:54:49.39", "9:54:51.30", "Vai! Desmaiou o cara, mano, desmaiou o cara.", ["desmaiou"]),
]
write("alan/clip-03-festa", {
    "sources": [source("c3", sfx=-4)],
    "hook": {"lines": ["Invadiu a festa", "ERRADA no GTA 6"], "title": ["Invadiu a festa ERRADA no GTA 6"],
             "kw": ["ERRADA"], "size": 72, "titleSize": 46, "top": 290, "noBg": True},
    "stamps": [{"s": "9:54:01.13", "d": 1.6, "t": "POPÓ?!", "size": 120}],
    "segments": segs, "captions": caps, "captionBottom": 1100,
}, ["c3"])
