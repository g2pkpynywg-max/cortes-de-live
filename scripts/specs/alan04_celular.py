import sys; sys.path.insert(0, "scripts/specs")
from alan_common import *

segs = [
    {"src": "c4a", "in": "5:29:35.40", "out": "5:29:54.70", "panels": G(),
     "zooms": [{"at": "5:29:38.31", "scale": 1.07, "hold": 1.4}, {"at": "5:29:47.81", "scale": 1.08, "hold": 1.4}]},
    {"src": "c4b", "in": "13:11:52.90", "out": "13:11:57.40", "panels": G()},
    {"src": "c4b", "in": "13:13:09.50", "out": "13:13:18.70", "panels": G()},
    {"src": "c4b", "in": "13:15:45.50", "out": "13:16:08.20", "panels": G(),
     "zooms": [{"at": "13:15:54.25", "scale": 1.07, "hold": 1.4}, {"at": "13:16:06.53", "scale": 1.08, "hold": 1.4}]},
]
caps = [
    C("5:29:37.20", "5:29:38.30", "Cara, cansei, chat."),
    C("5:29:38.31", "5:29:39.20", "Fiquei três horas no celular.", ["três", "horas", "celular"]),
    C("5:29:39.23", "5:29:40.50", "Mano, nem lembro o que eu ia fazer, mano."),
    C("5:29:40.55", "5:29:43.95", "Ah, lembrei. Eu ia chamar o cara pra consertar meu carro, mano.", ["carro"]),
    C("5:29:44.03", "5:29:46.95", "Nossa Senhora, mano. Fiquei três horas no celular, tá esquecido.", ["três", "horas"]),
    C("5:29:47.09", "5:29:49.60", "Cê viu, mano? Entrei no doom scrolling, mano.", ["doom", "scrolling"]),
    C("5:29:51.95", "5:29:54.70", "Eu fiquei scrollando e não parei mais, velho.", ["scrollando"]),
    C("13:11:53.05", "13:11:55.75", "Mano, enquanto a gente tá aqui, vamos scrollar no TikTok,", ["TikTok"]),
    C("13:11:55.79", "13:11:57.40", "velho, pra ver o que tem de novidade, né?", ["novidade"]),
    C("13:13:09.61", "13:13:13.95", "“Então quer dizer que se eu causar um probleminha em Ocean Beach, vou dar de cara com você.", ["probleminha"]),
    C("13:13:14.01", "13:13:15.70", "Fechado, rico, curte."),
    C("13:13:15.79", "13:13:17.75", "Já volto, vou cometer um bilhão de crimes.", ["bilhão", "crimes"]),
    C("13:13:17.83", "13:13:18.70", "Linguinha, linguinha, linguinha.”", ["Linguinha"]),
    C("13:15:45.75", "13:15:48.30", "Mano, acho que eu passei minha casa, chat.", ["passei", "casa"]),
    C("13:15:48.37", "13:15:50.55", "Acho que eu passei minha casa, mano.", ["casa"]),
    C("13:15:50.61", "13:15:54.20", "Calma, eu estava muito focado aqui no TikTok, mano.", ["TikTok"]),
    C("13:15:54.25", "13:15:57.05", "Passei minha casa, velho.", ["casa"]),
    C("13:15:57.11", "13:15:59.95", "Cara, ele nem viu o tempo passar, mano. Que loucura!", ["tempo", "passar"]),
    C("13:16:00.03", "13:16:03.20", "Mano, eu estava lá scrollando do nada, pau.", ["scrollando"]),
    C("13:16:03.27", "13:16:06.45", "Cheguei na minha casa. Nem a minha casa, na real."),
    C("13:16:06.53", "13:16:08.20", "Acabei de perceber que aqui não é a minha casa.", ["não", "é"]),
]
write("alan/clip-04-celular", {
    "sources": [source("c4a"), source("c4b")],
    "hook": {"lines": ["Viciado no TikTok…", "DENTRO do GTA 6"], "title": ["Viciado no TikTok… DENTRO do GTA 6"],
             "kw": ["TikTok", "DENTRO"], "size": 70, "titleSize": 46, "top": 290, "noBg": True},
    "labels": [{"s": "13:11:53.00", "d": 2.4, "t": "8 HORAS DEPOIS…"}],
    "stamps": [{"s": "13:15:46.09", "d": 1.6, "t": "PASSOU!", "size": 100}],
    "segments": segs, "captions": caps,
}, ["c4a", "c4b"])
