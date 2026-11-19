"""Segments of a transcript JSON inside a window. Usage: win.py <transcript.json> H:MM:SS H:MM:SS"""
import json, sys
def p(t): h, m, s = t.split(':'); return int(h)*3600 + int(m)*60 + float(s)
f = lambda x: f"{int(x//3600)}:{int(x%3600//60):02d}:{x%60:05.2f}"
a, b = p(sys.argv[2]), p(sys.argv[3])
for s in json.load(open(sys.argv[1])):
    if s['end'] >= a and s['start'] <= b: print(f"{f(s['start'])}-{f(s['end'])} {s['text'][:170]}")
