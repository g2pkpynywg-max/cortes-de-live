import sys; sys.path.insert(0, "scripts/specs")
from alan_common import *

segs = [
    {"src": "c2", "in": "5:08:40.30", "out": "5:09:00.20", "panels": G(),
     "zooms": [{"at": "5:08:47.79", "scale": 1.07, "hold": 1.4}]},
    {"src": "c2", "in": "5:09:01.55", "out": "5:09:09.00", "panels": G(),
     "zooms": [{"at": "5:09:03.55", "scale": 1.08, "hold": 1.5}]},
    {"src": "c2", "in": "5:09:44.90", "out": "5:10:00.70", "panels": R(300, 300),
     "zooms": [{"at": "5:09:46.55", "scale": 1.06, "hold": 1.4}, {"at": "5:09:56.83", "scale": 1.08, "hold": 1.6}]},
    {"src": "c2", "in": "5:11:06.40", "out": "5:11:15.60", "panels": G(),
     "zooms": [{"at": "5:11:13.32", "scale": 1.08, "hold": 1.6}]},
]
caps = [
    C("5:08:40.47", "5:08:41.70", "Que isso, que isso?"),
    C("5:08:41.77", "5:08:47.70", "Polícia! Polícia! Polícia! Polícia!", ["Polícia"]),
    C("5:08:47.79", "5:08:50.70", "Meu Deus, eu atropelei alguém sem querer.", ["atropelei", "sem", "querer"]),
    C("5:08:50.81", "5:08:55.50", "Polícia! Meu Deus! Polícia!", ["Polícia"]),
    C("5:08:55.61", "5:08:58.40", "Nossa! Meu Deus, gente, para de entrar na frente do meu carro,", ["frente"]),
    C("5:08:58.51", "5:09:00.20", "eu vou ser preso, pelo amor de Deus!", ["preso"]),
    C("5:09:01.69", "5:09:03.50", "O cara começou a me dar tiro, eu fui fugir,", ["tiro"]),
    C("5:09:03.55", "5:09:05.20", "atropelei 8 pessoas no meio do caminho!", ["8", "pessoas"]),
    C("5:09:07.47", "5:09:09.00", "Aí, agora fudeu, mano!", ["fudeu"]),
    C("5:09:45.13", "5:09:46.50", "Mano, na moral, cara,"),
    C("5:09:46.55", "5:09:48.70", "eu só queria comprar flor pra minha esposa.", ["flor", "esposa"]),
    C("5:09:48.79", "5:09:50.55", "Daí, no meio do caminho, eu tomo uma fechada,", ["fechada"]),
    C("5:09:50.61", "5:09:52.40", "o cara me arregaça na bala.", ["bala"]),
    C("5:09:52.49", "5:09:55.55", "Eu, pra fugir, porque eu sou um cara que eu não procuro briga…", ["briga"]),
    C("5:09:55.65", "5:09:58.25", "Eu fui fugir, atropelo 8 pessoas no caminho,", ["8", "pessoas"]),
    C("5:09:58.33", "5:10:00.70", "contra a minha vontade, e eu tô errado.", ["errado"]),
    C("5:11:10.92", "5:11:12.60", "Mano, isso daqui é o departamento de polícia?", ["polícia"]),
    C("5:11:12.66", "5:11:15.60", "Ah, que legal, eu atropelei 8 pessoas na frente da polícia, mano, ainda.", ["frente", "polícia"]),
]
write("alan/clip-02-flor", {
    "sources": [source("c2")],
    "hook": {"lines": ["Só queria comprar", "FLOR pra esposa…"], "title": ["Ele só queria comprar FLOR pra esposa…"],
             "kw": ["FLOR"], "size": 66, "titleSize": 46, "top": 290, "noBg": True},
    "stamps": [{"s": "5:09:04.07", "d": 1.6, "t": "8 PESSOAS!", "size": 110}],
    "segments": segs, "captions": caps,
}, ["c2"])
