# BINANCE TRADE ALARM - Proje kısa dökümantasyonu

Bu projede; Binance piyasasından coinlerin verilerini çekip, RSI indikatörüne göre AL ve ya SAT şeklinde mail gönderebileceğim.

_NOT_: Bu proje, çoğunlukla ChatGPT-4o kullanarak oluşturduğum bir projedir.

## 1 - Kütüphaneler:

Bu projede kullandığım kütüphaneler:

- **Pandas**: Verileri dataframe içinde tutmak için
- **Numpy**: Dataframe de çok boyutlu dizilerle çalışmak ve bazı matematiksel işlemleri kullanmak için
- **Time**: Mevcut zamanı almak için
- **DateTime**: Zaman dönüşümleri için
- **binance.clien**t: Binance istemcisi
- **smtplib**, **MIMEText**, **MIMEMultipart**: E-mail göndermek, e-mail içeriğini düzenlemek başta olmak üzere e-mail ile ilgili bir çok işlemleri gerçekleştirmek için


## 2 - İlk satırlar:

**df_hareketler** adında bir dataframe oluşturdum. **['Tarih', 'Coin', 'Fiyat', 'RSI değeri', 'Durum']** sütunlarına sahip bir dataframe oluşturdum. Ardından **read_csv** ile daha sonradan oluşturacağımız, verileri
üstüne yazacağımız bir 'csv' dosyasını geri çağırıyorum (Çağırma işlemini yapmadığım zaman projeyi her başlattığımızda csv dosyamız sıfırlanıyor.).

**API_KEY** ve **API_SECRET** isteğe bağlı olarak Binance hesabınızda oluşturduğunuz API keyleri doldurabilirsiniz (Eğer trade işlemlerini gerçekleştirecekseniz).


## 3 - E-mail gönderme fonksiyonu(send email):

- **_gonderen_**: maili gönderecek e-posta adresi
- **_sifre_**: maili gönderecek e-posta adresinin **UYGULAMA ŞİFRESİ**. Özellikle kalın ve büyük yazdım çünkü Google'dan göndereceğiniz e-mail şifresini girdiğiniz zaman hata veriyor. Burada göndereceğiniz
Google hesabınızdan uygulama şifresi almanız ve bu şifreyi projede kullanmanız gerekiyor.
- **_alici_**: Göndermek istediğiniz e-mail adresi. Çoklu e-mail adresleriniz varsa ['ornek1@gmail.com', 'ornek2@gmail.com'] şeklinde girebilirsiniz (Köşeli parantez ile yapınız.).

**send_email** fonksiyonunda konu başlığı, içerik, gönderen, şifre ve alıcı bilgileri ile e-posta göndermesini sağlıyorum.

_Ben burada Gmail adresleri kullanmaya çalıştım. Diğer mail adresleri de kullanılabilir mi bir bilgim yok. Ancak yahoo ve ya outlook örneklerine denk geldim._

## 4 - Calculate RSI:

RSI açılımı Relative Strength Index olan ve Türkçeye “Relatif Güç Endeksi” olarak çevrilen bir terimdir. Relatif güç endeksi bir varlığın son fiyat değişikliklerinin hızını ve büyüklüğünü ölçer. 

RSI, bu artan ve azalan günlerin ortalamaları arasındaki oranı kullanarak varlığın momentumunu ölçer. Yüksek RSI değerleri varlığın son fiyat değişikliklerinin hızlı ve büyük olduğunu, düşük değerler ise yavaş ve küçük olduğunu gösterir.

RSI değeri nedir sorusunu hesaplama üzerinden de açıklamak mümkün. RSI hesaplaması iki adımlı bir işlemdir. Aşamaları şöyle formüle edebiliriz:
 
**RSI birinci aşama = 100 − [100/ (1+ Ortalama kayıp) / Ortalama kazanç]**


Bu ilk formül, ortalama kazanç veya kaybı yüzdeye dönüştürür. Genellikle borsa fiyatının kayıp veya kazancını hesaplamak için 14 günlük bir süre kullanır.

**RSI ikinci aşama =100−[ 100/ 1+ ((Önceki Ortalama Kayıp×13) + Mevcut Kayıp)) /(Önceki Ortalama Kazanç×13) + Mevcut Kazanç]**


İkinci formül önceki piyasa fiyatını bugün bulunduğu noktaya yakınsarken önceki 14 günü hesaba katar. Böylelikle aralarındaki fark hesaplanmış olur. Sonuç olarak, iki adımı birleştiren basitleştirilmiş bir formül şöyledir:

**RSI = 100 – [100 / ( 1 + (Yukarı Doğru Fiyat Değişimi Ortalaması / Aşağı Doğru Fiyat Değişimi Ortalaması )) ]**

Bu fonksiyon bize RSI değerini döndürecektir. 

_NOT_ : Bu başlıktaki yazılar tamamen : _https://gedik.com/yatirimci-sozlugu/r/rsi-relative-stregth-index_ kaynağından alıntıdır ve olduğu kadar sadeleştirmeye çalıştım.


## 5 - Projenin ana kısmı: 

63. satırdan itibaren asıl yapmak istediğim noktaya gelmiş bulunmaktayım. 

**coins** listeme 'BTC', 'ETH', 'XRP', 'DOGE' gibi coinleri listeme aldım. Bu coinlerin RSI indikatör değerlerine göre **AL** ya da **SAT** şeklinde bize durum bildirecek ve buna göre bize 5 dakikada bir mail yollayacak.

**coins** listesi 'BTCUSDT' şeklinde yani yapmak istediğimiz coini hangi coin(XRP, ETH gibi) ve ya tether(USDT) ile yapacağımızı birleşik olarak belirtiyoruz. Bu örnekte Tether (USDT) ile Bitcoin (BTC) işlemlerini kapsar.

**rsi_treshold_buy**, RSI değeri 30 ve altında ise bize _AL_ şeklide uyarı vermemizi sağlayacaktır. **sell** ise _SAT_ 

Döngü içinde coinleri tek tek döndürecek, Binance istemcisinden (Client) coinlere ait 15 dakikalık sıklıkta bilgileri aldım ve döngü içinde bir dataframe'e aktardım. 

RSI hesaplamasını yazdığım fonksiyon ile hesapladım ve dataframe'e aktardım.

Yerel bir **fiyat** değişkeni açıp kapanış değerini aldım, **last_rsi** değişkeni RSI değerini alıyor. **current_time** son zamanı alıyor. 

**last_rsi** değeri **rsi_treshold_buy** değişkenine küçük ve ya eşit olduğunda (Yani 30 dan küçük ve ya eşitse): _Bize döngüde döndürdüğü coini almamız gereken maili gönderecek._

**last_rsi** değeri **rsi_treshold_sell** değişkenine büyük ve ya eşit olduğunda (Yani 70 dan büyük ve ya eşitse): _Bize döngüde döndürdüğü coini satmamız gereken maili gönderecek._

En son; proje çalıştığı sürece her 5 dakikada bir aldığı verileri csv dosyasına kaydedecek.



