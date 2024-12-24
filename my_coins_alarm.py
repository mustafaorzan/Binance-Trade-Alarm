import pandas as pd
import numpy as np
from binance.client import Client
from datetime import datetime
import time
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# AL - SAT için oluşturmak istediğim dataframe

df_hareketler = pd.DataFrame(columns=["Tarih","Coin", "Fiyat", "RSI", "Durum"])
df_hareketler = pd.read_csv('hareketler.csv') # Önceki verileri oku. 

# Binance API bilgileri
API_KEY = "your_api_key"
API_SECRET = "your_api_secret"


# Binance client
client = Client(API_KEY, API_SECRET)

# E-mail gönderme fonksiyonu
gonderen = "GÖNDEREN MAİL"
sifre = "UYGULAMA ŞİFRESİ (Google hesap ayarlarından bakınız.)"  # Uygulama şifresi kullanın!
alici = "ALICI MAİL"

def send_email(subject, body, sender, password, recipient):
    msg = MIMEMultipart()
    msg['From'] = sender
    msg['To'] = recipient
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender, password)
        text = msg.as_string()
        server.sendmail(sender, recipient, text)
        server.quit()
        print("E-posta başarıyla gönderildi.")
    except Exception as e:
        print(f"E-posta gönderilirken hata oluştu: {e}")


# RSI hesaplama fonksiyonu
def calculate_rsi(prices, window=14):
    deltas = prices.diff()
    gain = deltas.where(deltas > 0, 0)
    loss = -deltas.where(deltas < 0, 0)

    avg_gain = gain.rolling(window=window, min_periods=1).mean()
    avg_loss = loss.rolling(window=window, min_periods=1).mean()

    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))

    return rsi

# Coin listesi
coins = ["BTCUSDT", "ETHUSDT", "XRPUSDT", "DOGEUSDT", "BNBUSDT"]

# Al/Sat uyarısı
rsi_threshold_buy = 30
rsi_threshold_sell = 70

while True:
    email_body = ""
    for coin in coins:
        try:
            # Binance'den veri çekme
            klines = client.get_klines(symbol=coin, interval=Client.KLINE_INTERVAL_15MINUTE, limit=100)
            df = pd.DataFrame(klines, columns=["time", "open", "high", "low", "close", "volume", "close_time", "qav", "num_trades", "tbbav", "tbqav", "ignore"])
            df["close"] = df["close"].astype(float)

            # RSI hesaplama
            df["rsi"] = calculate_rsi(df["close"])

            # Fiyat Çekme
            fiyat = df['close'].iloc[-1]

            # Son RSI değeri ve durum
            last_rsi = df["rsi"].iloc[-1]
            current_time = datetime.now().strftime("%d.%m.%Y - %H:%M")

            if last_rsi <= rsi_threshold_buy:
                status = "AL"
                email_body += f"[Tarih: {current_time} \n Coin: {coin.upper()} \n Fiyat: {fiyat:.4f} \n Rsi: {last_rsi:.2f} \n Durum: {status}]\n"
                send_email(f"Mustafa Orzan - Coin Alarm {current_time}", email_body, gonderen, sifre, alici)
                
            elif last_rsi >= rsi_threshold_sell:
                status = "SAT"
                email_body += f"[Tarih: {current_time} \n Coin: {coin.upper()} \n Fiyat: {fiyat:.4f} \n Rsi: {last_rsi:.2f} \n Durum: {status}]\n"
                send_email(f"Mustafa Orzan - Coin Alarm {current_time}", email_body, gonderen, sifre, alici)
                
            else:
                status = "BEKLE"
                
            df_hareketler.loc[len(df_hareketler)] = [current_time, coin.upper(), np.round(fiyat, 4), np.round(last_rsi, 2), status]


            

        # Çıktı
            print(f"[Tarih: {current_time} | Coin: {coin.upper()} | Fiyat: {fiyat:.4f} | Rsi: {last_rsi:.2f} | Durum: {status}]")
        except Exception as e:
            print(f"{coin} için veri çekilirken hata oluştu: {e}")
    

    print("-----------------------------------\n")    
    print("5 dakika bekleniyor...\n")
    print("-----------------------------------\n")
    df_hareketler.to_csv('hareketler.csv',index=False)
    time.sleep(300)
