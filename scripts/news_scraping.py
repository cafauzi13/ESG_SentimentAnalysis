import pandas as pd
import requests
from bs4 import BeautifulSoup
import time
import random
import re
import cloudscraper
import csv # Tambahkan library csv untuk kontrol quoting

print("Mulai membaca file CSV... 📂")

# 1. Baca data link
try:
    df = pd.read_csv('data_greenwashing_rapi.csv')
    url_berita = df['Link'].tolist()
except FileNotFoundError:
    print("❌ File 'data_greenwashing_rapi.csv' tidak ditemukan!")
    raise SystemExit

# 2. Hapus kolom nomor jika ada (Revisi 1A - Hapus Kolom Nomor)
if 'No' in df.columns:
    df = df.drop(columns=['No'])

# 3. Fungsi pembersih teks otomatis (Diperkuat)
def bersihkan_teks(teks):
    if not isinstance(teks, str):
        return ""
    
    # Revisi 1A - Fix Bug: Hapus newline dan carriage return secara agresif di awal
    teks = re.sub(r'[\n\r\t]', ' ', teks)
    
    teks = re.sub(r'http[s]?://\S+', '', teks)
    teks = re.sub(r'(?i)baca juga:.*?(?=\.|$)', '', teks)
    teks = re.sub(r'(?i)ilustrasi.*?(?=\.|$)', '', teks)
    teks = re.sub(r'(?i)foto:.*?(?=\.|$)', '', teks)
    teks = re.sub(r'(?i)sumber:.*?(?=\.|$)', '', teks)
    teks = re.sub(r'[^a-zA-Z0-9.,!?%()"\'-]', ' ', teks)
    
    # Normalisasi spasi berlebih
    teks = re.sub(r'\s+', ' ', teks)
    
    return teks.strip()

# ==========================================
# 4. PROSES SCRAPING MENGGUNAKAN CLOUDSCRAPER
# ==========================================
kumpulan_isi_berita_bersih = []

# Membuat sesi scraper
scraper = cloudscraper.create_scraper(browser={
    'browser': 'chrome',
    'platform': 'windows',
    'desktop': True
})

print(f"\n🚀 Mulai menyedot dan membersihkan teks dari {len(url_berita)} link...")

for i, url in enumerate(url_berita):
    url = str(url).strip()
    print(f"[{i+1}/{len(url_berita)}] Memproses: {url[:60]}...") 
    
    try:
        if not url.startswith('http'):
            kumpulan_isi_berita_bersih.append("GAGAL_AKSES: Format URL tidak valid.")
            continue
            
        response = scraper.get(url, timeout=15)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # STRATEGI 1: Cari teks di dalam tag <p>
            paragraf_html = soup.find_all('p')
            isi_berita = [p.get_text().strip() for p in paragraf_html if p.get_text().strip() != ""]
            full_text = " ".join(isi_berita)
            
            # STRATEGI 2: Jika tag <p> kosong atau teksnya sedikit
            if len(full_text) < 150:
                div_html = soup.find_all(['div', 'article'], class_=re.compile(r'detail|read|body|content|text', re.I))
                for div in div_html:
                    full_text += " " + div.get_text(separator=" ").strip()

            full_text = re.sub(r'\s+', ' ', full_text).strip()
            
            if len(full_text) < 100:
                 kumpulan_isi_berita_bersih.append("GAGAL_DIAMBIL: Teks terlalu pendek/JS Protected.")
            else:
                 teks_bersih = bersihkan_teks(full_text)
                 kumpulan_isi_berita_bersih.append(teks_bersih)
        else:
            kumpulan_isi_berita_bersih.append(f"GAGAL_AKSES: Error {response.status_code}")
            
    except Exception as e:
        kumpulan_isi_berita_bersih.append(f"ERROR_KONEKSI: {str(e)[:30]}")
        
    time.sleep(random.uniform(1.5, 4.0)) 

# 5. Gabungkan dan bersihkan DataFrame
df['Isi Berita Clean'] = kumpulan_isi_berita_bersih

# Filter data yang gagal
df = df[~df['Isi Berita Clean'].str.contains("GAGAL_DIAMBIL|GAGAL_AKSES|ERROR_KONEKSI", na=False)]

# Revisi 1A - Fix Bug (Ekstra pengaman): Pastikan tidak ada newline tersisa di seluruh kolom DataFrame
for col in df.columns:
    if df[col].dtype == 'object':
        df[col] = df[col].astype(str).str.replace('\n', ' ', regex=False).str.replace('\r', '', regex=False)

# 6. Ekspor (Revisi 1A: Ganti nama file dan gunakan quoting=csv.QUOTE_ALL)
nama_file_output = 'raw_data.csv'
df.to_csv(nama_file_output, index=False, encoding='utf-8', quoting=csv.QUOTE_ALL)

print(f"\n✅ MANTAP! Proses selesai. Data (raw_data.csv) sudah rapi, tanpa newline, dan siap di-push ke GitHub untuk Pipeline selanjutnya!")