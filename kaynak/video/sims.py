"""Animated simulation scenes, piped to ffmpeg. Usage: python sims.py leak|tank seconds out.mp4"""
import os, sys, json, subprocess
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
from matplotlib.patches import FancyBboxPatch

REPO = os.environ.get("WILO_REPO", os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
sys.path.insert(0, REPO)
for f in ("Inter-Regular.otf", "Inter-Bold.otf", "Inter-SemiBold.otf"):
    fm.fontManager.addfont(f"/usr/share/fonts/opentype/inter/{f}")
plt.rcParams.update({"font.family": "Inter", "font.size": 17, "axes.edgecolor": "#9BB5B8",
                     "axes.labelcolor": "#0B2E33", "xtick.color": "#35575B", "ytick.color": "#35575B"})
BG = "#0B2E33"; TEAL = "#0F7C83"; INK = "#0B2E33"; RED = "#E4572E"; AMB = "#F2A93B"
W, H, FPS = 1920, 1080, 30

def frame_base(label, title):
    fig = plt.figure(figsize=(W / 100, H / 100), dpi=100, facecolor=BG)
    card = FancyBboxPatch((160 / W, (H - 22 - 900) / H), 1600 / W, 900 / H,
                          boxstyle="round,pad=0,rounding_size=0.004", transform=fig.transFigure,
                          facecolor="white", edgecolor="none", zorder=-10)
    fig.patches.append(card)
    fig.text(232 / W, 1 - 70 / H, label, color=TEAL, fontsize=17, weight="bold", va="center")
    fig.text(232 / W, 1 - 128 / H, title, color=INK, fontsize=34, weight="bold", va="center")
    return fig

def pipe(out, sec):
    return subprocess.Popen(["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-f", "rawvideo",
        "-pix_fmt", "rgba", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", "-t", str(sec),
        "-c:v", "libx264", "-crf", "16", "-preset", "veryfast", "-pix_fmt", "yuv420p", out],
        stdin=subprocess.PIPE)

def ease(x):
    x = min(max(x, 0), 1); return 1 - (1 - x) ** 3 if x < 1 else 1.0

def leak(sec, out):
    from src.sim.leak_sim import Building, NightUse, Leak, simulate_nights
    b = Building()
    runs = [simulate_nights(b, NightUse(), Leak("none", 0), 1, 7)[0],
            simulate_nights(b, NightUse(), Leak("pipe", 10), 1, 7)[0]]
    t = np.arange(len(runs[0])) / 3600.0
    step = 10
    data = []
    for r in runs:
        p = r["pressure_bar"].to_numpy(); on = r["pump1_running"].to_numpy()
        st = r["pump1_starts_total"].to_numpy(); st = st - st[0]
        # stop intervals (s)
        edges = np.flatnonzero(np.diff(on.astype(int)) != 0) + 1
        data.append(dict(p=p[::step], on=on[::step], st=st, t=t[::step], on_full=on))
    # longest pump stop in the leak night -> Q = dV / T_off
    on = data[1]["on_full"]; stops = []; cur = 0
    for v in on:
        if v == 0: cur += 1
        else:
            if cur: stops.append(cur)
            cur = 0
    t_off = sorted(stops)[-2] if len(stops) > 2 else max(stops)  # robust: 2nd longest
    q_est = b.delta_v / t_off * 3600

    fig = frame_base("SİMÜLASYON · GECE KAÇAĞI (00:00–05:00)",
                     "Kaçak tankı boşaltır, pompa gece boyunca tekrar kalkar")
    axes = [fig.add_axes([300 / W, (H - 480) / H, 980 / W, 245 / H]),
            fig.add_axes([300 / W, (H - 835) / H, 980 / W, 245 / H])]
    names = ["Kaçaksız bina", "Saatte 10 L boru kaçağı olan bina"]
    cols = [TEAL, RED]
    lines, fills = [], [None, None]
    for ax, nm, c in zip(axes, names, cols):
        ax.set_xlim(0, 5); ax.set_ylim(2.8, 4.3)
        ax.set_ylabel("Basınç (bar)")
        ax.set_title(nm, loc="left", fontsize=19, color=c, weight="bold", pad=8)
        ax.grid(alpha=0.25); ax.spines[["top", "right"]].set_visible(False)
        ax.set_xticks(range(6)); ax.set_xticklabels([f"0{h}:00" for h in range(6)])
        lines.append(ax.plot([], [], color=c, lw=2)[0])
    # stat panels
    sx = 1330 / W
    stat = []
    for i, (y, c) in enumerate([(1 - 300 / H, TEAL), (1 - 650 / H, RED)]):
        fig.text(sx, y + 0.07, "Pompa kalkışı", fontsize=18, color="#35575B")
        stat.append(fig.text(sx, y - 0.02, "0", fontsize=54, color=c, weight="bold"))
    res = fig.text(sx, 1 - 830 / H, "", fontsize=19, color=INK, weight="bold", linespacing=1.5)
    leg = fig.text(232 / W, 1 - 903 / H, "Her testere dişi bir pompa kalkışıdır. Bina, tank ve gece kullanımı varsayım (repo: src/sim/leak_sim.py).",
                   fontsize=14, color="#5B7477")
    proc = pipe(out, sec)
    N = int(sec * FPS)
    draw_end = 0.72
    for k in range(N):
        f = ease(k / (N * draw_end))
        tcur = 5 * f
        for i, d in enumerate(data):
            m = d["t"] <= tcur
            lines[i].set_data(d["t"][m], d["p"][m])
            idx = min(int(tcur * 3600), len(d["st"]) - 1)
            stat[i].set_text(str(int(d["st"][idx])))
        if k > N * 0.78:
            res.set_text(f"Duruş süresi T_off ≈ {t_off/60:.0f} dk\nΔV / T_off ≈ {q_est:.1f} L/sa\n(gerçek: 10 L/sa)")
        fig.canvas.draw()
        proc.stdin.write(fig.canvas.buffer_rgba().tobytes())
    proc.stdin.close(); proc.wait()
    print("leak q_est", q_est, "t_off", t_off)

def tank(sec, out):
    d = json.load(open(f"{REPO}/results/tank_week_trace.json"))
    keys = ["Şamandıra (hep dolu)", "Sabit takvim (kurulumda girilen)", "NABIZ (taban 18 sa)"]
    labels = ["Şamandıra (hep dolu)", "Sabit takvim", "NABIZ"]
    cols = [RED, AMB, TEAL]
    h = np.arange(168)
    sup = np.array(d["supply_on"])
    fig = frame_base("SİMÜLASYON · TAZE DEPO", "Takvim değişince sabit kural çöker, NABIZ uyum sağlar")
    a1 = fig.add_axes([300 / W, (H - 530) / H, 1372 / W, 310 / H])
    a2 = fig.add_axes([300 / W, (H - 845) / H, 1372 / W, 240 / H], sharex=a1)
    for a in (a1, a2):
        a.set_xlim(0, 167); a.grid(alpha=0.25); a.spines[["top", "right"]].set_visible(False)
        # red shading for no supply
        off = sup == 0
        starts = np.flatnonzero(np.diff(np.r_[0, off.astype(int)]) == 1)
        ends = np.flatnonzero(np.diff(np.r_[off.astype(int), 0]) == -1)
        for s, e in zip(starts, ends):
            a.axvspan(s, e + 1, color=RED, alpha=0.09, lw=0)
    a1.set_ylim(0, 10.8); a1.set_ylabel("Depo (m³)")
    a2.set_ylim(0, 55); a2.set_ylabel("Su yaşı (saat)")
    a2.set_xticks(range(0, 169, 24)); a2.set_xticklabels([f"Gün {i+1}" for i in range(8)])
    plt.setp(a1.get_xticklabels(), visible=False)
    L1 = [a1.plot([], [], color=c, lw=2.6, label=l)[0] for c, l in zip(cols, labels)]
    L2 = [a2.plot([], [], color=c, lw=2.6)[0] for c in cols]
    a1.legend(loc="upper left", ncol=3, frameon=True, fontsize=16, bbox_to_anchor=(0, 1.16))
    fig.text(1672 / W, 1 - 205 / H, "Kırmızı bant: şebekede su yok", fontsize=15, color=RED, ha="right")
    fig.text(232 / W, 1 - 903 / H, "Kesinti takvimi her gün 08–22 olduktan sonraki bir hafta. Senaryo ve bina varsayım (repo: src/sim/tank_sim.py).",
             fontsize=14, color="#5B7477")
    proc = pipe(out, sec)
    N = int(sec * FPS)
    for k in range(N):
        f = ease(k / (N * 0.8)); n = max(1, int(168 * f))
        for i, key in enumerate(keys):
            L1[i].set_data(h[:n], np.array(d[key]["level_l"][:n]) / 1000)
            L2[i].set_data(h[:n], d[key]["age_h"][:n])
        fig.canvas.draw()
        proc.stdin.write(fig.canvas.buffer_rgba().tobytes())
    proc.stdin.close(); proc.wait()

if __name__ == "__main__":
    {"leak": leak, "tank": tank}[sys.argv[1]](float(sys.argv[2]), sys.argv[3])
