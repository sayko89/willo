# Narration per scene: (source, [caption lines]); source = png still or "sim:<name>"
SCENES = [
 ("s01.png", [
  "Merhaba, biz Periapsis. Projemizin adı NABIZ.",
  "Bodrumdaki hidrofor, binanın su nabzını zaten tutuyor. Biz bu sinyali yapay zekâyla okuyoruz.",
 ]),
 ("s02.png", [
  "Su kesintileri apartmanları bodrum deposuna bağımlı hale getirdi: İzmir'de altı ay gece kesintisi yapıldı, Ankara'da su kontrollü verildi.",
  "Ama depoda bekleyen su bozuluyor: Diyarbakır'da koliformlu örnek oranı depo girişinde %35, çıkışında %52.",
  "Gece kaçakları da görünmüyor. Saatte 5 litrelik bir kaçak, ayda 3,6 m³ su ve yaklaşık 241 TL demek.",
 ]),
 ("s03.png", [
  "Bu kararları veren site yöneticisi; depoyu ne kadar dolu tutacağına ve faturanın neden arttığına bugün veri olmadan karar veriyor.",
  "Şamandıra depoyu hep tam doldurur. Ev tipi pompalar ise kaçakta yalnızca var ya da yok der; ne kadar olduğunu ve nereden geldiğini söylemez.",
 ]),
 ("s04.png", [
  "NABIZ, Wilo-Monitor'a eklenen bir yazılım modülü. Kaçak için ek sayaç gerekmiyor, pompanın kalkış sayacı yeterli.",
  "Depo için bir seviye sensörü ve motorlu vana ekliyoruz. Önce öneri modundayız: NABIZ önerir, karar yöneticide kalır.",
 ]),
 ("s05.png", [
  "Yönetici her pazartesi telefonunda binanın su karnesini görür: suyun yaşı, kesinti yedeği ve gece kaçağı.",
  "Kaçak bulunduğunda “rezervuar tipi, ayda 289 TL” bilgisi tesisatçıya doğrudan iş emri olur.",
 ]),
 ("s06.png", [
  "Yapay zekâ, pompa verisinden binanın tüketim parmak izini öğrenir ve iki karar verir.",
  "Birincisi, kesinti desenini öğrenip bir sonraki kesintiyi karşılayacak kadar su tutar. İkincisi, kaçağı ölçer ve türünü sınıflandırır.",
 ]),
 ("sim:leak", [
  "Simülasyonda iki binanın aynı gecesine bakalım: üstteki kaçaksız, alttakinde saatte 10 litrelik bir boru kaçağı var.",
  "Kaçak, basınç tankını yavaş yavaş boşaltır; pompa gece boyunca tekrar tekrar kalkar.",
  "NABIZ bu duruş sürelerinden kaçağın debisini hesaplıyor. Simülasyonda hatamız %10; basit “hacim bölü süre” yönteminde %131.",
 ]),
 ("s07.png", [
  "Özgün tarafımız şu: kaçak, pompanın debisinde değil duruş süresinde görünür.",
  "Rakipler kaçak var ya da yok derken, biz debi, maliyet ve tür veriyoruz.",
 ]),
 ("s08.png", [
  "Veri Wilo'nun cihazlarında hazır: kontrol ünitesi basıncı ve kalkış sayacını Modbus üzerinden standart olarak veriyor.",
  "Bilmediklerimizi açıkça Wilo'ya soru olarak yazdık: veri aralığı, sıfır debi eşiği ve pilot için gerçek bir kayıt.",
 ]),
 ("sim:tank", [
  "Depo tarafı: 180 günlük kesinti senaryosundan, kesintilerin her gün 08–22 arasına kaydığı bir hafta.",
  "Şamandıra depoyu hep dolu tutar, su iki güne kadar bekler. Sabit takvim ise değişen kesintide depoyu dibe kadar boşaltır.",
  "NABIZ kesinti desenini öğrenir: yedeği korur, suyu da şamandıradan daha taze tutar.",
 ]),
 ("s09.png", [
  "Sonuç: depodaki suyun ortalama bekleme süresi 39 saatten 25 saate iniyor; bulunan her 5 litrelik kaçak ayda 3,6 m³ su kurtarıyor.",
  "Ana göstergemiz binanın gece kaçak debisi; yanında depo su yaşını takip ediyoruz.",
 ]),
 ("s10.png", [
  "En kritik varsayımımız: küçük bir kaçağın pompanın duruş süresinden ölçülebilmesi.",
  "Hackathon günü 12 voltluk bir hidrofor düzeneğinde kaçak açıp gerçek debiyi teraziyle ölçecek, modelin tahminiyle canlı karşılaştıracağız.",
 ]),
 ("end.png", [
  "NABIZ: bina suyunu taze, tesisatı sızdırmaz tutmak için. Teşekkürler!",
 ]),
]

XF = 0.7  # crossfade seconds

def dur(line):
    return round(max(2.6, len(line) / 15.5 + 0.5), 2)

def scene_caption_len(lines):
    return round(sum(dur(l) for l in lines), 2)
