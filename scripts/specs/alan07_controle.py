import sys; sys.path.insert(0, "scripts/specs")
from alan_common import *

segs = [
    {"src": "c7a", "in": "2:45:09.30", "out": "2:45:13.80", "panels": G()},
    {"src": "c7a", "in": "2:45:28.30", "out": "2:45:34.40", "panels": G(),
     "zooms": [{"at": "2:45:32.96", "scale": 1.07, "hold": 1.2}]},
    {"src": "c7a", "in": "2:45:42.50", "out": "2:45:50.60", "panels": G()},
    {"src": "c7a", "in": "2:45:52.60", "out": "2:46:06.20", "panels": R(420, 300),
     "zooms": [{"at": "2:45:53.56", "scale": 1.06, "hold": 1.4}, {"at": "2:46:04.50", "scale": 1.08, "hold": 1.4}]},
    {"src": "c7b", "in": "10:19:51.80", "out": "10:20:02.00", "panels": G(),
     "zooms": [{"at": "10:19:55.75", "scale": 1.08, "hold": 1.6}]},
    {"src": "c7b", "in": "10:20:29.90", "out": "10:20:38.20", "panels": G(),
     "zooms": [{"at": "10:20:36.64", "scale": 1.08, "hold": 1.4}]},
]
caps = [
    C("2:45:09.51", "2:45:11.55", "Meu Deus, meu Deus, eu vou morrer, eu vou morrer!", ["morrer"]),
    C("2:45:11.61", "2:45:12.90", "Não, não, não, não, não!"),
    C("2:45:12.93", "2:45:13.80", "É muito tira!", ["tira"]),
    C("2:45:28.46", "2:45:30.75", "Cara, deve ser esse o Fênix!", ["Fênix"]),
    C("2:45:30.82", "2:45:32.90", "Entra rápido! Entra rápido!", ["rápido"]),
    C("2:45:32.96", "2:45:34.40", "Pelo amor de Deus, eu não posso morrer, eu tô sem vida!", ["sem", "vida"]),
    C("2:45:42.60", "2:45:44.20", "Sai, sai, sai, sai, sai, sai, sai, sai!", ["Sai"]),
    C("2:45:52.76", "2:45:55.65", "Cara, vocês sabem que eu só morri porque eu tô no controle, né?", ["controle"]),
    C("2:45:55.72", "2:45:59.90", "Se eu tivesse o mouse no teclado, mano…", ["mouse", "teclado"]),
    C("2:45:59.95", "2:46:04.40", "Eu tava assim, em outro mundo já, velho.", ["outro", "mundo"]),
    C("2:46:04.50", "2:46:06.20", "Infelizmente, me fui nerfado, mano.", ["nerfado"]),
    C("10:19:52.01", "10:19:55.20", "Meu Deus, meu Deus…"),
    C("10:19:55.29", "10:19:57.30", "Cara, o controle tem que ser abolido da face da terra,", ["controle", "abolido"]),
    C("10:19:57.35", "10:19:59.25", "sem brincadeira."),
    C("10:19:59.33", "10:20:02.00", "Quem vem pra jogar no controle não estava num dia bom, velho.", ["controle"]),
    C("10:20:30.06", "10:20:33.70", "Meu Deus, eu explodi essa moto, não tem gasolina nem motor, vazou o tanque.", ["gasolina"]),
    C("10:20:33.84", "10:20:36.60", "Calma, calma, mano,"),
    C("10:20:36.64", "10:20:38.20", "eu explodi a moto, tá sem gasolina.", ["sem", "gasolina"]),
]
write("alan/clip-07-controle", {
    "sources": [source("c7a"), source("c7b")],
    "hook": {"lines": ["A culpa é SEMPRE", "do controle"], "title": ["A culpa é SEMPRE do controle"],
             "kw": ["SEMPRE", "controle"], "size": 70, "titleSize": 46, "top": 290, "noBg": True},
    "labels": [{"s": "10:19:51.85", "d": 2.4, "t": "7 HORAS DEPOIS…"}],
    "stamps": [{"s": "2:46:04.90", "d": 1.3, "t": "NERFADO", "size": 76, "inScale": 1.2}],
    "segments": segs, "captions": caps,
}, ["c7a", "c7b"])
