# NABIZ · Water AI Hackathon 2026 — Periapsis

**Takım:** Periapsis (Safiye Özkan · Emir Metin · Uğur Furkan Yeşil)
**Alan:** Binalar · **Etkinlik:** Water AI Hackathon 2026 (Wilo Türkiye x imece)

NABIZ, apartman bodrumundaki depo + hidrofor düzeneğinden gelen pompa verisiyle binanın tüketim parmak izini öğrenir. Bu modelle iki iş yapar: kesinti riskine göre depo seviyesi önerir, gece kaçağını debi, maliyet ve tür olarak tespit eder. Wilo-Monitor'a eklenen bir modül olarak tasarlandı.

Proje kodu, simülasyonlar ve canlı prototip: [ugurfurkanyesil-rgb/wilo-hackathon](https://github.com/ugurfurkanyesil-rgb/wilo-hackathon) · [Canlı demo](https://ugurfurkanyesil-rgb.github.io/wilo-hackathon/)

## Ara teslim (24 Kasım 2026, 23:59)

| Dosya | İçerik |
|---|---|
| [`teslim/Periapsis_NABIZ_Proje_Fikri_Kanvasi.pdf`](teslim/Periapsis_NABIZ_Proje_Fikri_Kanvasi.pdf) | Wilo'nun Proje Fikri Kanvası şablonu doldurulmuş hali: 8 sorunun 1–2 cümlelik yanıtları, takım üyeleri ve rolleri |
| [`teslim/NABIZ_Proje_Fikri.pdf`](teslim/NABIZ_Proje_Fikri.pdf) | 10 sayfalık sunum: 8 sorunun kaynaklı ve simülasyon sonuçlu ayrıntısı (kapakta takım bilgisi) |
| [`teslim/NABIZ_Proje_Fikri.pptx`](teslim/NABIZ_Proje_Fikri.pptx) | Sunumun düzenlenebilir hali |
| [`teslim/e-posta.md`](teslim/e-posta.md) | Teslim e-postası. Kime: imece@imece.com, konu: "Water AI Hackathon - Periapsis Proje Fikri" |
| [`video/Periapsis_NABIZ_Video.mp4`](video/Periapsis_NABIZ_Video.mp4) | Opsiyonel tanıtım videosu (3 dk 22 sn, altyazılı, sessiz): sunum sahneleri ve iki animasyonlu simülasyon (gece kaçağı, taze depo) |
| [`video/NABIZ_video_metni.txt`](video/NABIZ_video_metni.txt) | Videonun seslendirme metni, sahne başlangıç süreleriyle |

Videoyu göndermek için YouTube'a "liste dışı" ya da Drive'a "bağlantıya sahip herkes" erişimiyle yükleyip linki e-postaya ekleyin.

## Yeniden üretme

`kaynak/` klasöründe teslim dosyalarını üreten betikler var:

- `kaynak/canvas.py`: Kanvas metinlerini Wilo'nun şablonuna (`kaynak/Water_AI_Poster_Ornegi.pdf`) yerleştirir.
  ```bash
  python kaynak/canvas.py kaynak/Water_AI_Poster_Ornegi.pdf teslim/Periapsis_NABIZ_Proje_Fikri_Kanvasi.pdf
  ```
- `kaynak/video/`: Videonun anlatım metni (`script.py`), simülasyon animasyonları (`sims.py`) ve montaj (`build.py`).
  - `sims.py` simülasyon kodunu ve sonuçlarını [wilo-hackathon](https://github.com/ugurfurkanyesil-rgb/wilo-hackathon) reposundan okur. Repo yolu dosyanın başındaki `WILO_REPO` ortam değişkeniyle verilir (varsayılan `../wilo-hackathon`).
  - `build.py` sahne görsellerini (`s01.png` … `s10.png`, sunum sayfalarının 1920×1080 hali, ve `end.png`) çalışma klasöründe bekler.
  - Gerekenler: Python 3, matplotlib, numpy, pandas, reportlab, pypdf, ffmpeg (libass ile), Inter yazı tipi.

> Tüm sayısal sonuçlar simülasyondan gelir, gerçek bina ölçümü değildir. Doğrulanmamış bilgiler "varsayım" olarak işaretlidir.
