"""Print word-level timings in a window. Usage: words.py H:MM:SS H:MM:SS"""
import json, sys
def p(t): h,m,s=map(int,t.split(':')); return h*3600+m*60+s
def f(x): return f"{int(x//3600)}:{int(x%3600//60):02d}:{x%60:05.2f}"
a,b=p(sys.argv[1]),p(sys.argv[2]); out=[]
for s in json.load(open('work/transcript_full.json')):
    for w in s['words']:
        if a<=w['s']<=b: out.append(f"{f(w['s'])} {w['w']}")
print(' | '.join(out))
