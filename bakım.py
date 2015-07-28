#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, os, shutil, urllib, re, tarfile
from bs4 import BeautifulSoup as bs
from datetime import datetime as tarih

class YAZILIM:
    def __init__(self, veri):
        self.IFADELER = []
        self.Arac_Al = Araclar()
        self.Veri = veri
        self.Parametreler = self.Veri[1:-1]
        self.Parametreler.append(self.Veri[-1])

        if '-yardım' in self.Parametreler and len(self.Parametreler) == 1:
            self.Arac_Al.Yardim_Ciktisi()

        self.KayitDurumu = 0
        self.KayitDosyasi = ""
        self.Surum = ""
        self.ArtikTemizlemeDurumu = 0
        self.BakimDurumu = 0
        self.GuncellemeDurumu = 0


        if '-k' in self.Parametreler:
            self.KayitDurumu = 1
            if len(self.Parametreler) > self.Parametreler.index('-k')+1 and not self.Parametreler[self.Parametreler.index('-k')+1].startswith('-'):
                self.KayitDosyasi = self.Parametreler[self.Parametreler.index('-k')+1]
        if '-a' in self.Parametreler:
            self.ArtikTemizlemeDurumu = 1
        
        if '-b' in self.Parametreler:
            self.BakimDurumu = 1
        
        if '-y' in self.Parametreler:
            Yetki = os.geteuid()
            if Yetki == 0:
                self.GuncellemeDurumu = 1
                if len(self.Parametreler) > self.Parametreler.index('-y')+1 and not self.Parametreler[self.Parametreler.index('-y')+1].startswith('-'):
                    self.Surum = self.Parametreler[self.Parametreler.index('-y')+1]
            else:
                print "-y parametresini kullanabilmeniz için işlemi sudo komutu ile (yetkili kullanıcı olarak) çalıştırmanız gerekiyor."
                self.IFADELER.append("%s: -y parametresi yetkili kullanıcı izni olmadan verildi. Çıkış yapılıyor..." %str(tarih.now()))
                if self.KayitDurumu:
                    if not self.KayitDosyasi == "":
                        self.KayitDosyasi = self.KayitDosyasi
                    else:
                        self.KayitDosyasi = "TARAYICIBAKIMI.KAYIT"
                    
                    self.Arac_Al.KAYIT_YAZDIR(self.KayitDosyasi, self.IFADELER)
                
        elif not "-k" in self.Parametreler and not "-a" in self.Parametreler and not "-b" in self.Parametreler and not "-y" in self.Parametreler:
            self.Arac_Al.Yardim_Ciktisi()

            
        
        """print "KayıtDurumu >>", self.KayitDurumu
        print "KayıtDosyası >>", self.KayitDosyasi
        print "Sürüm >>", self.Surum
        print "ArtıkTemizlemeDurumu >>", self.ArtikTemizlemeDurumu
        print "BakımDurumu >>", self.BakimDurumu
        print "GüncellemeDurumu >>", self.GuncellemeDurumu"""
        
        self.islemler(self.KayitDurumu, self.KayitDosyasi, self.Surum, self.ArtikTemizlemeDurumu, self.BakimDurumu, self.GuncellemeDurumu)
    
    def islemler(self, KayitDurumu, KayitDosyasi, Surum, ArtikTemizlemeDurumu, BakimDurumu, GuncellemeDurumu):
        KAYIT = os.getcwd()
        IFADELER = []
        if KayitDurumu:
            if KayitDosyasi != "":
                IFADELER.append("%s: Kayıt dosyası, %s ismiyle açılıyor..." %(str(tarih.now()), KayitDosyasi))
                print "Kayıt dosyası, %s ismiyle açılıyor..." %KayitDosyasi
                Dosya = open(KayitDosyasi, 'a')
                Dosya.close()
            else:
                KayitDosyasi = "TARAYICIBAKIMI.KAYIT"
                IFADELER.append("%s: Kayıt dosyası, %s ismiyle açılıyor..." %(str(tarih.now()), KayitDosyasi))
                print "Kayıt dosyası, TARAYICIBAKIMI.KAYIT ismiyle açılıyor..."
                Dosya = open("TARAYICIBAKIMI.KAYIT", 'a')
                Dosya.close()
        if ArtikTemizlemeDurumu:
            self.Arac_Al.ArtikTemizle(KayitDurumu, KayitDosyasi)
        
        if BakimDurumu:
            self.Arac_Al.ArtikTemizle(KayitDurumu, KayitDosyasi)
        
        
        if GuncellemeDurumu:
            Adres = self.Arac_Al.YeniSurumTespit()
            if Surum != "":
                if '.' in Surum:
                    self.Arac_Al.Guncellestir(KayitDosyasi, KayitDurumu, Surum, Adres)
                else:
                    self.Arac_Al.Guncellestir(KayitDosyasi, KayitDurumu, Surum+'.0', Adres)
            else:
                self.Arac_Al.Guncellestir(KayitDosyasi, KayitDurumu, Surum, Adres)
                
                
class Araclar:
    def Yardim_Ciktisi(self):
        print "-k [dosya_adı]: Yapılan işlemleri bir dosyaya kaydeder."
        print "-a : Artık verileri (cache) temizler."
        print "-b : Tarayıcıyı bakıma sokar."
        print "-y [sürüm]: Tarayıcıyı belirtilen sürüme günceller (Sürüm bulunamazsa en yeni sürüme güncellenir.)"
        sys.exit()
    def KAYIT_YAZDIR(self, KayitDosyasi, IFADELER):
        with open(KayitDosyasi, 'a') as Dosya:
            for i in IFADELER:
                Dosya.write(str(i) + '\n')
    def Guncellestir(self, KayitDosyasi, KayitDurumu, surum, Adres=""):
        self.KayitDurumu = KayitDurumu
        self.KayitDosyasi = KayitDosyasi
        self.surum = surum
        self.Adres = Adres
        
        self.IFADELER = []
        
        self.ILKDIZIN = os.getcwd()
        self.Kullanici_Dizini =  '/home/' + os.popen('users').read().split(' ')[0] + '/'
        os.chdir(self.Kullanici_Dizini)
        self.Olusturulan_Dosyalar= []
        
        self.islemlerDizini = os.getcwd()
        print "UYARI!: Yazılımı sudo komutu ile ya da yetkili kullanıcı olarak çalıştırmalısınız.\n\
Eğer zaten öyle yaptıysanız bu uyarıyı dikkate almayabilirsiniz."
        print "Firefox indiriliyor.."
        self.IFADELER.append("%s: Firefox indiriliyor..." %(str(tarih.now())))
        if surum == "":
            if not Adres == "":
                print "Bağlanılıyor %s" %Adres
                self.IFADELER.append("%s: Bağlanılıyor %s" %(str(tarih.now()), Adres))
                urllib.urlretrieve('%s' %Adres, 'firefox.tar.gz')
                self.Olusturulan_Dosyalar.append(os.getcwd() + os.sep + 'firefox.tar.gz')
                print "Dosya indirildi.. İndirilen dosya çıkartılıyor.. Lütfen bekleyiniz.."
                self.IFADELER.append("%s: Dosya indirildi.. İndirilen dosya çıkartılıyor.." %str(tarih.now()))
                Dosya = tarfile.open('firefox.tar.gz')
                Dosya.extractall()
            else:
                print "Hata! Adres %s geçersiz." %Adres
                self.IFADELER.append("%s: Hata! Adres %s geçersiz." %(str(tarih.now()), Adres))
                self.Cikis()
        else:
            try:
                if self.Bilgi_Al() == "i686":
                    Adres = "https://download.mozilla.org/?product=firefox-%s-SSL&os=linux&lang=tr" %surum
                elif self.Bilgi_Al() == "x86_64":
                    Adres = "https://download.mozilla.org/?product=firefox-%s-SSL&os=linux64&lang=tr" %surum
                print "Bağlanılıyor %s" %Adres
                self.IFADELER.append("%s: Bağlanılıyor %s" %(str(tarih.now()), Adres))
                urllib.urlretrieve(Adres, 'firefox.tar.gz')
                self.Olusturulan_Dosyalar.append(os.getcwd() + os.sep + 'firefox.tar.gz')
                print "Dosya indirildi.. İndirilen dosya çıkartılıyor.. Lütfen bekleyiniz.."
                self.IFADELER.append("%s: Dosya indirildi.. İndirilen dosya çıkartılıyor.." %str(tarih.now()))
                Dosya = tarfile.open('firefox.tar.gz')
                Dosya.extractall()
            except:
                Soru = raw_input("\n\nBir hata meydana geldi! Sürümde hata olabilir.\nEn yeni sürüm kurulsun mu ? (e/h)")
                self.IFADELER.append("%s: Bir hata meydana geldi! Sürümde hata olabilir." %str(tarih.now()))
                YANITLAR = ["e", "evet"]
                if Soru.lower() in YANITLAR:
                    Adres = self.YeniSurumTespit()
                    self.Guncellestir(KayitDosyasi, KayitDurumu, "", Adres)
                else:
                    self.Cikis()

        for isim in Dosya.getnames():
            print isim
            self.Olusturulan_Dosyalar.append(os.getcwd() + os.sep + isim)

        print "Dosya çıkartıldı."
        self.IFADELER.append("%s: Dosya çıkartıldı." %str(tarih.now()))
        print "Sistemdeki firefox dizini tespit ediliyor.. Lütfen bekleyiniz.."
        self.IFADELER.append("%s: Sistemdeki firefox dizini tespit ediliyor.." %str(tarih.now()))
        
        TespitDizini = ""
        firefoxDizini = ""
        firefoxYalnizcaDizin = ""
        self.DosyaSayaci = 0
        os.chdir('/')
        
        for Kok, Dizinler, Dosyalar in os.walk('.'):
            for dizin in Dizinler:
                Tam_Yol = os.path.join(Kok, dizin)
                if (dizin == "firefox" or dizin == "MozillaFirefox" or dizin == "Firefox") and Tam_Yol.split('/')[1] == 'usr'\
                and Tam_Yol.split('/')[2] == 'lib' and Tam_Yol.split('/')[3] == dizin and len(Tam_Yol.split('/')) == 4:
                    TespitDizini = Tam_Yol
                    firefoxDizini = Tam_Yol
                    firefoxYalnizcaDizin = dizin
                else:
                    TespitDizini = "YOK"
                    
        if firefoxDizini != "":
            firefoxDizini = firefoxDizini[1:-1] + firefoxDizini[-1]
            print "Tespit edilen firefox dizini : %s" %firefoxDizini
            self.IFADELER.append("%s: Tespit edilen firefox dizini : %s" %(str(tarih.now()), firefoxDizini))
            
        else:
            print "Firefox dizini tespit edilemedi."
            self.IFADELER.append("%s: Firefox dizini tespit edilemedi." %str(tarih.now()))
            firefoxDizini = raw_input("Lütfen sisteminizdeki firefox dizinini giriniz : ")
            self.IFADELER.append("%s: Girilen firefox dizini : %s"%(str(tarih.now()), firefoxDizini))
            firefoxYalnizcaDizin = firefoxDizini.split('/')[-1]
        
        
        print "%s dizini yedek amaçlı kullanıcı dizinine kopyalanıyor.. Lütfen bekleyiniz.." %firefoxYalnizcaDizin
        self.IFADELER.append("%s: %s dizini yedek amaçlı kullanıcı dizinine kopyalanıyor.." %(str(tarih.now()), firefoxYalnizcaDizin))
        
        os.chdir(self.Kullanici_Dizini)
        
        self.YedekDizinleri = []
        self.YedekSayilari = []
        for i in os.listdir('.'):
            if '%s_YeDeK' %firefoxYalnizcaDizin  in i and i.replace('%s_YeDeK' %firefoxYalnizcaDizin, '', 1).isdigit():
                self.YedekDizinleri.append(i)
                self.YedekDizinleri.sort()
        if self.YedekDizinleri == []:
            self.DosyaSayaci = 0
        else:
            for i in self.YedekDizinleri:
                self.YedekSayilari.append(i.replace('%s_YeDeK' %firefoxYalnizcaDizin, '', 1))
                self.YedekSayilari.sort()
        
        
        try:
            self.DosyaSayaci = self.YedekSayilari[-1]
        except:
            try:
                self.DosyaSayaci = self.YedekSayilari[0]
            except:
                self.DosyaSayaci = 0



        self.DosyaSayaci = int(self.DosyaSayaci) + 1
        
        
        try:    
            shutil.copytree(firefoxDizini, './%s_YeDeK%s' %(firefoxYalnizcaDizin, self.DosyaSayaci))
        except:
            print "Yedek alınamadı! Çıkış yapılıyor.."
            self.IFADELER.append("%s: Yedek alınamadı! Çıkış yapılıyor.." %str(tarih.now()))
            self.Cikis()
            
            
            
        print "Dosya kopyalama tamamlandı."
        self.IFADELER.append("%s: Dosya kopyalama tamamlandı." %str(tarih.now()))
        
        print "%s dizinine geçiş yapılıyor.." %firefoxDizini
        self.IFADELER.append("%s: %s dizinine geçiş yapılıyor.." %(str(tarih.now()), firefoxDizini))
        os.chdir(firefoxDizini)
        
        print "%s içerisindeki tüm dosyalar ve dizinler siliniyor.." %firefoxDizini
        self.IFADELER.append("%s: %s içerisindeki tüm dosyalar ve dizinler siliniyor.." %(str(tarih.now()), firefoxDizini))
        
        for Sil in os.listdir('.'):
            try:
                if os.path.isdir(Sil):
                    shutil.rmtree(Sil)
                else:
                    os.remove(Sil)
            except:
                print "Lütfen işlemi yetkili kullanıcı olarak çalıştırınız."
                self.IFADELER.append("%s: Lütfen işlemi yetkili kullanıcı olarak çalıştırınız." %str(tarih.now()))
                self.Cikis()
                
        print "Silme işlemi tamamlandı. İndirilen yeni sürüm %s dizinine kopyalanıyor.." %firefoxDizini
        self.IFADELER.append("%s: Silme işlemi tamamlandı. İndirilen yeni sürüm %s dizinine kopyalanıyor.." %(str(tarih.now()), firefoxDizini))
        os.chdir(self.islemlerDizini)
        os.chdir('firefox')
        
        for Kopyala in os.listdir('.'):
            if os.path.isdir(Kopyala):
                shutil.copytree(Kopyala, '%s/%s' %(firefoxDizini, Kopyala))
            else:
                shutil.copy(Kopyala, firefoxDizini)
        print "Kopyalama tamamlandı!"
        self.IFADELER.append("%s: Kopyalama tamamlandı!" %str(tarih.now()))
        
        if surum == "":
            print "Firefox en yeni sürüme yükseltildi." 
            self.IFADELER.append("%s: Firefox en yeni sürüme yükseltildi." %str(tarih.now()))
        else:
            print "Firefox %s sürümüne yükseltildi." %surum
            self.IFADELER.append("%s: Firefox %s sürümüne yükseltildi." %(str(tarih.now()), surum))
        self.Cikis()
    
    def ArtikTemizle(self, KayitDurumu, KayitDosyasi):
        self.KayitDurumu = KayitDurumu
        self.KayitDosyasi = KayitDosyasi
        
        KAYIT = os.getcwd()
        self.Olusturulan_Dosyalar = []
        self.IFADELER = []
        self.KullaniciDizini = os.popen("echo $HOME").read().replace('\n', '', -1)
        if self.KullaniciDizini == "/root" or self.KullaniciDizini == "/root/":
            self.KullaniciDizini = '/home/' + os.popen("users").read().split(' ')[0].replace('\n', '', -1)
        print "Kullanıcı dizini tespit edildi!: %s" %self.KullaniciDizini
        self.IFADELER.append("%s: Kullanıcı dizini tespit edildi!: %s" %(str(tarih.now()), self.KullaniciDizini))
        os.chdir('%s/.cache/mozilla/firefox' %self.KullaniciDizini) 
        for i in os.listdir('.'):
            print "Artık dosya siliniyor %s" %(os.getcwd() + os.sep + i)
            Sor = raw_input("Dosya silinsin mi ? : %s (e/h)" %(os.getcwd() + os.sep + i))
            self.IFADELER.append("%s: Artık dosya siliniyor %s" %(str(tarih.now()), (os.getcwd() + os.sep + i)))
            if os.path.isdir(i):
                if Sor.lower() == "e":
                    shutil.rmtree(i)
            else:
                if Sor.lower() == "e":
                    os.remove(i)
                        
        os.chdir(KAYIT)
        if KayitDurumu:
            self.KAYIT_YAZDIR(KayitDosyasi, self.IFADELER)
    
    
    def Cikis(self):
        if self.Olusturulan_Dosyalar != []:
            self.Olusturulan_Dosyalar.reverse()
            for Dosya in self.Olusturulan_Dosyalar:
                os.chdir(os.path.dirname(Dosya))
                print "Dosya siliniyor %s" %Dosya
                self.IFADELER.append('%s: Dosya siliniyor %s' %(str(tarih.now()), Dosya))
                if os.path.isdir(Dosya):
                    shutil.rmtree(Dosya)
                else:
                    try:
                        os.remove(Dosya)
                    except: pass
            os.chdir(self.ILKDIZIN)
        
        if self.KayitDurumu:
            self.KAYIT_YAZDIR(self.KayitDosyasi, self.IFADELER)
        
        sys.exit()
    
    def YeniSurumTespit(self):
        bit = self.Bilgi_Al()
        if bit == "i686":
            Kodlar = urllib.urlopen('https://www.mozilla.org/tr/firefox/new/').read()
            KARISTIR = bs(Kodlar)
            Bul1 = KARISTIR.find('li', {"class" : "os_linux"})
            KARISTIR = bs(str(Bul1))
            Bul = KARISTIR.find('a', {"class" : "download-link"})
            SATIR = str(Bul).split('\n')[0]
        
            for i in SATIR.split(' '):
                if 'href=' in i:
                    Adres = i        
            Adres = Adres.replace('href=', '', 1)
            Adres = Adres.replace('>', '', -1)
            Adres = Adres[1: -1].replace('amp;', '')
            return Adres
        elif bit == "x86_64":
            Kodlar = urllib.urlopen('https://www.mozilla.org/tr/firefox/new/').read()
            KARISTIR = bs(Kodlar)
            Bul1 = KARISTIR.find('li', {"class" : "os_linux64"})
            KARISTIR = bs(str(Bul1))
            Bul = KARISTIR.find('a', {"class" : "download-link"})
            SATIR = str(Bul).split('\n')[0]
            
            for i in SATIR.split(' '):
                if 'href=' in i:
                    Adres = i
            
            Adres = Adres.replace('href=', '', 1)
            Adres = Adres.replace('>', '', -1)
            Adres = Adres[1: -1].replace('amp:', '')
            return Adres
            
            
            
    def Bilgi_Al(self):
        return os.popen("uname -m").read().replace('\n', '', -1)
    
        

        

if __name__ == "__main__":
    Arac_Al = Araclar()
    if Arac_Al.Bilgi_Al() == "i686" or Arac_Al.Bilgi_Al() == "x86_64":
        Komutlar = sys.argv
    
        if len(Komutlar) >= 2:
            UYGULAMA = YAZILIM(Komutlar)
        else:
            Arac_Al.Yardim_Ciktisi()
    else:
        print "Bu yazılım yalnızca linux 32bit ve linux 64bit uyumludur."
        
