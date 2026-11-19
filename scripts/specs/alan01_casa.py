import sys; sys.path.insert(0, "scripts/specs")
from alan_common import *

segs = [
    {"src": "c1a", "in": "3:22:26.00", "out": "3:22:31.40", "panels": G()},
    {"src": "c1b", "in": "3:29:04.60", "out": "3:29:23.00", "panels": G(),
     "zooms": [{"at": "3:29:08.24", "scale": 1.07, "hold": 1.4}]},
    {"src": "c1b", "in": "3:29:26.50", "out": "3:29:31.00", "panels": G()},
    {"src": "c1c", "in": "14:52:52.55", "out": "14:52:56.30", "panels": G()},
    {"src": "c1c", "in": "14:53:19.80", "out": "14:53:31.00", "panels": G(), "noFlash": True,
     "zooms": [{"at": "14:53:26.39", "scale": 1.07, "hold": 1.6}]},
    {"src": "c1d", "in": "15:18:17.95", "out": "15:18:25.70", "panels": R(500, 260),
     "zooms": [{"at": "15:18:20.52", "scale": 1.06, "hold": 1.6}]},
]
caps = [
    C("3:22:26.21", "3:22:27.95", "Ô, minha casa tá ficando show, mano!", ["show"]),
    C("3:22:28.07", "3:22:31.40", "Olha, botou até o ventilador pra secar mais rápido a tinta, mano.", ["ventilador", "tinta"]),
    C("3:29:04.78", "3:29:06.45", "Meu Deus do céu, chat, não é possível, mano,"),
    C("3:29:06.50", "3:29:08.10", "vou arrumar o telhado agora, mano!", ["telhado"]),
    C("3:29:08.24", "3:29:10.70", "Eu vou ficar arrumando minha casa!", ["casa"]),
    C("3:29:10.80", "3:29:14.40", "É o que eu gosto, eu gosto, pô!", ["gosto"]),
    C("3:29:14.48", "3:29:17.80", "Fazer o quê?"),
    C("3:29:17.88", "3:29:20.05", "É a vida, mano!", ["vida"]),
    C("3:29:20.10", "3:29:23.00", "É a vida, que jogo bom, é isso!", ["jogo", "bom"]),
    C("3:29:26.66", "3:29:28.85", "Quero saber de roubar ninguém, não,", ["roubar"]),
    C("3:29:28.90", "3:29:31.00", "quero só arrumar minha casa.", ["arrumar", "casa"]),
    C("14:52:52.75", "14:52:54.85", "Meu Deus! Botaram fogo na minha…", ["fogo"]),
    C("14:52:54.91", "14:52:56.30", "cara, minha cobra! Meu Deus!", ["cobra"]),
    C("14:53:26.39", "14:53:28.65", "A cobra! Minha cobra!", ["cobra"]),
    C("14:53:28.73", "14:53:31.00", "Ela vai fugir, pelo menos.", ["fugir"]),
    C("15:18:18.28", "15:18:20.45", "Eu fiquei 3 horas reformando a casa", ["3", "horas"]),
    C("15:18:20.52", "15:18:21.95", "pra tacarem fogo na minha casa, mano.", ["fogo"]),
    C("15:18:22.02", "15:18:24.10", "Bizarro, velho."),
    C("15:18:24.20", "15:18:25.70", "Paraíso perdido, mano.", ["Paraíso", "perdido"]),
]
write("alan/clip-01-casa", {
    "sources": [source("c1a"), source("c1b", sfx=-6), source("c1c"), source("c1d")],
    "hook": {"lines": ["Passou 3 HORAS", "reformando a casa…"], "title": ["Reformou a casa por 3 HORAS… e tacaram FOGO"],
             "kw": ["HORAS", "FOGO"], "size": 72, "titleSize": 46, "top": 290, "noBg": True},
    "labels": [{"s": "14:52:52.60", "d": 2.4, "t": "11 HORAS DEPOIS…"}, {"s": "15:18:18.00", "d": 2.0, "t": "1 HORA DEPOIS"}],
    "stamps": [{"s": "14:53:20.30", "d": 1.6, "t": "FOGO!", "size": 130}],
    "segments": segs, "captions": caps,
}, ["c1a", "c1b", "c1c", "c1d"])
