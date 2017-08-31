#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, os, shutil, urllib, re, tarfile, time
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
        self.rescueFolder = ""
        self.rescueFirefox = 0
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
        
        if '-r' in self.Parametreler:
            permission = os.geteuid()            
            if permission == 0:
                self.rescueFirefox = 1
                if len(self.Parametreler) > self.Parametreler.index('-r')+1 and not self.Parametreler[self.Parametreler.index('-r')+1].startswith('-'):
                    self.rescueFolder = self.Parametreler[self.Parametreler.index('-r')+1]
            else:
                print "-r parametresini kullanabilmeniz için işlemi yetkili kullanıcı olarak çalıştırmanız gerekiyor."
                self.IFADELER.append("%s: -r parametresi yetkili kullanıcı izni olmadan verildi. Çıkış yapılıyor..." %str(tarih.now()))
                
                if self.KayitDurumu:
                    if not self.KayitDosyasi == "":
                        self.KayitDosyasi = self.KayitDosyasi
                    else:
                        self.KayitDosyasi = "TARAYICIBAKIMI.KAYIT"
                    
                    self.Arac_Al.KAYIT_YAZDIR(self.KayitDosyasi, self.IFADELER)
            
        
        if '-y' in self.Parametreler:
            Yetki = os.geteuid()
            if Yetki == 0:
                self.GuncellemeDurumu = 1
                if len(self.Parametreler) > self.Parametreler.index('-y')+1 and not self.Parametreler[self.Parametreler.index('-y')+1].startswith('-'):
                    self.Surum = self.Parametreler[self.Parametreler.index('-y')+1]
            else:
                print "-y parametresini kullanabilmeniz için işlemi yetkili kullanıcı olarak çalıştırmanız gerekiyor."
                self.IFADELER.append("%s: -y parametresi yetkili kullanıcı izni olmadan verildi. Çıkış yapılıyor..." %str(tarih.now()))
                if self.KayitDurumu:
                    if not self.KayitDosyasi == "":
                        self.KayitDosyasi = self.KayitDosyasi
                    else:
                        self.KayitDosyasi = "TARAYICIBAKIMI.KAYIT"
                    
                    self.Arac_Al.KAYIT_YAZDIR(self.KayitDosyasi, self.IFADELER)
                
        elif not "-k" in self.Parametreler and not "-a" in self.Parametreler and not "-b" in self.Parametreler and not "-y" in self.Parametreler and not "-r" in self.Parametreler:
            self.Arac_Al.Yardim_Ciktisi()

            
        
        """print "KayıtDurumu >>", self.KayitDurumu
        print "KayıtDosyası >>", self.KayitDosyasi
        print "Sürüm >>", self.Surum
        print "ArtıkTemizlemeDurumu >>", self.ArtikTemizlemeDurumu
        print "BakımDurumu >>", self.BakimDurumu
        print "GüncellemeDurumu >>", self.GuncellemeDurumu"""
        
        self.islemler(self.KayitDurumu, self.KayitDosyasi, self.Surum, self.ArtikTemizlemeDurumu, self.BakimDurumu, self.GuncellemeDurumu, self.rescueFirefox, self.rescueFolder)
    
    def islemler(self, KayitDurumu, KayitDosyasi, Surum, ArtikTemizlemeDurumu, BakimDurumu, GuncellemeDurumu, rescueFirefox, rescueFolder):
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
        
        if rescueFirefox:
            self.Arac_Al.rescueffox(KayitDurumu, KayitDosyasi, rescueFolder)
        
        if GuncellemeDurumu and not self.rescueFirefox:
            Adres = self.Arac_Al.YeniSurumTespit()
            if Surum != "":
                if not os.path.exists(Surum):
                    if '.' in Surum:
                        self.Arac_Al.Guncellestir(KayitDosyasi, KayitDurumu, Surum, Adres)
                    else:
                        self.Arac_Al.Guncellestir(KayitDosyasi, KayitDurumu, Surum+'.0', Adres)
                else:
                    self.Arac_Al.Guncellestir(KayitDosyasi, KayitDurumu, Surum, Adres, 1)
            else:
                self.Arac_Al.Guncellestir(KayitDosyasi, KayitDurumu, Surum, Adres)
                
                
class Araclar:
    sizeOfFile = 0
    saveTime = 0
    saveTime_ = 0
    bytesList = []
    counter = 0
    def findUserDir(self):
        res = os.popen('users').read().strip().split(' ')[0]
        if res == "root":
            return "/root/"
        else:
            return '/home/' + res + '/'
    
    def rescueFromFolder(self, folder, rescueMode=1):
        self.Kullanici_Dizini =  self.findUserDir()
        self.print_("Sistemdeki firefox dizini tespit ediliyor.. Bekleyin...")
        
        TespitDizini, firefoxDizini, firefoxYalnizcaDizin = self.detectFirefoxFolder()
        
        
        self.DosyaSayaci = 0
        

        if firefoxDizini != "":
            #firefoxDizini = firefoxDizini[1:-1] + firefoxDizini[-1]
            print "Tespit edilen firefox dizini : %s" %firefoxDizini
            self.IFADELER.append("%s: Tespit edilen firefox dizini : %s" %(str(tarih.now()), firefoxDizini))
            
        else:
            self.print_("Firefox dizini tespit edilemedi.")
            firefoxDizini = raw_input("Lütfen sisteminizdeki firefox dizinini girin : ")
            self.IFADELER.append("%s: Girilen firefox dizini : %s"%(str(tarih.now()), firefoxDizini))
            firefoxYalnizcaDizin = firefoxDizini.split('/')[-1]
        
        permis = raw_input("Belirtilen dizindeki tüm dosyalar yedeklendikten sonra silinecektir. Onay? [e/h] > ")
        if permis.lower() != 'e':
            sys.exit()
        
        self.print_("%s dizini yedek amaçlı kullanıcı dizinine kopyalanıyor.. Bekleyin..." %firefoxYalnizcaDizin)
        
        os.chdir(self.Kullanici_Dizini)
        
        self.DosyaSayaci = 1
        while "%s_YeDeK%s" %(firefoxYalnizcaDizin, self.DosyaSayaci) in os.listdir('.'):
            self.DosyaSayaci += 1

        
        firefoxCmd = os.popen("whereis firefox").read().strip().split()[1]
        fold = "./%s_YeDeK%s" %(firefoxYalnizcaDizin, self.DosyaSayaci)
        os.mkdir(fold)
        
        self.print_("Oluşturulan dizin: %s" %fold)     
        self.copyDir(firefoxDizini, fold)
        os.system("sudo ln -s %s %s/firefox_sym_link" %(os.popen("readlink -f %s" %firefoxCmd).read().strip(), fold))
        #shutil.copyfile(firefoxCmd, './%s_YeDeK%s/firefox_sym_link' %(firefoxYalnizcaDizin, self.DosyaSayaci))
        
        with open("%s/okubeni.txt" %fold, "w") as f:
            f.write("%s\nFirefox'u bu klasördeki sürümüne döndürmek için:\n1- %s dosyasını silin.\n2- Bu dizindeki firefox_sym_link dosyasını %s dizinine %s adıyla kopyalayın.\n3- %s dizinindeki her şeyi silin.\n4- Bu dizindeki her şeyi %s dizinine kopyalayın.\nBu kadar ;)\n%s" %("-"*80, firefoxCmd, os.path.dirname(firefoxCmd), os.path.basename(firefoxCmd), firefoxDizini, firefoxDizini, "-"*80))
        #try:    
        #shutil.copytree(firefoxDizini, './%s_YeDeK%s' %(firefoxYalnizcaDizin, self.DosyaSayaci))
        #except:
        #    print "Yedek alınamadı! Çıkış yapılıyor.."
        #    self.IFADELER.append("%s: Yedek alınamadı! Çıkış yapılıyor.." %str(tarih.now()))
        #    self.Cikis()
            
            
            
        self.print_("Dosya kopyalama tamamlandı.")
        self.print_("%s dizinine geçiş yapılıyor.." %firefoxDizini)
        os.chdir(firefoxDizini)
        
        self.print_("%s içerisindeki tüm dosyalar ve dizinler siliniyor.." %firefoxDizini)
        
        for Sil in os.listdir('.'):
            try:
                if os.path.isdir(Sil):
                    try:
                        shutil.rmtree(Sil)
                    except: os.remove(Sil)
                else:
                    os.remove(Sil)
            except:
                if os.geteuid() != 0:
                    self.print_("Hata! İşlemi yetkili kullanıcı olarak çalıştırın.")
                else:
                    self.print_("Dosyalar kopyalanırken hata oluştu!")
                self.Cikis()
                
        self.print_("Silme işlemi tamamlandı. Firefox dosyaları %s dizinine kopyalanıyor.." %firefoxDizini)
        os.chdir(self.ILKDIZIN)
        os.chdir(folder)
        
        for Kopyala in os.listdir('.'):
            if os.path.isdir(Kopyala):
                shutil.copytree(Kopyala, '%s/%s' %(firefoxDizini, Kopyala))
            elif os.path.isfile(Kopyala):
                shutil.copy(Kopyala, firefoxDizini)
                
        self.print_("Kopyalama tamamlandı!")
        self.print_("%s siliniyor..." %os.popen("whereis firefox").read().strip().split()[1])
        os.remove(firefoxCmd)
        
        self.print_("%s yoluna sembolik bağ oluşturuluyor... (%s)" %(firefoxDizini+"/firefox", firefoxCmd))
        os.system("ln -s %s/firefox %s" %(firefoxDizini, firefoxCmd))
        
    def rescueffox(self, saving, saveFile, rescueFolder):
        self.KayitDurumu = saving
        self.KayitDosyasi = saveFile
        self.IFADELER = []
        
        self.ILKDIZIN = os.getcwd()
        self.Kullanici_Dizini =  '/home/' + os.popen('users').read().split(' ')[0] + '/'
        os.chdir(self.Kullanici_Dizini)
        self.Olusturulan_Dosyalar= []
        
        self.islemlerDizini = os.getcwd()
        
        if os.path.dirname(rescueFolder) == rescueFolder and rescueFolder == os.path.basename(rescueFolder):
            rescueFolder = os.getcwd() + rescueFolder
        
        self.rescueFromFolder(rescueFolder)
        
        self.print_("Firefox belirtilen klasördeki dosyalarla kurtarıldı!")
        os.chdir(self.Kullanici_Dizini)
        self.Cikis()
        
    
    def print_(self, msg):
        if self.KayitDurumu:
            self.IFADELER.append("%s: %s" %(str(tarih.now()), msg))
        print(msg)
        
    def detectFirefoxFolder(self):
        getRes = os.popen("whereis firefox").read().strip().split()[1]
        folder = os.path.dirname(os.popen("readlink -f %s" %(getRes)).read().strip())
        if folder == getRes:
            folder = ""
        if self.confirmFolder(folder):
            return (folder, folder, os.path.basename(folder))
    
        potentialFolders = ["/usr/lib/firefox", "/usr/lib64/firefox", "/usr/lib64/Firefox", "/usr/lib64/MozillaFirefox", "/usr/lib/MozillaFirefox", "/usr/lib/Firefox", "/etc/firefox", "/etc/MozillaFirefox", "/etc/Firefox"]
        
        for folder in potentialFolders:
            sys.stdout.write("%s için bakılıyor... " %folder)
            if self.confirmFolder(folder):
                detectedFolder = folder
                fFoxFolder = folder
                justfFoxFolder = os.path.basename(folder)
                print "[+] Tespit edildi!"
                return (detectedFolder, fFoxFolder, justfFoxFolder)
            else:
                print "[-]"
                
        return ("YOK", "", "")
            
        
    
    def confirmFolder(self, folder):
        getRes = os.popen("whereis firefox").read().strip().split()[1]
        if not os.path.exists(folder):
            return 0
        
        size = 0
        fileNumber = 0
        folderNumber = 0
        for r, fo, fi in os.walk(folder):
            folderNumber += 1
            for f in fi:
                fileNumber += 1
                size += os.path.getsize(os.path.join(r, f))
        
        totalNumber = fileNumber+folderNumber
        if totalNumber > 40 and len(os.listdir(folder)) > 20 and size > 1024*1024*15:
            if "run-mozilla.sh" in os.listdir(folder) and ("firefox" in os.listdir(folder) or "firefox-bin" in os.listdir(folder)):
                if folder == os.path.dirname(os.popen("readlink -f %s" %getRes).read().strip()):
                    return 1
                
                
        return 0
        
    def copyDir(self, src, dst):
        for root, folders, files in os.walk(src):
            for d in folders:
                if not os.path.exists(os.path.join(root, d).replace(src, dst)):
                    os.mkdir(os.path.join(root, d).replace(src, dst))
            for f in files:
                sys.stdout.write("Kopyalanıyor %s... " %os.path.join(root, f))
                keep = str(tarih.now())
                try:
                    self.copy(os.path.join(root, f), (os.path.join(root, f).replace(src, dst)))
                except: 
                    print "[-] Hata!"
                    self.IFADELER.append("%s: Kopyalanıyor %s... [-] Hata! (%s)" %(keep, os.path.join(root, f), str(tarih.now())))
                    
                else:
                    print "[+] Tamam."
                    self.IFADELER.append("%s: Kopyalanıyor %s... [+] Tamam! (%s)" %(keep, os.path.join(root, f), str(tarih.now())))
    
        
    def copy(self, src, dst):
        if os.path.islink(src):
            linkto = os.readlink(src)
            os.symlink(linkto, dst)
        else:
            shutil.copy(src, dst)

    def Yardim_Ciktisi(self):
        print "-k [dosya_adı]: Yapılan işlemleri bir dosyaya kaydeder."
        print "-a : Artık verileri (cache) temizler."
        print "-b : Tarayıcıyı bakıma sokar."
        print "-r [klasör_yolu]: Belirtilen klasördeki yedek dosyalarını kullanarak firefox'u kurtarır."
        print "-y [sürüm]: Tarayıcıyı belirtilen sürüme günceller (Sürüm bulunamazsa en yeni sürüme güncellenir.)"
        print "\tya da\t"
        print "-y [dosya_yolu]: Tarayıcıyı belirtilen tar.gz dosyasındakileri kullanarak kurar."
        sys.exit()
    def KAYIT_YAZDIR(self, KayitDosyasi, IFADELER):
        with open(KayitDosyasi, 'a') as Dosya:
            for i in IFADELER:
                Dosya.write(str(i) + '\n')
    
    def optimization(self, bytes):
        if bytes >= 1024 and bytes < 1048576:
            return "%.2f" %(bytes/1024.0), "KiB"
        if bytes >= 1048576 and bytes < 1073741824:
            return "%.2f" %(bytes/1024.0/1024), "MiB"
        if bytes >= 1073741824:
            return "%.2f" %(bytes/1024.0/1024/1024), "GiB"
        elif bytes < 1024:
            return bytes, "bytes"
    
    def timeOptimization(self, seconds):
        if seconds >= 60 and seconds < 3600:
            return "%s dk. %s sn." %(int(seconds)/60, seconds-(int(seconds)/60*60))
        if seconds >= 3600:
            return "%s saat %s dk. %s sn." %(int(seconds)/60/60, int(seconds-(int(seconds)/60/60*60*60))/60, seconds-(int(seconds-(int(seconds)/60/60*60*60))/60*60))
        else:
            return "%s sn." %(seconds)
    
    def report(self, count, bs, ts):
        elapsedTime = time.time() - self.saveTime        
        bfrdownloaded = count*bs - self.sizeOfFile
        
        per = 100.0*count*bs/ts
        if per > 100: per = 100
        per = "%.2f" %per
        
        
        
        sys.stdout.write("\r%")
        sys.stdout.write(per)
        sys.stdout.write ("  |  ")
        #sys.stdout.write("\b"*(len(per)+1))
        
        seconds = 0
        dwnbytes = 0
        for size, sec in self.bytesList:
            seconds += sec
            dwnbytes += size
        
        #print self.bytesList
        
        remainingSec = 0
        
        if seconds != 0: 
            bytesPerSecond = float(dwnbytes)/seconds
            try:
                remainingSec = float(ts - count*bs)/bytesPerSecond
            except: pass
        else: bytesPerSecond = 0
        
        
        
        bps = self.optimization(bytesPerSecond)
        bps = "%s %s/saniye" %(bps[0], bps[1])
        sys.stdout.write(bps)
        
        
        remaining = " | %s kaldı.                     " %self.timeOptimization(int(remainingSec))
        sys.stdout.write(remaining)
        
        """if elapsedTime > 5:
            self.saveTime = time.time()
            
            
        
        if elapsedTime_ > 1:
            self.saveTime_ = time.time()
            bytesPerSecond = float(downloadedSize)/elapsedTime
            bps = self.optimization(bytesPerSecond)
            bps = "%s %s" %(bps[0], bps[1])
            
            
            sys.stdout.write(bps)
            
            #sys.stdout.write("\b"*(len(bps)+1))
            
            self.sizeOfFile = count*bs"""
        
        if elapsedTime > 1:
            self.saveTime = time.time()
            self.sizeOfFile = count*bs
            if len(self.bytesList) < 5:
                self.bytesList.append((bfrdownloaded, elapsedTime))
            elif len(self.bytesList) == 5:
                self.bytesList[self.counter] = (bfrdownloaded, elapsedTime)
                self.counter += 1
        
            if self.counter == 5:
                self.counter = 0
            
            
        
        
    
    def Guncellestir(self, KayitDosyasi, KayitDurumu, surum, Adres="", fromFile=0):
        self.KayitDurumu = KayitDurumu
        self.KayitDosyasi = KayitDosyasi
        self.surum = surum
        self.Adres = Adres
        
        self.IFADELER = []
        
        self.ILKDIZIN = os.getcwd()
        self.Kullanici_Dizini =  self.findUserDir()
        os.chdir(self.Kullanici_Dizini)
        self.Olusturulan_Dosyalar= []
        
        self.islemlerDizini = os.getcwd()

        
        if surum == "" and fromFile==0:
            if not Adres == "":
                self.print_("Firefox indiriliyor...")
                self.print_("Bağlanılıyor %s" %Adres)
                self.saveTime = time.time()
                try:
                    urllib.urlretrieve('%s' %Adres, 'firefox.tar.gz', reporthook=self.report)
                except KeyboardInterrupt:
                    self.print_("Ctrl+C")
                    self.Cikis()
                self.Olusturulan_Dosyalar.append(os.getcwd() + os.sep + 'firefox.tar.gz')
                print
                self.print_("Dosya indirildi... İndirilen dosya çıkartılıyor... Bekleyin...")
                self.fileToExtract = "firefox.tar.gz"
            else:
                self.print_("Hata! Adres %s geçersiz." %Adres)
                os.chdir(self.Kullanici_Dizini)
                self.Cikis()
        elif fromFile==0:
            try:
                if self.Bilgi_Al() == "i686":
                    Adres = "https://download.mozilla.org/?product=firefox-%s-SSL&os=linux&lang=tr" %surum
                elif self.Bilgi_Al() == "x86_64":
                    Adres = "https://download.mozilla.org/?product=firefox-%s-SSL&os=linux64&lang=tr" %surum
                self.print_("Bağlanılıyor %s" %Adres)
                self.saveTime = time.time()
                try:
                    urllib.urlretrieve(Adres, 'firefox.tar.gz', reporthook=self.report)
                except KeyboardInterrupt:
                    self.print_("Ctrl+C")
                    self.Cikis()
                print
                self.Olusturulan_Dosyalar.append(os.getcwd() + os.sep + 'firefox.tar.gz')
                self.print_("Dosya indirildi. İndirilen dosya çıkartılıyor... Bekleyin.")
                self.fileToExtract = "firefox.tar.gz"
                
            except:
                Soru = raw_input("\n\nBir hata meydana geldi! Sürümde hata olabilir.\nEn yeni sürüm kurulsun mu ? (e/h)")
                self.IFADELER.append("%s: Bir hata meydana geldi! Sürümde hata olabilir." %str(tarih.now()))
                YANITLAR = ["e", "evet"]
                if Soru.lower() in YANITLAR:
                    Adres = self.YeniSurumTespit()
                    self.Guncellestir(KayitDosyasi, KayitDurumu, "", Adres)
                else:
                    os.chdir(self.Kullanici_Dizini)
                    self.Cikis()
        elif fromFile == 1:
            self.print_("Dosya çıkartılıyor %s..." %surum)
            self.fileToExtract = self.surum
        
        Dosya = tarfile.open(self.fileToExtract)
        
        for name in Dosya.getnames():
            self.print_("Çıkartılıyor %s..." %name)
            self.Olusturulan_Dosyalar.append(os.getcwd() + os.sep + name)
            Dosya.extract(name)
        

        self.print_("Dosya çıkartıldı.")
        
        self.rescueFromFolder(os.path.join(os.getcwd(), "firefox"), 0)
        
        if surum == "":
            self.print_("Firefox en yeni sürüme yükseltildi." )
        else:
            self.print_("Firefox %s sürümüne yükseltildi." %surum)
            
        os.chdir(self.Kullanici_Dizini)
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
            KARISTIR = bs(Kodlar, "html.parser")
            Bul1 = KARISTIR.find('li', {"class" : "os_linux"})
            KARISTIR = bs(str(Bul1), "html.parser")
            Bul = KARISTIR.find('a', {"class" : "download-link"})
            SATIR = str(Bul).split('\n')[0]
        
            for i in SATIR.split(' '):
                if 'href=' in i:
                    Adres = i        
            Adres = Adres.replace('href=', '', 1)
            Adres = Adres.replace('>', '', -1)
            Adres = Adres[1: -1].replace('amp;', '')

            
            
            
            
        elif bit == "x86_64":
            Kodlar = urllib.urlopen('https://www.mozilla.org/tr/firefox/new/').read()
            KARISTIR = bs(Kodlar, "html.parser")
            Bul1 = KARISTIR.find('li', {"class" : "os_linux64"})
            KARISTIR = bs(str(Bul1), "html.parser")
            Bul = KARISTIR.find('a', {"class" : "download-link"})
            SATIR = str(Bul).split('\n')[0]
            
            for i in SATIR.split(' '):
                if 'href=' in i:
                    Adres = i
            
            Adres = Adres.replace('href=', '', 1)
            Adres = Adres.replace('>', '', -1)
            Adres = Adres[1: -1].replace('amp:', '')
            
        Adres = self.addFirstAddr(Adres)
        
        codes = urllib.urlopen(Adres).read()
        soup = bs(codes, "html.parser")
        find = soup.find('a', {"id" : "direct-download-link"})
        foundLine = str(find)
        
        address = re.findall('href="(.*?)"', foundLine)[0]
        address = self.addFirstAddr(address)
        
        codes = urllib.urlopen(address).read()
        soup = bs(codes, "html.parser")
        find = soup.find('tr', {"id" : "tr"})
        foundLine = str(find)
        
        
        if bit == "i686":
            searchWord = "os=linux&amp;"
        elif bit == "x86_64":
            searchWord = "os=linux64&amp;"
        
        #print foundLine
        
        addresses = re.findall('href="(.*?)"', foundLine)
        
        for i in addresses:
            if searchWord in i:
                address = i
                break
        
        """soup = bs(foundLine)
        find = soup.find('td', {"class" : searchWord})
        foundLine = str(find)
        
        
        address = re.findall('href="(.*?)"', foundLine)[0]"""
        address = self.addFirstAddr(address)
        
        
        return address
        
    def addFirstAddr(self, address):
        if not address.startswith("https://") and not address.startswith("http://"):
            if not address.startswith("https://www.mozilla.org") or address.startswith("/") or not address.startswith("https://mozilla.org") or not address.startswith("http://www.mozilla.org") or not address.startswith("http://mozilla.org"):
                    if address.startswith("/"):
                        address = "https://www.mozilla.org" + address
                    else:
                        address = "https://www.mozilla.org/" + address
        return address            
            
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
        

