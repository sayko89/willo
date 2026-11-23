from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.utils import simpleSplit
from pypdf import PdfReader, PdfWriter
import io, sys

pdfmetrics.registerFont(TTFont("R", "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"))
pdfmetrics.registerFont(TTFont("B", "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"))
H = 1683.78
INK = (0.04, 0.18, 0.2)

fields = {
    (65, 250, 388, 281): "NABIZ: Hidrofor verisiyle akıllı bina suyu",
    (434, 250, 757, 281): "Periapsis",
    (802, 250, 1126, 281): "Binalar",
}
boxes = {
 "01": ((71, 458, 567, 557),
  "Kesintiler (İzmir'de 13 ilçede 6 ay gece kesintisi, Ankara'da kontrollü su) apartmanları bodrum deposuna bağımlı yaptı; depoda bekleyen su bozuluyor (Diyarbakır, 200 konut: koliformlu örnek depo girişinde %35, çıkışında %52). Gece kaçakları da ortak faturaya görünmeden yansıyor: 5 L/saat ≈ ayda 3,6 m³ ve ≈241 TL."),
 "02": ((624, 434, 1120, 557),
  "Önce site yönetim firması ve apartman yöneticisi (önce SiBoost'lu siteler, sonra basit hidroforlu apartmanlar). Depoyu kesinti duyurusuna göre elle dolduruyor, kaçağı faturadan sonra arıyor. Ön ankette (9 kişi: yönetici, teknik personel, tesisatçı, sakin) 8'i haftalık karneyi yararlı buldu, 4'ü kaçak ya da şamandıra arızası yaşamış; ödeme isteği varsayım (3 evet, 4 fiyatına bağlı)."),
 "03": ((71, 714, 567, 837),
  "Şamandıra depoyu her zaman tam doldurur; Keraflo Tanktronic gibi sistemler seviyeyi elle girilen takvime göre ayarlar, kesinti riski ve suyun depoda bekleme süresi hesaba girmez. Grundfos SCALA2 ve DAB Esybox gibi pompalar kaçakta yalnız evet/hayır alarmı verir; kaçağın debisi, maliyeti ve türü (boru mu, klozet rezervuarı mı) bilinmez."),
 "04": ((624, 714, 1120, 837),
  "NABIZ, Wilo-Monitor'a eklenen bir modül: yönetici her pazartesi telefonunda \u201cbina su karnesi\u201dni görür; gece kaçağı L/saat, TL/ay ve tür (boru mu, rezervuar mı) olarak gelir ve tesisatçıya doğrudan iş emri olur. Aynı veriden ikinci kazanç: kesinti riski artınca \u201cdepoyu doldur\u201d, risk düşünce \u201cseviyeyi indir\u201d önerisi; karar yöneticide kalır."),
 "05": ((71, 994, 567, 1117),
  "Pompanın kalkış/duruş zamanları, basınç ve depo seviyesinden binanın tüketim parmak izini öğrenir: kesinti desenini öğrenip depo seviyesi önerir, gece kullanımını kaçaktan ayırıp kaçak debisini ölçer ve kaçağı boru/rezervuar diye sınıflandırır. Simülasyonda debi hatası %10 (basit “pompalanan hacim / süre” yönteminde %131), tür doğruluğu %97; sabit takvim, kesinti takvimi değişince 6 kat fazla susuz saat bıraktı."),
 "06": ((624, 1018, 1120, 1117),
  "Wilo SC2.0 kontrol ünitesi Modbus TCP ile basınç, pompa çalışma biti ve kalkış sayacını standart veriyor; 1 dakikalık sayaç verisi yetiyor (simülasyonda tespit %88). Ek donanım: depo seviye sensörü + motorlu vana. Doğrulanmadı (varsayım): Wilo-Monitor veri aralığı, SCe sıfır debi eşiği, gerçek bina verisine erişim."),
 "07": ((71, 1298, 567, 1397),
  "Depodaki suyun ortalama bekleme süresi şamandıraya göre 39 saatten 25 saate iner (simülasyon), bulunan her 5 L/saatlik kaçak ayda 3,6 m³ su kurtarır. Takip edeceğimiz ana gösterge: binanın gece kaçak debisi (L/saat); yanında depo su yaşı (saat)."),
 "08": ((624, 1274, 1120, 1397),
  "Varsayım: 5–50 L/saatlik kaçak, gece kullanımına rağmen pompanın duruş süresinden ölçülebilir. Simülasyonda tahminciyi kurmadığımız bina ve kullanımda bile ≥10 L/sa kaçakların %97'si bulundu; eşik tank boyuyla artıyor (100 L tankta 20 L/sa). Hackathon günü 12 V düzenekte iğneli vanayla kaçak açıp gerçek debiyi teraziyle ölçer, tahminle canlı karşılaştırırız."),
}
members = [
 ("Safiye Özkan", "Veri ve yapay zekâ modeli, sunum"),
 ("Emir Metin", "Saha araştırması ve iş modeli (mülakatlar, Wilo soruları)"),
 ("Uğur Furkan Yeşil", "Simülasyon, gömülü sistem ve test düzeneği"),
]
rows = [(93, 1500, 579, 1522), (93, 1525, 579, 1546), (93, 1549, 579, 1570), (93, 1573, 579, 1594)]
role_x = 596

buf = io.BytesIO()
c = canvas.Canvas(buf, pagesize=(1190.55, H))
c.setFillColorRGB(*INK)

def fit(text, w, h, start=13.5, minsize=9):
    s = start
    while s >= minsize:
        lead = s * 1.32
        lines = simpleSplit(text, "R", s, w)
        if len(lines) * lead <= h:
            return s, lead, lines
        s -= 0.25
    sys.exit("does not fit: " + text[:40])

for (x0, t, x1, b), txt in fields.items():
    c.setFont("B", 14); c.drawString(x0 + 8, H - b + 10, txt)

for k, ((x0, t, x1, b), txt) in boxes.items():
    pad = 6
    s, lead, lines = fit(txt, x1 - x0 - 2 * pad, b - t - 2 * pad)
    print(k, s, len(lines))
    c.setFont("R", s)
    y = H - t - pad - s
    for ln in lines:
        c.drawString(x0 + pad, y, ln); y -= lead

for (n, r), (x0, t, x1, b) in zip(members, rows):
    c.setFont("R", 12.5)
    c.drawString(x0 + 6, H - b + 6, n)
    c.drawString(role_x + 6, H - b + 6, r)
c.save()

base = PdfReader(sys.argv[1]).pages[0]
base.merge_page(PdfReader(io.BytesIO(buf.getvalue())).pages[0])
w = PdfWriter(); w.add_page(base); w.write(sys.argv[2])
