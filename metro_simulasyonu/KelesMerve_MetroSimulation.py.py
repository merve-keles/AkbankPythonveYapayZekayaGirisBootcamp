from collections import defaultdict, deque
import heapq
from typing import Dict, List, Set, Tuple, Optional

class Istasyon:         #metrodaki her bir istasyonu ve bağlantılarını temsil etmek için yazılmıştır. 
    def __init__(self, idx: str, ad: str, hat: str):             #metro istasyonları
        self.idx = idx
        self.ad = ad
        self.hat = hat
        self.komsular: List[Tuple['Istasyon', int]] = [] 

    def komsu_ekle(self, istasyon: 'Istasyon', sure: int):       #bağlantı istasyonları
        self.komsular.append((istasyon, sure))

class MetroAgi:
    def __init__(self):
        self.istasyonlar: Dict[str, Istasyon] = {}                  #tüm istasyonları saklar (idx->istasyon)
        self.hatlar: Dict[str, List[Istasyon]] = defaultdict(list)  #hatlara göre istasyonları gruplar

    def istasyon_ekle(self, idx: str, ad: str, hat: str) -> None:
        if idx not in self.istasyonlar:            #istasyon daha önce eklenmemişse
            istasyon = Istasyon(idx, ad, hat)      #yeni bir istasyon nesnesi oluştur
            self.istasyonlar[idx] = istasyon       #istasyonu ekle
            self.hatlar[hat].append(istasyon)      #istasyonu bulunduğu hatta ekle

    def baglanti_ekle(self, istasyon1_id: str, istasyon2_id: str, sure: int) -> None:
        istasyon1 = self.istasyonlar[istasyon1_id]  #ilk istasyonu al
        istasyon2 = self.istasyonlar[istasyon2_id]  #ikinci istasyonu al
        istasyon1.komsu_ekle(istasyon2, sure)       #ilk istasyona ikinciyi komşu olarak ekle
        istasyon2.komsu_ekle(istasyon1, sure)       #ikinci istasyona ilki komşu olarak ekle

    def en_az_aktarma_bul(self, baslangic_id: str, hedef_id: str) -> Optional[Tuple[List[Istasyon], int, int]]:
        """BFS algoritması kullanarak en az aktarmalı rotayı bulur ve ücreti hesaplar."""
        if baslangic_id not in self.istasyonlar or hedef_id not in self.istasyonlar:  #geçersiz bşlngç-bitiş
            return None

        baslangic = self.istasyonlar[baslangic_id]    #başlangıç istasyonunu al
        hedef = self.istasyonlar[hedef_id]            #bitiş istasyonunu al

        kuyruk = deque([(baslangic, [baslangic], 0)])    #mevcut_istasyon, rota, aktarma_sayisi
        ziyaret_edildi = set()                           #ziyaret edilen istasyonları saklar

        while kuyruk:
            mevcut_istasyon, rota, aktarma_sayisi = kuyruk.popleft()   #kuyruktan bir eleman al

            if mevcut_istasyon == hedef:                   #hedefe ulaşıldıysa
                ucret = 25 + (aktarma_sayisi * 5)          #ücret hesapla: İlk biniş 25 TL, her aktarma 5 TL
                return rota, aktarma_sayisi, ucret         #rotayı, aktarma sayısını ve ücreti döndür

            if mevcut_istasyon not in ziyaret_edildi:      #istasyon daha önce ziyaret edilmemişse
                ziyaret_edildi.add(mevcut_istasyon)        #istasyonu ziyaret edildi olarak işaretle
                for komsu, _ in mevcut_istasyon.komsular:  #komşu istasyonları gez
                    if komsu not in ziyaret_edildi:        #komşu ziyaret edilmemişse
                        yeni_aktarma_sayisi = aktarma_sayisi    #aktarma sayısını güncelle
                        if komsu.hat != mevcut_istasyon.hat:    #hat değişikliği varsa
                            yeni_aktarma_sayisi += 1       #aktarma sayısını artır
                        kuyruk.append((komsu, rota + [komsu], yeni_aktarma_sayisi))   #kuyruğa ekle

        return None  #rota bulunamazsa none döndür


    def en_hizli_rota_bul(self, baslangic_id: str, hedef_id: str) -> Optional[Tuple[List[Istasyon], int, int, int]]:
    #A* algoritması kullanarak en hızlı rotayı bulur ve ücreti hesaplar
    #bşlngç/bitiş ist metro ağında yoksa none döndür
        if baslangic_id not in self.istasyonlar or hedef_id not in self.istasyonlar:
            return None

    #bşlngç/bitiş ist al
        baslangic = self.istasyonlar[baslangic_id]
        hedef = self.istasyonlar[hedef_id]

    #öncelik kuyruğu (heapq kullanılarak): 
    # (toplam_tahmini_sure, id(mevcut_istasyon), mevcut_istasyon, rota, toplam_sure, aktarma_sayisi)
    #başlangıçta kuyruk, başlangıç istasyonu ve boş bir rota ile başlatılır
        kuyruk = [(0, id(baslangic), baslangic, [baslangic], 0, 0)]
    
        ziyaret_edildi = set()    #ziyaret edilen ist takip etmek için küme oluştur

    #kuyruk boşalana kadar devam et
        while kuyruk:
        #kuyruktan en düşük tahmini süreye sahip elemanı al (heapq.heappop)
            _, _, mevcut_istasyon, rota, toplam_sure, aktarma_sayisi = heapq.heappop(kuyruk)

        #eğer mevcut ist bitiş ist ise
            if mevcut_istasyon == hedef:
                ucret = 25 + (aktarma_sayisi * 5)          #ücret hesapla: İlk biniş 25 TL, her aktarma 5 TL
                return rota, toplam_sure, aktarma_sayisi, ucret    #rotayı,top süreyi,aktarma say ve ücr döndür

            if mevcut_istasyon not in ziyaret_edildi:  #eğer mevcut ist daha önce ziyaret edilmemişse
                ziyaret_edildi.add(mevcut_istasyon)    #ist ziyaret edildi olarak işaretle
            
                for komsu, sure in mevcut_istasyon.komsular:    #mevcut ist komş gez
                    if komsu not in ziyaret_edildi:             #eğer komşu daha önce ziyaret edilmemişse
                        yeni_aktarma_sayisi = aktarma_sayisi    #akt sayısını güncele (eğer hat değişiyorsa)
                        if komsu.hat != mevcut_istasyon.hat:
                            yeni_aktarma_sayisi += 1

    #yeni rotayı, toplam süreyi ve aktarma sayısını hesapla ve kuyruğa ekle (heapq.heappush)
                        heapq.heappush(
                            kuyruk,
                            (
                                toplam_sure + sure,       #tahmini toplam süre
                                id(komsu),                #benzersiz kimlik (heapq'nin sıralama için kullanması için)
                                komsu,                    #komşu istasyon
                                rota + [komsu],           #yeni rota(mevcut rotaya komşuyu ekle)
                                toplam_sure + sure,       #toplam süre
                                yeni_aktarma_sayisi,      #yeni aktarma sayısı
                            ),
                        )

    #hedefe ulaşılamazsa none döndür
        return None

    
# örnek senaryolar
if __name__ == "__main__":
    metro = MetroAgi()
    
    # İstasyonlar ekleme
    # Kırmızı Hat
    metro.istasyon_ekle("K1", "Kızılay", "Kırmızı Hat")
    metro.istasyon_ekle("K2", "Ulus", "Kırmızı Hat")
    metro.istasyon_ekle("K3", "Demetevler", "Kırmızı Hat")
    metro.istasyon_ekle("K4", "OSB", "Kırmızı Hat")
    
    # Mavi Hat
    metro.istasyon_ekle("M1", "AŞTİ", "Mavi Hat")
    metro.istasyon_ekle("M2", "Kızılay", "Mavi Hat")  # Aktarma noktası
    metro.istasyon_ekle("M3", "Sıhhiye", "Mavi Hat")
    metro.istasyon_ekle("M4", "Gar", "Mavi Hat")
    
    # Turuncu Hat
    metro.istasyon_ekle("T1", "Batıkent", "Turuncu Hat")
    metro.istasyon_ekle("T2", "Demetevler", "Turuncu Hat")  # Aktarma noktası
    metro.istasyon_ekle("T3", "Gar", "Turuncu Hat")  # Aktarma noktası
    metro.istasyon_ekle("T4", "Keçiören", "Turuncu Hat")
    
    # Bağlantılar ekleme
    # Kırmızı Hat bağlantıları
    metro.baglanti_ekle("K1", "K2", 4)  # Kızılay -> Ulus
    metro.baglanti_ekle("K2", "K3", 6)  # Ulus -> Demetevler
    metro.baglanti_ekle("K3", "K4", 8)  # Demetevler -> OSB
    
    # Mavi Hat bağlantıları
    metro.baglanti_ekle("M1", "M2", 5)  # AŞTİ -> Kızılay
    metro.baglanti_ekle("M2", "M3", 3)  # Kızılay -> Sıhhiye
    metro.baglanti_ekle("M3", "M4", 4)  # Sıhhiye -> Gar
    
    # Turuncu Hat bağlantıları
    metro.baglanti_ekle("T1", "T2", 7)  # Batıkent -> Demetevler
    metro.baglanti_ekle("T2", "T3", 9)  # Demetevler -> Gar
    metro.baglanti_ekle("T3", "T4", 5)  # Gar -> Keçiören
    
    # Hat aktarma bağlantıları (aynı istasyon farklı hatlar)
    metro.baglanti_ekle("K1", "M2", 2)  # Kızılay aktarma
    metro.baglanti_ekle("K3", "T2", 3)  # Demetevler aktarma
    metro.baglanti_ekle("M4", "T3", 2)  # Gar aktarma
    
    # Test senaryoları
    print("\n=== Test Senaryoları ===")
    
    # Senaryo 1: AŞTİ'den OSB'ye
    print("\n1. AŞTİ'den OSB'ye:")
    sonuc = metro.en_az_aktarma_bul("M1", "K4")
    if sonuc:
        rota, aktarma_sayisi, ucret = sonuc
        print("En az aktarmalı rota:", " -> ".join(i.ad for i in rota))
        print(f"Aktarma sayısı: {aktarma_sayisi}")
        print(f"Toplam ücret: {ucret} TL")
    
    sonuc = metro.en_hizli_rota_bul("M1", "K4")
    if sonuc:
        rota, sure, aktarma_sayisi, ucret = sonuc
        print(f"En hızlı rota ({sure} dakika):", " -> ".join(i.ad for i in rota))
        print(f"Aktarma sayısı: {aktarma_sayisi}")
        print(f"Toplam ücret: {ucret} TL")
    
    # Senaryo 2: Batıkent'ten Keçiören'e
    print("\n2. Batıkent'ten Keçiören'e:")
    sonuc = metro.en_az_aktarma_bul("T1", "T4")
    if sonuc:
        rota, aktarma_sayisi, ucret = sonuc
        print("En az aktarmalı rota:", " -> ".join(i.ad for i in rota))
        print(f"Aktarma sayısı: {aktarma_sayisi}")
        print(f"Toplam ücret: {ucret} TL")
    
    sonuc = metro.en_hizli_rota_bul("T1", "T4")
    if sonuc:
        rota, sure, aktarma_sayisi, ucret = sonuc
        print(f"En hızlı rota ({sure} dakika):", " -> ".join(i.ad for i in rota))
        print(f"Aktarma sayısı: {aktarma_sayisi}")
        print(f"Toplam ücret: {ucret} TL")
    
    # Senaryo 3: Keçiören'den AŞTİ'ye
    print("\n3. Keçiören'den AŞTİ'ye:")
    sonuc = metro.en_az_aktarma_bul("T4", "M1")
    if sonuc:
        rota, aktarma_sayisi, ucret = sonuc
        print("En az aktarmalı rota:", " -> ".join(i.ad for i in rota))
        print(f"Aktarma sayısı: {aktarma_sayisi}")
        print(f"Toplam ücret: {ucret} TL")
    
    sonuc = metro.en_hizli_rota_bul("T4", "M1")
    if sonuc:
        rota, sure, aktarma_sayisi, ucret = sonuc
        print(f"En hızlı rota ({sure} dakika):", " -> ".join(i.ad for i in rota))
        print(f"Aktarma sayısı: {aktarma_sayisi}")
        print(f"Toplam ücret: {ucret} TL")