# Jüri soruları ve cevaplarımız

Ara değerlendirmede ve 5 Aralık finalinde gelebilecek zor sorular. Her cevap kısa tutuldu ve kanıtın nerede olduğu belirtildi.

### 1. "%10 hata sizin kendi simülasyonunuzda. Gerçekte de böyle olacağını nereden biliyorsunuz?"
Bilmiyoruz, bunu iddia da etmiyoruz. Yaptıklarımız:
- Tahminciyi, kurarken kullanmadığımız bir bina ve kullanım modelinde test ettik: eski rezervuar, farklı basınç ayarı, 2 kat gürültü. Sonuç: ≥10 L/sa kaçakların %97'si bulundu, debi hatası yine %10 (`results/strengthen.md` §B).
- Yöntem fiziğe dayanıyor (T_off = ΔV / Q). ΔV kurulumda test vanasıyla ölçülüyor, yani model binaya göre kalibre ediliyor.
- Gerçek ölçüm finalde yapılacak: 12 V düzenek, iğneli vana, terazi (`docs/v1-test-rig.md`). Wilo'dan pilot için gerçek bir SiBoost kaydı istiyoruz.

### 2. "Büyük sitelerde tank büyük, gece kullanımı fazla. Orada çalışıyor mu?"
Kısmen, ve bunu ölçtük. Tespit eşiği tank boyuyla artıyor: 24 L tankta 5 L/sa, 100 L tankta 20 L/sa (`results/strengthen.md` §A). Bu yüzden:
- Karnede binanın eşiği açıkça yazıyor: "görebildiğimiz en küçük kaçak X L/sa".
- Büyük sitede 20 L/sa, tek bir dairede sürekli akan bir rezervuara denk; ayda ≈14 m³ ve ≈960 TL.
- En hassas sonuç basit hidroforlu apartmanlarda. Retrofit kit bu segment için.

### 3. "Bu yapay zekâ mı, yoksa bir eşik kuralı mı?"
Fizik, ölçülecek büyüklüğü veriyor. Yapay zekânın işi şunlar:
- **Gece kullanımını kaçaktan ayırmak:** Basit "pompalanan hacim / süre" yöntemi kullanımı da kaçak sayıyor ve %131 hata veriyor, bizimki %10.
- **Kaçak türünü sınıflandırmak:** Lojistik regresyonla boru mu, rezervuar mı (%97).
- **Binanın kesinti desenini öğrenip depo seviyesi önermek:** Sabit takvim, takvim değişince aynı tazelikte 6 kat fazla susuz saat bıraktı.

Her bina farklı olduğu için kural bina bina elle ayarlanamaz; model her binada kendi kendine kalibre oluyor.

### 4. "Site yöneticisi buna gerçekten ihtiyaç duyuyor mu, para öder mi?"
Henüz doğrulamadık, kanvasta "varsayım" olarak işaretli. Kısa anket hazır (`docs/hizli-dogrulama.md`), finalden önce 3 görüşme planlı (`docs/interview-guide.md`). Problemin varlığı yayımlanmış saha çalışmalarına dayanıyor (Diyarbakır, Adana, İzmir kesintileri). Ödeme kanalı: WiloCare aylık paketi; ödeyen site yönetim firması.

### 5. "Neden iki fikir? Hangisi asıl?"
Asıl ürün gece kaçağı. Depo önerisi, aynı veriden (pompa + depo seviyesi) gelen ikinci kazanç. Ek donanım yalnızca bir seviye sensörü ve motorlu vana. Tek kullanıcı (site yönetimi), tek nokta (bodrum), tek ekran (haftalık karne).

### 6. "Wilo SiBoost zaten kaçak algılama sunuyor. Farkınız ne?"
SiBoost'un SCADA kaçak algılamasının yöntemi ve ne raporladığı yayımlanmamış; bunu Wilo'ya soru olarak yazdık. Bizim önerimiz debi (L/sa), maliyet (TL/ay) ve tür vermek. Bunu kontrol ünitesinin zaten taşıdığı kalkış sayacından, Wilo-Monitor modülü olarak yapıyoruz. Yani rakip değil, Wilo'nun mevcut ürününe eklenen bir katman.
