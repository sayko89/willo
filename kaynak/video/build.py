import subprocess, os
from script import SCENES, XF, dur, scene_caption_len

ENC = ["-c:v", "libx264", "-crf", "16", "-preset", "veryfast", "-pix_fmt", "yuv420p", "-r", "30"]

def run(cmd):
    subprocess.run(cmd, check=True)

def ts(t):
    h = int(t // 3600); m = int(t % 3600 // 60); s = t % 60
    return f"{h}:{m:02d}:{s:05.2f}"

files, lens = [], []
for i, (src, lines) in enumerate(SCENES):
    last = i == len(SCENES) - 1
    L = round(scene_caption_len(lines) + (1.2 if last else XF), 2)
    lens.append(L)
    out = f"sc{i:02d}.mp4"
    if src.startswith("sim:"):
        out = f"sim_{src[4:]}.mp4"
    else:
        N = int(round(L * 30))
        z_in = i % 2 == 0  # alternate slow push-in / pull-out
        z = f"1+0.04*on/{N}" if z_in else f"1.04-0.04*on/{N}"
        if src == "end.png":
            z = f"1+0.02*on/{N}"
        vf = (f"scale=3840:2160,zoompan=z='{z}':x='iw/2-iw/zoom/2':y='ih*0.44-ih/zoom*0.44'"
              f":d={N}:s=1920x1080:fps=30,format=yuv420p")
        if not os.path.exists(out):
            run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-i", src, "-vf", vf,
                 "-frames:v", str(N), *ENC, "tmp_" + out])
            os.rename("tmp_" + out, out)
    files.append(out)

# xfade chain + subtitles
inputs = sum((["-i", f] for f in files), [])
fc, prev, t = [], "[0:v]", 0.0
starts = [0.0]
for i in range(1, len(files)):
    t += lens[i - 1] - XF
    starts.append(t)
    lab = f"[x{i}]"
    fc.append(f"{prev}[{i}:v]xfade=transition=fade:duration={XF}:offset={t:.3f}{lab}")
    prev = lab
total = starts[-1] + lens[-1]

hdr = """[Script Info]
ScriptType: v4.00+
PlayResX: 1920
PlayResY: 1080
WrapStyle: 0

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Default,Inter,40,&H00FFFFFF,&H00FFFFFF,&H00332E0B,&H00332E0B,0,0,0,0,100,100,0,0,1,0,0,2,170,170,28,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
ev = []
for (src, lines), s in zip(SCENES, starts):
    t = s + (0.25 if s > 0 else 0.3)
    for l in lines:
        d = dur(l)
        ev.append(r"Dialogue: 0,%s,%s,Default,,0,0,0,,{\fad(200,200)}%s" % (ts(t), ts(t + d - 0.2), l))
        t += d
open("subs.ass", "w").write(hdr + "\n".join(ev) + "\n")

fc.append(f"{prev}subtitles=subs.ass:fontsdir=/usr/share/fonts/opentype/inter,"
          f"fade=t=in:st=0:d=0.6,fade=t=out:st={total-1.0:.2f}:d=1.0,format=yuv420p[v]")
run(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", *inputs, "-filter_complex", ";".join(fc),
     "-map", "[v]", "-t", f"{total:.2f}", "-c:v", "libx264", "-crf", "20", "-preset", "veryfast",
     "-pix_fmt", "yuv420p", "-movflags", "+faststart", "tmp_final.mp4"])
os.rename("tmp_final.mp4", "../Periapsis_NABIZ_Video.mp4")
print("total", round(total, 2))
open("../NABIZ_video_metni.txt", "w").write("NABIZ — Video anlatım metni (Periapsis)\n\n" + "\n\n".join(
    f"[Sahne {i} · {ts(s)[2:7]}]\n" + "\n".join(ls) for i, ((_, ls), s) in enumerate(zip(SCENES, starts), 1)) + "\n")
