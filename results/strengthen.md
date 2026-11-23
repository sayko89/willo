# Ek deneyler: büyük tank ve model dışı test

Tarih: 2026-11-23 · Betik: `scripts/run_strengthen.py` · Ham sonuçlar: `results/strengthen_runs.csv`, `results/strengthen_summary.json` · 810 koşu

Bütün sonuçlar **simülasyondur**. Örneklem küçük (her hücrede 12–15 koşu), oranları ±%10–15 belirsizlikle okuyun.

## A. Büyük tank: yöntem büyük sitede çalışıyor mu?

İlk hedef segment Wilo SiBoost'lu büyük siteler. Bu binalarda basınç tankı büyük, gece kullanımı fazla. Tespit oranını tank boyu ve kullanılan gece sayısına göre ölçtük. Boru kaçağı, gece kullanımı saatte 0,5–3 olay.

**Tespit oranı, 7 gece (kaçak debisine göre):**

| Tank | 5 L/sa | 10 L/sa | 20 L/sa | 50 L/sa | Yanlış alarm (kaçaksız) | Debi hatası |
|---|---|---|---|---|---|---|
| 24 L | %92 | %100 | %100 | %100 | %8 | %2 |
| 50 L | %50 | %100 | %100 | %100 | %17 | %5 |
| 100 L | %25 | %75 | %100 | %100 | %17 | %11 |

**Okuma:**
- **Tespit eşiği tank boyuyla artıyor.** Fiziği basit: duruş süresi T_off = ΔV / Q. Büyük tankta küçük bir kaçağın duruşu, gecenin sessiz aralığına sığmayacak kadar uzuyor. 24 L tankta 5 L/sa, 50 L tankta 10 L/sa, 100 L tankta 20 L/sa ve üstü güvenilir.
- **Daha çok gece kullanmak çözüm değil.** 14 ve 21 gecede tespit oranı değişmedi. Büyük tankta yanlış alarm ise arttı (100 L, 21 gece: %67). Bu yüzden 7 gece kalıyor.
- **Ürüne yansıması:** Kurulumda ΔV ölçülüyor (test vanasıyla kalibrasyon), dolayısıyla binanın tespit eşiği baştan biliniyor. Karnede şu satır yer alır: "Bu binada görebildiğimiz en küçük kaçak: X L/sa". Büyük sitede 20 L/sa eşiği küçük görünmeyebilir, ama bu tek bir dairedeki sürekli akan bir rezervuara denk; ayda ≈14 m³ ve ≈960 TL eder.
- **Sunumdaki segment ifadesi** buna göre düzeltildi: "SiBoost'lu siteler, büyük tankta eşik ≈20 L/sa; basit hidroforlu apartmanlar, eşik 5–10 L/sa".

## B. Model dışı test: sonuç simülatörün kendi varsayımlarına mı bağlı?

Tahminci, simülatörün varsayılan binası ve gece kullanımıyla geliştirildi. Bu testte bina ve kullanım bilerek **farklı** seçildi, tahmincinin kodu değişmedi:
- eski tip rezervuar (8–12 L, daha hızlı dolum)
- daha uzun musluk kullanımları (10–60 sn)
- daha kalabalık gece (saatte 1–3 olay)
- farklı pompa ayarı (2,5–3,5 bar)
- 2 kat basınç sensörü gürültüsü

| | Ana deney (aynı model) | Model dışı test |
|---|---|---|
| Tespit, ≥10 L/sa | %85–100 | **%97** |
| Tespit, 5 L/sa | — | %52 |
| Debi hatası (tespit edilenlerde) | %10 | **%10** |
| Yanlış alarm | %5 | **%0** |

Tür ayrımı bu testte ölçülmedi, çünkü tür modeli varsayılan bina verisiyle eğitildi. Yeni bina tipinde yeniden eğitim ya da kurulum kalibrasyonu gerekir. Bu, finaldeki düzenek testinin konusu.

**Sınır:** Bu test de bir simülasyon. "Farklı varsayımlar altında da çalışıyor" gösteriyor, "gerçek binada çalışıyor" göstermiyor. O sorunun cevabı 12 V düzenek testi ve gerçek bir SiBoost kaydı (`docs/v1-test-rig.md`, `docs/canvas-draft.md` §8).
