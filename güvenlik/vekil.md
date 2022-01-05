# Vekil üzerinden güvenli bağlantı

[TOC]



## 1. Giriş

Bilginin hızla yayıldığı ve küresel bilgisayar ağının özel veya mesleki hayatımızın odağına kaydığı bir zamanda, veri güvenliğimiz tehdit eden yapılarla her an karşı karşıya gelebileceğimizi göz önünde bulundurmalıyız. Ticari veya sosyal faaliyetlerimizin yanında, yüksek orantıda yasa dışı unsurlaru barındıran bir ortamdan bahsediyoruz. Özel verilerimizin güvenliğini sağlamayı amaçlarken, orta dereceli bilgi ve tecrübeye sahip kullanıcılara uygun pratik, ücretsiz ve taşınabilir bir çözüm üzerinde durmaya çalışacağım. Bunun ötesinde özel yaşam ve güvenlik hakkında biraz duyarlılık oluşturmayı önemsiyorum.



## 2. Hazırlık

Güvenli hat kullanmıyorsanız küresel bilgisayar ağında sandığınız kadar anonim olmayabilirsiniz. Hiç değilse sağlayıcılarınız, şartlara göre ağ yöneticileri veya gizli takipcileriniz veri trafiğinizi kolayca izleyebilir ve analiz için kaydedebilirler. Bu durum özellikle kamusal alanlarda (internet salonları, otel, yurt, ...) ve iş yerlerinde sıkıntı yaratabiliyor. Bu atölyede hedefimiz bağlantımızı bağımsız bir sunucu üzerinden yönlendirerek takibimizi zorlaştırmak ve iletişimi tamamen şifrelemek olacaktır.

Sunacağım metotla arkasında bulunduğumuz güvenlik duvarının ayarlarına müdahale etmeden, engellenen hizmetlere arka kapı açmak da mümkündür. Güvenlik duvarları veri akışını denetleyen ve çeşitli filtrelerden oluşan yazılımlardır/donanımlar dır. Faal oldukları ortamlarda uygulanan kısıtlamaların yanında mutlaka açık portlarda bulundurmaktadırlar. Örneğimde kullanacağım portları (22: SSH, 7561: Tanımlanmamış) kendi ihtiyaçlarınız doğrultusunda değiştirebilir ve açık port arayışında nmap gibi port tarayıcılarından faydalanabilirsiniz.

Atölyemizde, resimlendireceğim sistemin çekirdeğini yönlendirme ve şifrelemeyi üzerinden yapacağımız SSH sunucusu oluşturacaktır. Bunun bilincinde olmamız önemlidir. Deneme aşamasında ücretsiz bir sunucuyla başlayacağız, fakat e-posta, çevrimiçi alışveriş veya bankacılık gibi hassas hizmetleri ücretsiz bir sunucu üzerinden kullanmamanızı ve ileri aşamalarda fiyatları 5\$ - 10\$ arasında değişen gizlilik ilkelerine sahip profesyonel hizmetlere geçmenizi öneriyorum. Alternatif olarak ev veya ofislerinizde kendi SSH sunucularınızı kurabilir, güvensiz ortamlarda iletişiminizi onların üzerinden yönlendirebilirsiniz.

#### 2.1. Araç ve gereçler

##### 2.1.1. SSH sunucusu

​	Önerilen: [xshellz](https://www.xshellz.com)
​		:heavy_check_mark: SSH ve port yönlendirme
​		:heavy_check_mark: Ücretsiz hizmet planı
​		:heavy_check_mark: Hızlı üyelik
​		:x: Şeffaf gizlilik ilkesi (burada sadece deneme amaçlı kullanacağız)
Detay: [Üyelik](https://www.xshellz.com/signup) / [Yönetim paneli](https://www.xshellz.com/xpanel/create) / [Kullanım şartları](https://www.xshellz.com/terms-of-service) / [Hizmet planları](https://www.xshellz.com/pricing)

##### 2.1.2. SSH alıcısı

​	Önerilen: OpenSSH
​		:heavy_check_mark: Port yönledirme ve güvenli tünel oluşturma
​		:heavy_check_mark: Taşınabilir, ücretsiz ve açık kaynaklı
​		:heavy_check_mark: Komut satırı
​		:heavy_check_mark: Yüksek uyarlama kapasitesi
​		:heavy_check_mark: İz bırakmadan kaldırılabilir
​	Detay: [Kullanım kılavuzu](https://www.openssh.com/manual.html)
​	İndir: [v8.6.0.0 (x86)](https://github.com/PowerShell/Win32-OpenSSH/releases/download/V8.6.0.0p1-Beta/OpenSSH-Win32.zip) / [v8.6.0.0 (x64)](https://github.com/PowerShell/Win32-OpenSSH/releases/download/V8.6.0.0p1-Beta/OpenSSH-Win64.zip)

##### 2.1.3. Web tarayıcısı

​	Önerilen: Mozilla Firefox Portable
​		:heavy_check_mark: Güvenli tünel kullanma kabiliyeti
​		:heavy_check_mark: Taşınabilir, ücretsiz ve açık kaynaklı
​		:heavy_check_mark: Komut satırı
​		:heavy_check_mark: Yüksek uyarlama kapasitesi
​		:heavy_check_mark: İz bırakmadan kaldırılabilir
​	Detay: [Kullanım kılavuzu](https://support.mozilla.org/tr/products/firefox)
​	İndir: [v95.0.2 (x86/x64)](https://sourceforge.net/projects/portableapps/files/Mozilla%20Firefox%2C%20Portable%20Ed./Mozilla%20Firefox%2C%20Portable%20Edition%2095.0.2/FirefoxPortable_95.0.2_Turkish.paf.exe/download)

#### 2.2. Önbakış

1. SSH hesabı oluşturacağız.
2. SSH alıcısıyla sunucumuza bağlanacağız.
3. Taşınabilir tarayıcımızı SSH tünelini kullanacak şekilde uyarlayacağız.
4. Gizliliğin tadını çıkaracağız.



## 3. Uygulama

Çalışmamın ilk şeklinde PuTTY ile SSH oturumu oluşturmayı öngörüyordum. Fakat sistemin veritabanını kullanmadan komut satırında bağlantının kopmasını engelleyen `keepalive` değerini kabul etmediği için başka çözüm arayışlarına girmek zorunda kaldım. Aslında iyi de oldu. Linux dünyasından bilinen OpenSSH ile çok daha güçlü bir alıcı/sunucuya sahip olacağımızı kısa sürede farkedeceksiniz. Buna rağmen PuTTY'yi denemek isteyenler gereken bilgileri ek bölümünde bulabilirler.

#### 3.1. SSH sunucusu üyeliği

- *<u>2.1.3. Web tarayıcısı</u>* bölümünden taşınabilir Firefox'u indiriyor ve `FirefoxPortable_95.0.2_Turkish.paf.exe` üzerinden dökümü başlatıyoruz.
- Karşılama ekranında <kbd>İleri</kbd> ile devam ediyoruz.
- Hedef dizininde öngörülen yolu devralıyor veya dökülmesini istediğimiz yere işaret edecek şekilde <kbd>Gözat...</kbd> üzerinden düzenliyoruz (örn. Masaüstü).
- <kbd>Kur</kbd> ile dökümü başlatıyor ve tamamlandıktan sonra <kbd>Bitir</kbd> üzerinden kapatıyoruz.
- Windows gezginiyle taşınabilir tarayıcıyı döktüğümüz dizine gidiyor ve `FireFoxPortable.exe` ile çalıştırıyoruz.
- *<u>2.1.1. SSH sunucusu</u>* bölümünden *<u>Üyelik</u>* bağlantısını kopyalıyor, FireFox Portable adres çubuğuna yapıştırıp, onaylıyoruz.
- Açılan formu doldurup, captcha'yı tamamlıyor ve <kbd>Create Account</kbd> butonuyla ilerliyoruz.
	
	[^Username]:Panele giriş için kullanıcı adı
	[^Email]:Doğrulama için kullanılacak eposta adresiniz
	[^Password]:Panele giriş şifresi

- Kayıt oluşturduktan kısa süre sonra epostamıza xshellz tarafından ileti gönderilecektir. İçindeki doğrulama bağlantısını kopyalıyor ve Firefox Portable araç çubuğuna yapıştırarak açıyoruz. Üyeliğimiz aktif duruma geçecektir.
- *<u>2.1.1. SSH sunucusu</u>* bölümünden *<u>Yönetim paneli</u>* bağlantısını kopyalıyor, FireFox Portable adres çubuğuna yapıştırıp ve açıyoruz.
- Üyelik esnasında tanımladığımız kullanıcıyı ve şifreyi giriyor ve <kbd>Login to xShellz</kbd> ile onaylıyoruz.
- Üst menüden <kbd>>_ xPanel</kbd> bölümüne giriyoruz, <kbd>+ Create Shell</kbd> üzerinden oturum sağlayıcısı oluşturuyoruz.
- Ücretsiz planda sadece tek lokasyon seçeneği mevcuttur. <kbd>USA</kbd> lokasyonunu seçip, <kbd>Create</kbd> ile devralıyoruz.
- Son ekranda bağlantı için gereken bilgiler sıralanacaktır.

	[^Hostname]:shell.xshellz.com (sunucu adresi)
	[^Port]:22 (SSH hizmeti portu)
	[^Username]:Kullanıcı adınız
	[^Set SSH Password]:Burada SSH hizmeti için farklı bir şifre tanımlayın ve <kbd>Set shell password</kbd> butonuyla onaylayın. Şifreniz en az 8 karakterden oluşmalı ve bir özel karakter içermelidir
	[^Shell Locatıon]:Oturum sağlayıcısı lokasyonu

#### 3.2. Dinamik port yönlendirme ve SSH oturumu açma

- *<u>2.1.2. SSH alıcısı</u>* bölümünden OpenSSH'yı indiriyor ve arşivi bulabileceğimiz bir yere döküyoruz (örn. Masaüstü).
- Windows gezginiyle döktüğümüz OpenSSH klasörüne giriyoruz. İçinde birçok dosyalar barındırdığını göreceğiz. Burada `oturum.bat` isminde yeni bir toplu işlem dosyası oluşturuyor ve sıradaki üç komut satırlarını içine kaydediyoruz. Sunucunun tam ismini veya IP adresini <span style="color:red">sunucu</span>, kullanıcı adını da <span style="color:red">kullanıcı</span> şeklinde belirtilen yerlerle değiştirmeyi ihmal etmiyoruz. İleride SSH oturumunu toplu işlem dosyasını çalıştırarak kolaylıkla gerçekleştireceğiz. 

```bash
@ECHO OFF
set HOME=%cd%
"%HOME%\ssh.exe" -2 -P22 sunucu -D7561 -l kullanıcı -o ServerAliveInterval=60 -o ServerAliveCountMax=120
```

|                                                        Komut | Açıklama                                                     |
| -----------------------------------------------------------: | ------------------------------------------------------------ |
| <span style="color:green">@</span><span style="color:blue">ECHO OFF</span> | Komut satırını yazdırmaz (çıktıyı gizler)                    |
| <span style="color:green">set</span> <span style="color:blue">HOME</span>=%cd% | OpenSSH klasörüne işaret eden ortam değişkeni                |
|            <span style="color:green">"%HOME%\ssh.exe"</span> | SSH alıcısının yolu                                          |
|                                                           -2 | Daha güvenli olan SSH-2 protokolünü zorunlu kılma            |
|                         -P<span style="color:blue">22</span> | Port takdimi ve güvenli tünelin hedef portu (22)             |
|                        <span style="color:red">sunucu</span> | SSH sunucusu (yerine SSH sunucunuzun tam adını veya IP adresini girin, örneğimizde: shell.xshellz.com) |
|                       -D<span style="color:blue">7561</span> | Dinamik port takdimi ve güvenli tünelin kaynak portu (7561)  |
|                                                           -l | Kullanıcı takdimi                                            |
|                     <span style="color:red">kullanıcı</span> | Kullanıcı adı (yerine SSH sunucunuzda kayıtlı üye/kullanıcı adınızı dirin) |
|    -o ServerAliveInterval=<span style="color:blue">60</span> | Pasif durumlarda bağlantının kesilmesini engelleyen, her 60 saniyede sunucuya sinyal atan komut satırı tercihi |
|   -o ServerAliveCountMax=<span style="color:blue">120</span> | Sunucuya gönderilen sinyalleri azami 120 adete sınırlayan komut satırı tercihi. Buna göre bağlantımız pasif durumlarda 120 x 60 saniye = 2 saat kesilmeyecektir. |

- `oturum.bat` dosyasını oluşturduktan sonra üzerine sol tuşla çift tıklayarak çalıştırıyoruz.
- Herşeyi doğru yaptıysak Windows komut ekranı açılacaktır ve SSH oturumu için şifre girmemizi isteyecektir. *<u>3.1. SSH sunucusu üyeliği</u>* bölümünde *<u>Set SSH Password</u>* kısmında tanımladığımız şifreyi girmemiz ve enter tuşuyla onaylamamız gerekmektedir.
- Şifremiz kabul edildiği takdirde böyle bir ekranla karşılanacağız:

```
Linux xshellz-free 4.9.0-17-amd64 #1 SMP Debian 4.9.290-1 (2021-12-12) x86_64
Welcome back to xShellz Free Server.

                           _//_\\
                         ,"    //".
                        /          \
                      _/           |
                     (.-,--.       |
    Hmmmm,           /o/  o \     /
     Interlicious    \_\    /  /\/\
             \       (__`--'   ._)
                     /  `-.     |
                    (     ,`-.  |
                     `-,--\_  ) |-.

Users of the Rizon IRC Network: Please connect to the sli.rizon.net server using the shell.xshellz.com vhost.
Use xshellzhelp to list all available commands.
Thanks for using xShellz Shell Services.
Start with typing: xshellzhelp
```

- Bu ekranı aktif kullanmayacağımız için küçültebilir veya arka tarafa atabiliriz (kapatmayın).

> **Dikkat**: Oturumunuzu bitirmek için **logout** komutunu kullanmalısınız. Aksi takdirde SSH sunucunuzda kullanıcı hesabınız faaliyetde kalabilir ve aynı gün içinde tekrar bağlanmanız mümkün olmayabilir!

#### 3.3. Güvenli tünel kullanımı

- Taşınabilir Firefox penceresini ön plana alıyor veya Windows gezginiyle taşınır tarayıcıyı döktüğünüz dizine gidip, `FireFoxPortable.exe` üzerinden çalıştırıyoruz.

- Üst sağda bulunan menü sembolünü <kbd>&#9776;</kbd> açıyor ve <kbd>Ayarlar</kbd> seçeneğine tıklıyoruz.

- Ekranı alta kaydırarak *<u>Ağ ayarları</u>* kısmından <kbd>Ayarlar...</kbd> seçiyor ve *<u>Bağlantı ayarlarını</u>* şu şekilde düzenliyoruz:

	Vekil sunucuyu elle ayarla: <span style="color:blue">etkin</span>
	SOCKS sunucusu: <span style="color:blue">127.0.0.1</span>	Port: <span style="color:blue">7561</span>
	SOCKS v5: <span style="color:blue">etkin</span>

- Değişiklikleri <kbd>Tamam</kbd> ile devralıp, ayarlar ekranını kapatıyoruz.

Web tarayıcımız güvenli tüneli kullanabilir hale gelmiştir. Gerektiğinde OpenSSH klasörü içinde oluşturduğumuz `oturum.bat` dosyasını çalıştırarak ve FireFox Portable'nin konum çubuğuna herhangi bir adres girerek, tünel içinde hareket edebiliyoruz.

Kendinize "Ayarlarım doğru mu, gerçekten tarayıcım tüneli kullanıyormu?" diye soruyorsanız, hemen sağlamasını yapabiliriz. Windows 10 sistemlerinde standart olan Microsoft Edge tarayıcısını çalıştırıyoruz ve [ip-adress.com](https://www.ip-adress.com) sayfasını ziyaret ediyoruz. Bizi bulunduğumuz yerde veya yakın bir lokasyonda gösterecektir. Aynısını uyarladığımız FireFox Portable ile yaptığımızda, bulunduğumuz yerden farklı bir lokasyon (muhtemelen ABD veya Kanada) gösteriyorsa, yönlendirme başarıyla gerçekleşmiştir.



## 4. Denetleme

Burada çevrimiçi etkinliklerimizin üçüncü şahıslar tarafından tanımlanabilir/takip edilebilirliğini denetleyeceğiz. OpenSSH oturumunu başlatıp, FireFox Portable ile herhangi bir site (örn. [iletisim.gov.tr](https://www.iletisim.gov.tr)) ziyaret eder ve oluşan trafiği Wireshark ağ analizi yazılımıyla incelersek, şöyle bir sonuçla karşılaşırız (çıktıdan alıntıdır):

| No.  | Time     | Source   | Destination | Protocol | Length | Info                                                         |
| ---- | -------- | -------- | ----------- | -------- | ------ | ------------------------------------------------------------ |
| 27   | 3.393270 | CLIENTIP | ROUTERIP    | DNS      | 79     | Standard query 0x29b4 AAAA <mark>www.iletisim.gov.tr</mark>  |
| 28   | 3.438179 | ROUTERIP | CLIENTIP    | DNS      | 129    | Standard query response 0x29b4 AAAA <mark>www.iletisim.gov.tr</mark> SOA press.iletisim.gov.tr |
| 29   | 3.466589 | SERVERIP | CLIENTIP    | TCP      | 54     | 22 → 50270 [ACK] Seq=1 Ack=101 Win=508 Len=0                 |
| 30   | 3.466589 | SERVERIP | CLIENTIP    | TCP      | 54     | 22 → 50270 [ACK] Seq=1 Ack=201 Win=508 Len=0                 |
| 31   | 3.602340 | SERVERIP | CLIENTIP    | SSH      | 98     | Server: Encrypted packet (len=44)                            |
| 32   | 3.602340 | SERVERIP | CLIENTIP    | SSH      | 98     | Server: Encrypted packet (len=44)                            |
| 33   | 3.602444 | CLIENTIP | SERVERIP    | TCP      | 54     | 50270 → 22 [ACK] Seq=201 Ack=89 Win=508 Len=0                |
| 34   | 3.609604 | CLIENTIP | SERVERIP    | SSH      | 610    | Client: Encrypted packet (len=556)                           |
| 35   | 3.616761 | CLIENTIP | SERVERIP    | SSH      | 610    | Client: Encrypted packet (len=556)                           |

Rapordan anlaşılacağı gibi iletişimin şifrelenmiş paketler halinde seyretmesine rağmen, www.iletisim.gov.tr gibi DNS sorgulamaları açık gerçekleşmekte ve etkinliklerimiz hakkında üçüncü şahıslara ipuçları vermektedirler (2. ve 3. satır). Bu sistemin zaafı değil, tarayıcının standart, fakat değiştirilmesi gereken davranışıdır. Ayrıca kullanıcı profilleri oluşturan ve sayfalarda reklamları şekillendiren Google AdSense gibi hizmetlerin engellenmesinde fayda görüyorum.

#### 4.1. İsim alanı sorgulaması

İsim alanı sorgulamasının devredilmesi için sıradaki iki seçenekten sadece birini uygulamalıyız. Birinci yöntemle sorgulamayı kalıcı devrederken, vekil yöneticisiyle alan sorgulamasını ihtiyaca göre açıp, kapatabilir, birden çok vekile devredebilir ve aralarında hızlıca geçiş yapabiliriz. İkinci yöntem olan vekil yöneticisini tavsiye edebilirim.

##### A) Sabit yöntem

FireFox Portable uygulamasını çalıştırıyoruz, konum çubuğuna `about:config` yazıyor ve onaylıyoruz. Hemen akabinde açılan uyarıyı <kbd>Riski kabul ederek devam et</kbd> butonuna tıklayarak kapatıyoruz. <kbd>Tümünü göster</kbd> butonuyla ayarları açığa çıkardıktan sonra alfabeye göre sıralanan listeden `network.proxy.socks_remote_dns` ayarını buluyor ve üzerine iki defa sol tuşla tıklayarak değerini `false`den `true`ya çeviriyoruz.

##### B) Vekil yöneticisi

​	Önerilen: FoxyProxy
​		:heavy_check_mark: Taşınabilir, ücretsiz ve açık kaynaklı
​		:heavy_check_mark: Yüksek uyarlama kapasitesi
​		:heavy_check_mark: Birden çok ağ ayarı desteği
​	Detay: [Hakkında](https://addons.mozilla.org/tr/firefox/addon/foxyproxy-standard/)
​	İndir: [v7.5.1](https://addons.mozilla.org/firefox/downloads/file/3616824/foxyproxy_standard-7.5.1-an+fx.xpi)

Üsteki indir bağlantısını kopyalıyoruz, FireFox Portable'nin adres çubuğuna yapıştırıp onaylıyoruz ve FoxyProxy eklentisinin kurulmasını sağlıyoruz.

- FireFox Portable'nin sağ üst köşesinde FoxyProxy simgesi belirecektir. Üzerine tıklıyor ve açılan menüden <kbd>Options</kbd> seçiyoruz.

- Açılan ekranda sol üst köşede <kbd>+ Add</kbd> butonuyla yeni vekil tanımlıyoruz ve ayarlarını şu şekilde yapıyoruz:

	Title or Description: <span style="color:blue">SSH Oturumu</span>

	Proxy Type: <span style="color:blue">SOCKS5</span>

	Proxy IP address or DNS name: <span style="color:blue">127.0.0.1</span>

	Port: <span style="color:blue">7561</span>

- <kbd>Save</kbd> butonuyla ayarlarımızı kaydediyoruz.

- <kbd>Edit</kbd> ile vekil kaydımızı tekrar açıyoruz ve `Send DNS through SOCKS5 proxy` değerinin aktif, yani <kbd>On</kbd> olduğuna emin oluyoruz. Bu ayar isim alanı sorgulamasının SSH oturumu üzerinden yapılmasını sağlayacaktır. Tamamsa, ekranı <kbd>Save</kbd> ile kapatıyoruz.

Böylece FoxyProxy eklentisiyle <span style="color:blue">SSH Oturumu</span> isimli vekil profili oluşturmuş olduk. Profil seçimini FireFox Portable'nin sağ üst köşesinde bulunan FoxyProxy'nin simgesi üzerinden <span style="color:green">SSH Oturumu</span> ibaresini seçerek yapabiliyoruz. Yönlendirmeyi kapatmak ve tarayıcıyı normal kullanmak için <span style="color:red">Turn Off (Use FireFox Settings)</span> ibaresini seçmemiz yeterli olacaktır. Her seçimde FoxyProxy simgesinin değiştiğini farkedeceksiniz.

#### 4.2. Gömülü reklamların engellenmesi

​	Önerilen: Adblock Plus
​		:heavy_check_mark: Taşınabilir, ücretsiz ve açık kaynaklı
​		:heavy_check_mark: Yüksek uyarlama kapasitesi
​		:heavy_check_mark: Geniş kapsamlı listeler (abonelikler)
​	Detay: [Hakkında](https://addons.mozilla.org/tr/firefox/addon/adblock-plus/)
​	İndir: [v3.11.4](https://addons.mozilla.org/firefox/downloads/file/3872123/adblock_plus-3.11.4-an+fx.xpi)

Üsteki indir bağlantısını kopyalıyoruz, FireFox Portable'nin adres çubuğuna yapıştırıp onaylıyoruz ve Adblock Plus eklentisinin kurulmasını sağlıyoruz.

- FireFox Portable'nin sağ üst köşesinde Adblock Plus simgesi belirecektir. Üzerine tıklıyor ve açılan menüden <kbd>&#9881;</kbd> (dişli çark) seçiyoruz.
- Açılan ekranı alta kaydırıp Dil bölümünde <kbd>Değiştir</kbd> butonuna tıklıyoruz ve karşımıza çıkan listeden bir abonelik seçiyoruz. <span style="color:blue">Deutsch + İngilizce</span> aboneliğiyle iyi tecrübeler edindim ve tavsiye olarak burada öne çıkarabilirim. Yinede farklı abonelikleri denemekte serbestiz. Dilediğimizde aboneliğimizi iptal edip, başka listeler kullanabilir, mevcutları genişletebilir veya sıfırdan yenilerini oluşturabiliriz.
- Ziyaret ettiğimiz siteleri desteklemek istemiyor ve iyi niyetliler dahil her türlü reklamları engellemek istiyorsak, <span style="color:blue">Kabul edilebilir reklamlara izin ver</span> ibaresinin yanındaki kutucuktan işareti kaldırabiliyoruz.
- Adblock Plus ile ilgili ayarlar otomatik kaydediliyor, <span style="color:blue">Adblock Plus Seçenekleri</span> sekmesini kapatabiliriz.

**Tebrikler, işlemlerimizi böylece tamamlamış olduk**. Firefox Portable ve OpenSSH klasörlerini USB belleğe kopyalabilir ve otel, yurt, havalimanı gibi güvensiz ortamlarda applikasyonlarımızı çalıştırıp, iletişimi takip edilmeyecek şekilde gerçekleştirebiliriz.



## 5. Ek bölüm

#### 5.1. SSH alıcısı (alternatif)

​	Önerilen: PuTTY
​		:heavy_check_mark: Port yönledirme ve güvenli tünel oluşturma
​		:heavy_check_mark: Taşınabilir, ücretsiz ve açık kaynaklı
​		:heavy_check_mark: Komut satırı
​		:heavy_check_mark: Yüksek uyarlama kapasitesi
​		:x: İz bırakmadan kaldırılabilir
​	Detay: [Kullanım kılavuzu](https://documentation.help/PuTTY/)
​	İndir: [v0.76 (x86)](https://the.earth.li/~sgtatham/putty/latest/w32/putty.zip) / [v0.76 (x64)](https://the.earth.li/~sgtatham/putty/latest/w64/putty.zip)

PuTTY, arayüz üzerinden yapılan ayarları işletim sisteminin veritabanına kaydetmektedir (`HKEY_CURRENT_USER\Software\SimonTatham`). Taşınabilirlik ve veri güvenliğimiz için alıcımızı arayüz kullanmadan toplu işlem dosyası üzerinden çalıştırıp, verileri parametreler halinde bildirebiliriz. Sıradaki iki komut satırını kopyalayıp, PuTTY'nin bulunduğu klasörde oluşturacağımız toplu işlem dosyasına yapıştırıyoruz (örn. C:\Putty\oturum.bat). Sunucumuzun tam ismini veya IP adresini <span style="color:red">sunucu</span>, kullanıcı adımızı da <span style="color:red">kullanıcı</span> şeklinde belirtilen yerlerle değiştirmeyi unutmuyoruz.

```bash
@ECHO OFF
putty.exe -ssh -2 -P 22 -D 7561 sunucu -l kullanıcı
```

|                                                        Komut | Açıklama                                                     |
| -----------------------------------------------------------: | ------------------------------------------------------------ |
| <span style="color:green">@</span><span style="color:blue">ECHO OFF</span> | Komut satırını yazdırmaz (çıktıyı gizler)                    |
|                   <span style="color:green">putty.exe</span> | SSH alıcısının yolu                                          |
|                                                         -ssh | Erişim protokolü                                             |
|                                                           -2 | Daha güvenli olan SSH-2 protokolünü zorunlu kılma            |
|                        -P <span style="color:blue">22</span> | Port takdimi ve güvenli tünelin hedef portu (22)             |
|                      -D <span style="color:blue">7561</span> | Dinamik port takdimi ve güvenli tünelin kaynak portu (7561)  |
|                        <span style="color:red">sunucu</span> | SSH sunucusu (yerine SSH sunucunuzun tam adını veya IP adresini girin, örneğimizde: shell.xshellz.com) |
|                                                           -l | Kullanıcı takdimi                                            |
|                     <span style="color:red">kullanıcı</span> | Kullanıcı adı (yerine SSH sunucunuzda kayıtlı üye/kullanıcı adınızı dirin) |

#### 5.2. Kaynak

[Shells](https://shells.red-pill.eu/)
[Proxy Firefox through a SSH tunnel](https://calomel.org/firefox_ssh_proxy.html)
[Firefox: Useragent](http://kb.mozillazine.org/General.useragent.locale)
[Firefox: Remote DNS](http://kb.mozillazine.org/Network.proxy.socks_remote_dns)
[SOCKS5: DNS lookups](https://bugzilla.mozilla.org/show_bug.cgi?id=134105)
[PuTTY User Manual](http://the.earth.li/~sgtatham/putty/0.63/htmldoc/index.html)
[GNU Genel Kamu Lisansı (GPL) Nedir?](https://www.tech-worm.com/gnu-genel-kamu-lisansi-gpl-nedir/)

#### 5.3. Yasal uyarı

Yazılarımı imkanlarım dahilinde titizlikle oluşturuyorum ve bilgi ve tecrübelerimi paylaşırken mümkün oldukca güvenilir kaynaklardan faydalanmaya çalışıyorum. Yasal sorunlarla karşılaşmamak için yazılarımın bütünlüğü, geçerliliği ve güncelliği hakkında mesuliyet kabul etmiyorum. Yanlış kullanımdan dolayı oluşan zararlardan sorumlu değilim. Referans içeriklerin sorumlulukları sahiplerine aittir. Kaynak olarak gösterdiğim anda yasal veya ahlaki sakıncalar bulundurmuyorlardı. İleride içeriklerde veya hizmetlerde olabilecek değişikliklerden sorumlu değilim.

Çalışmalarımın tüm içerikleri, metin, grafik, logo ve yazılım kodları; dış görünüm ve teknik unsurlar, sayfanın toplama, düzenleme ve içerik derlemenin tamamı, her türlü haklar dahil olmak üzere bana aittir ve GPLv3 şartları altında yayınlanmaktadır. Bu unsurları kısmen veya tamamen, doğrudan veya dolaylı olarak aynen veya değiştirilmiş şekliyle kullanımı, alıntılanması, iktibası, çoğaltılması, işlenmesi, depolanması, başka bilgisayara yüklenmesi, dağıtımı, nakli, tekrar yayınlanması, teşhiri, uyarlanması, temsili, kişisel veya ticari amaçla elde bulundurulması, satılması veya yukarıda sayılan fiilerin teşvik edilmesi, yapılmasının kolaylaştırılması haklarımı koruyarak mümkündür.

[GNU Genel Kamu Lisansı](http://www.gnu.org/licenses/gpl-3.0.tr.html)
[GNU General Public License v3.0](https://choosealicense.com/licenses/gpl-3.0/)
