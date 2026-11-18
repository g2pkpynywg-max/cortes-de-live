"""Print transcript segments in a time window. Usage: window.py H:MM:SS H:MM:SS"""
import json, sys
def p(t): h,m,s=map(int,t.split(':')); return h*3600+m*60+s
def f(x): return f"{int(x//3600)}:{int(x%3600//60):02d}:{x%60:05.2f}"
a,b=p(sys.argv[1]),p(sys.argv[2])
for s in json.load(open('work/transcript_full.json')):
    if s['end']>=a and s['start']<=b: print(f"{f(s['start'])}-{f(s['end'])} {s['text']}")
