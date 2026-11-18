#!/usr/bin/env bash
# Step 1: probe the livestream and extract a 16 kHz mono WAV for transcription and audio analysis.
# Usage: scripts/ingest.sh input/live.mp4
set -euo pipefail
SRC="${1:?usage: scripts/ingest.sh input/<file>.mp4}"
mkdir -p work
ffprobe -v error -show_entries format=duration,size:stream=codec_name,width,height,r_frame_rate,sample_rate \
  -of json "$SRC" > work/probe.json
ffmpeg -y -v error -i "$SRC" -vn -ac 1 -ar 16000 work/audio.wav
# Loudness per second (for energy peaks: laughter, shouting, applause)
ffmpeg -v info -i work/audio.wav -af "astats=metadata=1:reset=16000,ametadata=print:key=lavfi.astats.Overall.RMS_level:file=work/loudness.txt" -f null - 2>/dev/null
# Silences (for clean cut points)
ffmpeg -i work/audio.wav -af silencedetect=noise=-35dB:d=0.6 -f null - 2> work/silences.txt || true
# 1 frame every 10 s for a visual contact sheet (scene/face framing check)
mkdir -p work/frames && ffmpeg -y -v error -i "$SRC" -vf "fps=1/10,scale=480:-2" work/frames/f_%05d.jpg
echo "Ingest done: work/probe.json, work/audio.wav, work/loudness.txt, work/silences.txt, work/frames/"
