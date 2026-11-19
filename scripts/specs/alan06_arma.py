import sys; sys.path.insert(0, "scripts/specs")
from alan_common import *

segs = [
    {"src": "c6", "in": "12:05:57.90", "out": "12:06:03.35", "panels": G(0)},
    {"src": "c6", "in": "12:06:07.15", "out": "12:06:11.50", "panels": G(0), "noFlash": True,
     "zooms": [{"at": "12:06:10.39", "scale": 1.06, "hold": 1.0}]},
    {"src": "c6", "in": "12:06:25.80", "out": "12:06:35.20", "panels": G(0),
     "zooms": [{"at": "12:06:32.63", "scale": 1.08, "hold": 1.6}]},
    {"src": "c6", "in": "12:06:40.80", "out": "12:06:47.50", "panels": G(0)},
    {"src": "c6", "in": "12:07:05.60", "out": "12:07:10.80", "panels": G(0),
     "zooms": [{"at": "12:07:09.14", "scale": 1.1, "hold": 1.4}]},
]
caps = [
    C("12:05:58.03", "12:05:58.70", "Comprei, chat."),
    C("12:05:58.75", "12:06:00.95", "Viajei aqui, perdi a mão, perdi a mão, mano.", ["perdi", "mão"]),
    {"s": "12:06:02.15", "e": "12:06:03.35", "t": "Viajei, viajei.", "kw": ["Viajei"], "wt": ["12:06:02.20", "12:06:02.75"]},
    C("12:06:07.27", "12:06:09.85", "“Comprar o componente necessário”, comprei.", ["comprei"]),
    C("12:06:09.93", "12:06:11.50", "Nossa, eu tô gastando todo o meu dinheiro, mano.", ["dinheiro"]),
    C("12:06:26.01", "12:06:28.60", "Nossa, chat, eu gastei todo o meu dinheiro montando uma arma, me arrependi, mano.", ["arrependi"]),
    C("12:06:31.95", "12:06:33.90", "Cara, caralho, eu gastei todo o meu dinheiro…", ["todo", "dinheiro"]),
    C("12:06:33.97", "12:06:35.20", "mas a arma ficou linda.", ["linda"]),
    C("12:06:41.11", "12:06:42.25", "Gastei literalmente todo o meu dinheiro…", ["literalmente"]),
    C("12:06:42.33", "12:06:44.60", "mas a arma ficou linda.", ["linda"]),
    C("12:07:06.64", "12:07:09.05", "Nossa, é… bala, mano, a arma…", ["bala"]),
    C("12:07:09.14", "12:07:10.80", "Eu não comprei bala, mano.", ["não", "comprei", "bala"]),
]
write("alan/clip-06-arma", {
    "sources": [source("c6", sfx=-6)],
    "hook": {"lines": ["Gastou TUDO", "na arma dos sonhos…"], "title": ["Gastou TUDO na arma… e esqueceu a BALA"],
             "kw": ["TUDO", "BALA"], "size": 64, "titleSize": 44, "top": 290, "noBg": True},
    "stamps": [{"s": "12:07:09.20", "d": 1.6, "t": "SEM BALA!", "size": 110}],
    "segments": segs, "captions": caps,
}, ["c6"])
