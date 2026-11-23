"""Ek deneyler (ara teslim sonrası güçlendirme).

A) Büyük tank: tespit oranı tank boyu (24/50/100 L) ve kullanılan gece sayısıyla (7/14/21) nasıl değişiyor?
   Soru: hedef segment büyük siteler (büyük tank, kalabalık gece); yöntem orada çalışıyor mu?
B) Model dışı test: tahminciyi kurarken varsaydığımızdan FARKLI bir bina ve kullanım
   (eski rezervuar 8-12 L, daha uzun musluk kullanımı, 2,5-3,5 bar ayar, 2 kat sensör gürültüsü).
   Soru: sonuç, simülatörün kendi varsayımlarına mı bağlı?

Hepsi simülasyon; parametreler varsayım [V]. Çıktı: results/strengthen_summary.json, results/strengthen.md
"""
from __future__ import annotations

import json
import sys
from multiprocessing import Pool
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from src.sim import leak_estimator as est  # noqa: E402
from src.sim.leak_sim import Building, Leak, NightUse, simulate_nights  # noqa: E402

OUT = ROOT / "results"
CV_MAX = json.loads((OUT / "leak_summary.json").read_text(encoding="utf-8"))["cv_max"]
RATES = [5, 10, 20, 50]


def run_case(args):
    exp, V0, nights, kind, lph, seed = args
    rng = np.random.default_rng(seed)
    if exp == "A":
        b = Building(V0=V0)
        use = NightUse(rate_per_h=float(rng.uniform(0.5, 3.0)))
        p_mid = 3.5
    else:  # B: out-of-model building and usage
        b = Building(V0=V0, p_on=2.5, p_off=3.5, noise_bar=0.04)
        use = NightUse(rate_per_h=float(rng.uniform(1.0, 3.0)), flush_l=(8.0, 12.0),
                       flush_lps=0.15, tap_s=(10.0, 60.0))
        p_mid = 3.0
    dv, _ = est.calibrate(simulate_nights(b, NightUse(rate_per_h=0.3), Leak("pipe", 10), 3, seed + 10_000),
                          10, p_mid=p_mid)
    leak = Leak(kind, lph, p_nom=p_mid) if kind != "none" else Leak("none", 0)
    e = est.estimate_leak(simulate_nights(b, use, leak, nights, seed), dv, cv_max=CV_MAX, p_mid=p_mid)
    det = e.leak_type != "none"
    err = abs(e.leak_lph - lph) / lph if (det and lph > 0 and np.isfinite(e.leak_lph)) else np.nan
    return dict(exp=exp, V0=V0, nights=nights, kind=kind, lph=lph, seed=seed, detected=det, ape=err)


def main():
    cases = []
    for V0 in (24, 50, 100):
        for n in (7, 14, 21):
            for s in range(300, 312):
                cases.append(("A", V0, n, "none", 0, s))
                cases += [("A", V0, n, "pipe", r, s) for r in RATES]
    for V0 in (24, 50):
        for s in range(400, 415):
            cases.append(("B", V0, 7, "none", 0, s))
            cases += [("B", V0, 7, k, r, s) for k in ("pipe", "reservoir") for r in RATES]
    with Pool() as p:
        df = pd.DataFrame(p.map(run_case, cases, chunksize=4))
    df.to_csv(OUT / "strengthen_runs.csv", index=False)

    leak = df[df.kind != "none"]
    none = df[df.kind == "none"]
    a = leak[leak.exp == "A"]
    tabA = a.pivot_table(index="V0", columns="nights", values="detected", aggfunc="mean").round(2)
    tabA_rate = a[a.nights == 7].pivot_table(index="V0", columns="lph", values="detected", aggfunc="mean").round(2)
    tabA_rate14 = a[a.nights == 14].pivot_table(index="V0", columns="lph", values="detected", aggfunc="mean").round(2)
    faA = none[none.exp == "A"].pivot_table(index="V0", columns="nights", values="detected", aggfunc="mean").round(2)
    mapeA = a.pivot_table(index="V0", columns="nights", values="ape", aggfunc="mean").round(3)
    b = leak[leak.exp == "B"]
    summ = {
        "A_detection_by_tank_nights": {int(k): {int(c): float(v) for c, v in r.items()} for k, r in tabA.iterrows()},
        "A_detection_by_tank_rate_7n": {int(k): {int(c): float(v) for c, v in r.items()} for k, r in tabA_rate.iterrows()},
        "A_detection_by_tank_rate_14n": {int(k): {int(c): float(v) for c, v in r.items()} for k, r in tabA_rate14.iterrows()},
        "A_false_alarm_by_tank_nights": {int(k): {int(c): float(v) for c, v in r.items()} for k, r in faA.iterrows()},
        "A_flow_error_by_tank_nights": {int(k): {int(c): float(v) for c, v in r.items()} for k, r in mapeA.iterrows()},
        "B_detection": round(float(b.detected.mean()), 3),
        "B_detection_ge10": round(float(b[b.lph >= 10].detected.mean()), 3),
        "B_detection_by_rate": {int(k): round(float(v), 2) for k, v in b.groupby("lph").detected.mean().items()},
        "B_flow_error": round(float(b.ape.mean()), 3),
        "B_false_alarm": round(float(none[none.exp == "B"].detected.mean()), 3),
        "n_runs": len(df),
    }
    (OUT / "strengthen_summary.json").write_text(json.dumps(summ, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps(summ, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
