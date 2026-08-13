"""
=====================================================================
NETFLIX VERİ ANALİZİ
=====================================================================

Netflix katalog veri seti üzerinde NumPy, Pandas ve Matplotlib ile
yapılmış keşifsel veri analizi (EDA) çalışması.

Veri seti, 2021 yılına kadar Netflix'te yayınlanmış yaklaşık 8800
film ve diziyi; yayın yılı, ülke, tür, yaş sınırı ve süre gibi
bilgileriyle birlikte içerir.

Analizde cevap aranan sorular:
  - Katalog ne kadar güncel? Hangi dönemin yapımları ağırlıkta?
  - Film mi dizi mi baskın?
  - İçerik üretimi hangi ülkelerde yoğunlaşıyor?
  - Hangi kategoriler öne çıkıyor?
  - Katalog hangi yaş grubunu hedefliyor?

Veri kaynağı : https://www.kaggle.com/datasets/shivamb/netflix-shows
Çalıştırmak  : py netflix_veri_analizi.py
Gereksinimler: numpy, pandas, matplotlib

netflix_titles.csv dosyası bu betikle aynı klasörde olmalıdır.
Grafikler ekranda açılır; devam etmek için pencereyi kapatmak yeterlidir.
=====================================================================
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


# =====================================================================
# BÖLÜM 0: VERİ SETİNİN YÜKLENMESİ
# =====================================================================

# Ham katalog verisi okunuyor. Her satır bir film ya da diziyi temsil eder.
df = pd.read_csv("netflix_titles.csv")

print("\n=== VERİ SETİNİN YÜKLENMESİ ===")
print("Satır sayısı:", df.shape[0])
print("Sütun sayısı:", df.shape[1])
print("Sütunlar:", list(df.columns))
# 8807 içerik, 12 sütun. Sütunların büyük kısmı metin; tek sayısal alan release_year.

# =====================================================================
# BÖLÜM 1: YAYIN YILI İSTATİSTİKLERİ (NumPy)
# =====================================================================

print("\n=== BÖLÜM 1: YAYIN YILI İSTATİSTİKLERİ ===")

# Yayın yılı sütunu, hızlı vektörel hesaplama için NumPy dizisine alınıyor.
yillar = np.array(df["release_year"])

print("\n[1.1] Yayın yılı dizisi")
print("Dizi tipi:", type(yillar))
print("Veri tipi:", yillar.dtype)
print("Eleman sayısı:", len(yillar))
print("İlk 10 değer:", yillar[:10])
# Sütunda eksik değer yok ve tamamı tam sayı; bu yüzden ön temizlik gerekmiyor.

# Dağılımın merkezi ve yayılımı: ortalama, medyan, standart sapma ve uç değerler.
ortalama = np.mean(yillar)
medyan = np.median(yillar)
standart_sapma = np.std(yillar)
en_kucuk = np.min(yillar)
en_buyuk = np.max(yillar)

print("\n[1.2] Temel istatistikler")
print("Ortalama:", round(ortalama, 2))
print("Medyan:", medyan)
print("Standart sapma:", round(standart_sapma, 2))
print("Minimum:", en_kucuk)
print("Maksimum:", en_buyuk)
# Ortalama (2014.18) medyandan (2017) küçük: dağılım sola çarpık.
# Az sayıdaki çok eski yapım ortalamayı aşağı çekiyor.

# Katalog ne kadar güncel? Boolean indeksleme ile 2015 sonrası içeriğin payı.
sonra_2015 = (yillar > 2015).sum()
oran = sonra_2015 / len(yillar) * 100

print("\n[1.3] Katalogun güncelliği")
print("2015'ten sonra yayınlanan içerik sayısı:", sonra_2015)
print("Yüzdesi: %", round(oran, 1))
# Katalogun yaklaşık üçte ikisi 2015 sonrası. Netflix güncel içeriğe ağırlık veriyor.

# Yapımların on yıllık dönemlere dağılımı (histogram).
bins = np.arange(1920, 2030, 10)
sayilar, kenarlar = np.histogram(yillar, bins=bins)

print("\n[1.4] On yıllık dönemlere dağılım")
for i in range(len(sayilar)):
    print(kenarlar[i], "-", kenarlar[i + 1] - 1, ":", sayilar[i], "içerik")
# Katalog neredeyse tamamen 2010-2019 döneminde toplanmış; öncesi çok seyrek.

# Kaç farklı yayın yılı temsil ediliyor?
farkli_yillar = np.unique(yillar)

print("\n[1.5] Temsil edilen yayın yılları")
print("Farklı release_year sayısı:", len(farkli_yillar))
print("En eski yıl:", farkli_yillar[0], "- En yeni yıl:", farkli_yillar[-1])
# Aralık 1925-2021 (96 yıl) ama yalnızca 74 farklı yıl var:
# bazı yıllardan katalogda hiç yapım yok.

# =====================================================================
# BÖLÜM 2: KATALOG YAPISININ İNCELENMESİ (Pandas)
# =====================================================================

print("\n=== BÖLÜM 2: KATALOG YAPISI ===")

# Veri setine ilk bakış: örnek satırlar, sütun tipleri ve sayısal özet.
print("\n[2.1] Veri setine ilk bakış")
print("İlk 10 satır:")
print(df.head(10))

print("\nVeri seti bilgileri:")
df.info()  # info() çıktıyı kendisi bastığı için print içine alınmaz

print("\nİstatistiksel özet:")
print(df.describe())
# describe() yalnızca release_year'ı gösteriyor, çünkü tek sayısal sütun o.

# Veri kalitesi kontrolü: hangi sütunlarda ne kadar boşluk var?
eksik_degerler = df.isnull().sum()

print("\n[2.2] Eksik veri kontrolü")
print("Her sütundaki eksik değer sayısı:")
print(eksik_degerler)
# En çok eksik veri director sütununda. Dizilerde tek bir yönetmen
# yazılmadığı için bu beklenen bir durum, hatalı veri değil.

# Katalog kompozisyonu: film mi dizi mi ağırlıkta?
tip_sayilari = df["type"].value_counts()

print("\n[2.3] Film ve dizi dağılımı")
print(tip_sayilari)
# 6131 film / 2676 dizi — katalogun yaklaşık %70'i film.

# Süre analizleri yalnızca filmler için anlamlı olduğundan ayrı bir tablo çıkarılıyor.
movies_df = df[df["type"] == "Movie"].copy()  # yeni sütun ekleneceği için copy()

print("\n[2.4] Yalnızca filmleri içeren tablo")
print("movies_df satır sayısı:", len(movies_df))
print(movies_df[["title", "release_year", "duration"]].head())
# Satır sayısı yukarıdaki Movie sayısıyla birebir aynı; filtre doğru çalışıyor.

# Üretim coğrafyası: katalogda hangi ülkeler baskın?
ilk10_ulke = df["country"].value_counts().head(10)

print("\n[2.5] Üretim coğrafyası - ilk 10 ülke")
print(ilk10_ulke)
# ABD açık ara önde. "United States, India" gibi ortak yapımlar bu sayımda
# ayrı bir kategori olarak görünür; ülke bazlı kesin toplam için ayrıştırma gerekir.

# Kategori dağılımı. Bir içerik birden fazla türe ait olabildiği için
# önce virgülden ayrılıp explode ile ayrı satırlara bölünüyor.
turler = df["listed_in"].dropna().str.split(", ").explode()
ilk5_tur = turler.value_counts().head(5)

print("\n[2.6] En popüler 5 kategori")
print(ilk5_tur)
# International Movies ve Dramas başı çekiyor:
# Netflix'in uluslararası içeriğe verdiği ağırlık burada net görülüyor.

# Yıllara göre üretim hacmi ve zirve yılı.
yillara_gore = df.groupby("release_year").size()
en_cok_yil = yillara_gore.idxmax()
en_cok_adet = yillara_gore.max()

print("\n[2.7] Yıllara göre üretim hacmi")
print(yillara_gore)
print("En çok içerik yayınlanan yıl:", en_cok_yil, "-", en_cok_adet, "içerik")
# Zirve 2018'de (1147 içerik). Sonrasındaki düşüş gerçek bir daralma değil;
# veri seti 2021'de toplandığı için son yıllar eksik kalıyor.

# Süre analizi: "90 min" gibi metin değerler sayısala çevriliyor.
# Filmlerde format her zaman "<sayı> min" olduğu için sadece birim atılıyor.
movies_df["sure_dakika"] = movies_df["duration"].str.replace(" min", "", regex=False).astype(float)
en_uzun_5 = movies_df.nlargest(5, "sure_dakika")[["title", "duration", "release_year"]]

print("\n[2.8] Film süreleri")
print("En uzun 5 film:")
print(en_uzun_5)
print("Ortalama film süresi:", round(movies_df["sure_dakika"].mean(), 1), "dakika")
# Ortalama 99.6 dakika ile standart sinema süresine yakın.
# 300 dakikayı aşan yapımlar ise belgesel, konser kaydı veya
# interaktif yapımlar (ör. Black Mirror: Bandersnatch) gibi istisnalar.

# =====================================================================
# BÖLÜM 3: GÖRSELLEŞTİRME (Matplotlib)
# =====================================================================

print("\n=== BÖLÜM 3: GÖRSELLEŞTİRME ===")
print("Grafikler ekranda açılacak, devam etmek için pencereyi kapatınız.")


# Grafik 1 - Katalogun film / dizi dağılımı
plt.figure(figsize=(7, 5))
plt.bar(tip_sayilari.index, tip_sayilari.values, color="red")

plt.title("Netflix Movie ve TV Show Sayıları")
plt.xlabel("İçerik Türü")
plt.ylabel("İçerik Sayısı")

plt.show()
# Film çubuğu dizi çubuğunun yaklaşık iki katı yüksekliğinde.

# Grafik 2 - Üretim hacminin yıllar içindeki seyri
plt.figure(figsize=(10, 5))
plt.plot(yillara_gore.index, yillara_gore.values, color="red")

plt.title("Yıllara Göre İçerik Sayısı")
plt.xlabel("Yayın Yılı")
plt.ylabel("İçerik Sayısı")

plt.show()
# 2000'lere kadar çizgi neredeyse düz; 2015 sonrası sert bir yükselişle
# 2018'de zirve yapıyor. Netflix'in içerik yatırımının büyüme eğrisi.

# Grafik 3 - En çok içerik üreten ilk 10 ülke
# Ülke adları uzun olduğu için dikey bar yerine yatay bar tercih edildi.
plt.figure(figsize=(10, 6))
plt.barh(ilk10_ulke.index, ilk10_ulke.values, color="red")

plt.title("En Çok İçerik Üreten İlk 10 Ülke")
plt.xlabel("İçerik Sayısı")
plt.ylabel("Ülke")
plt.gca().invert_yaxis()  # en büyük değer en üstte görünsün

plt.tight_layout()
plt.show()
# ABD, ikinci sıradaki Hindistan'ın yaklaşık üç katı içerikle listeyi domine ediyor.


# Grafik 4 - Hedef kitle profili: yaş sınırı (rating) dağılımı
rating_sayilari = df["rating"].value_counts()

# Kategori sayısı pastaya sığmayacak kadar fazla.
# İlk 6 kategori korunup geri kalanlar "Diğer" altında toplanıyor.
pasta_veri = rating_sayilari.head(6)
pasta_veri["Diğer"] = rating_sayilari[6:].sum()

plt.figure(figsize=(8, 8))
plt.pie(pasta_veri.values, labels=pasta_veri.index, autopct="%1.1f%%")

plt.title("Rating (Yaş Sınırı) Dağılımı")

plt.show()
# TV-MA (%36.4) ve TV-14 (%24.5) birlikte pastanın %60'ından fazlasını kaplıyor:
# katalog ağırlıklı olarak yetişkin ve genç yetişkin izleyiciye yönelik.

# Grafik 5 - Dört bulgunun tek panoda özeti
fig, axs = plt.subplots(2, 2, figsize=(14, 10))
fig.suptitle("Netflix Veri Analizi Özeti")

# Sol üst: içerik türü
axs[0, 0].bar(tip_sayilari.index, tip_sayilari.values, color="red")
axs[0, 0].set_title("Movie ve TV Show Sayıları")
axs[0, 0].set_xlabel("İçerik Türü")
axs[0, 0].set_ylabel("İçerik Sayısı")

# Sağ üst: yıllara göre içerik
axs[0, 1].plot(yillara_gore.index, yillara_gore.values, color="red")
axs[0, 1].set_title("Yıllara Göre İçerik Sayısı")
axs[0, 1].set_xlabel("Yayın Yılı")
axs[0, 1].set_ylabel("İçerik Sayısı")

# Sol alt: ilk 10 ülke
axs[1, 0].barh(ilk10_ulke.index, ilk10_ulke.values, color="red")
axs[1, 0].set_title("En Çok İçerik Üreten İlk 10 Ülke")
axs[1, 0].set_xlabel("İçerik Sayısı")
axs[1, 0].set_ylabel("Ülke")
axs[1, 0].invert_yaxis()

# Sağ alt: rating dağılımı
axs[1, 1].pie(pasta_veri.values, labels=pasta_veri.index, autopct="%1.1f%%")
axs[1, 1].set_title("Rating Dağılımı")

plt.tight_layout()
plt.show()
# Dört grafik bir arada okunduğunda katalogun profili netleşiyor:
# ABD merkezli, 2015 sonrası hızla büyüyen, film ağırlıklı ve
# yetişkin izleyiciyi hedefleyen bir içerik kütüphanesi.


print("\nAnaliz tamamlandı.")
