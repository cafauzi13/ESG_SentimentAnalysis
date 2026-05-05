import pandas as pd
import time
import random
import csv
import re  # <-- TAMBAHAN: untuk ekstrak tanggal dari URL
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# ── 1. BACA EXCEL ─────────────────────────────────────────────────
df = pd.read_excel(
    r"C:\!KULIAH\PBA\Project multatuli\link multatuli.xlsx",
    sheet_name="Sheet1",
    header=2
)
links = df["Link"].dropna().unique().tolist()
print(f"Total link unik: {len(links)}")

# ── 2. SETUP BROWSER ──────────────────────────────────────────────
options = Options()
options.add_argument("--window-size=1920,1080")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option("useAutomationExtension", False)
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),
    options=options
)
driver.execute_cdp_cmd(
    "Page.addScriptToEvaluateOnNewDocument",
    {"source": "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"}
)

# ── 3. FUNGSI SCRAPE ──────────────────────────────────────────────
def scrape_artikel(url):
    try:
        driver.get(url)
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        time.sleep(15)

        # ── CEK CLOUDFLARE ─────────────────────────────────────────
        page_source = driver.page_source
        if "Performing security verification" in page_source or "Ray ID" in page_source:
            print(f"  ⚠️  Kena Cloudflare, tunggu 60 detik...")
            time.sleep(60)
            driver.refresh()
            time.sleep(20)
            page_source = driver.page_source

        if "Performing security verification" in page_source:
            print(f"  ❌ Masih kena Cloudflare, skip")
            return {
                "Link": url, "Sentiment": "", "Penerbit": "Project Multatuli", 
                "Tag": "", "Perusahaan": "", "Tahun": "", 
                "Isi Berita Clean": "CLOUDFLARE_BLOCKED"
            }

        # Scroll simulasi manusia
        driver.execute_script("window.scrollTo(0, 400);")
        time.sleep(2)
        driver.execute_script("window.scrollTo(0, 800);")
        time.sleep(2)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3)

        # ── AMBIL JUDUL ────────────────────────────────────────────
        judul = ""
        judul_selectors = [
            ".elementor-widget-theme-post-title h2",
            ".elementor-widget-theme-post-title h1",
            "h1.entry-title",
            "h2.entry-title",
            "h1",
            "h2",
        ]
        for sel in judul_selectors:
            try:
                el = driver.find_element(By.CSS_SELECTOR, sel)
                teks = el.text.strip()
                if len(teks) > 5:
                    judul = teks
                    break
            except:
                continue

        # ── AMBIL ISI ARTIKEL ─────────────────────────────────────
        isi = ""
        try:
            isi = driver.execute_script("""
                var el = document.querySelector('.elementor-widget-theme-post-content');
                return el ? el.innerText : '';
            """).strip()
        except:
            pass

        if len(isi) < 300:
            isi_selectors = [
                ".elementor-widget-theme-post-content",
                ".elementor-widget-text-editor",
                ".entry-content",
                ".post-content",
                "article",
            ]
            for sel in isi_selectors:
                try:
                    el = driver.find_element(By.CSS_SELECTOR, sel)
                    teks = el.text.strip()
                    if len(teks) > 300:
                        isi = teks
                        break
                except:
                    continue

        if len(isi) < 300:
            print(f"  ⚠️  Isi artikel tidak ditemukan")
            isi = "ISI_TIDAK_DITEMUKAN"

        # ── AMBIL TANGGAL (DIPAKSAKAN) ─────────────────────────────
        tanggal = ""
        
        # 1. Coba cari dari Meta Tags (Paling akurat)
        try:
            meta_date = driver.find_element(By.CSS_SELECTOR, "meta[property='article:published_time']")
            if meta_date:
                tanggal_raw = meta_date.get_attribute("content")
                if tanggal_raw:
                    tanggal = tanggal_raw.split("T")[0]  # Mengambil format YYYY-MM-DD
        except:
            pass

        # 2. Kalau Meta Tags gagal, coba selector HTML
        if not tanggal:
            tanggal_selectors = [
                ".elementor-post-info__item--type-date",
                "[itemprop='datePublished']",
                "time.entry-date",
                "time.published",
                "time",
                ".posted-on",
                "[class*='date']",
            ]
            for sel in tanggal_selectors:
                try:
                    el = driver.find_element(By.CSS_SELECTOR, sel)
                    teks = el.text.strip()
                    if teks:
                        tanggal = teks
                        break
                except:
                    continue

        # 3. Kalau masih gagal, paksakan tarik dari URL berita
        if not tanggal:
            match = re.search(r'/(\d{4})/(\d{2})/', url)
            if match:
                tanggal = f"{match.group(1)}-{match.group(2)}"

        print(f"  ✅ OK - {judul[:60]} | {len(isi)} karakter | Tanggal: {tanggal}")

        # --- Hapus Newline & Gabung Teks ---
        judul_bersih = judul.replace('\n', ' ').replace('\r', ' ')
        isi_bersih = isi.replace('\n', ' ').replace('\r', ' ')
        
        teks_final = f"{judul_bersih}. {isi_bersih}" if judul_bersih else isi_bersih

        return {
            "Link": url,
            "Sentiment": "",                
            "Penerbit": "Project Multatuli",  
            "Tag": "",                      
            "Perusahaan": "",               
            "Tahun": tanggal,               
            "Isi Berita Clean": teks_final  
        }

    except Exception as e:
        print(f"  ❌ GAGAL - {e}")
        return {
            "Link": url, "Sentiment": "", "Penerbit": "Project Multatuli", 
            "Tag": "", "Perusahaan": "", "Tahun": "", 
            "Isi Berita Clean": f"GAGAL: {e}"
        }

# ── 4. LOOP SEMUA LINK ────────────────────────────────────────────
hasil = []

for i, link in enumerate(links):
    print(f"\n[{i+1}/{len(links)}] {link}")
    hasil.append(scrape_artikel(link))

    if (i + 1) % 5 == 0:
        pd.DataFrame(hasil).to_csv(
            "raw_multatuli.csv",           
            index=False,                   
            encoding="utf-8-sig",
            quoting=csv.QUOTE_ALL          
        )
        print(f"  💾 Progress tersimpan ({i+1} artikel)")

    if (i + 1) % 10 == 0:
        istirahat = random.uniform(180, 300)
        print(f"  😴 Istirahat panjang {istirahat/60:.1f} menit...")
        time.sleep(istirahat)
    else:
        jeda = random.uniform(60, 90)
        print(f"  ⏳ Jeda {jeda:.0f} detik...")
        time.sleep(jeda)

# ── 5. SIMPAN HASIL FINAL ─────────────────────────────────────────
driver.quit()
pd.DataFrame(hasil).to_csv(
    "raw_multatuli.csv",               
    index=False,                       
    encoding="utf-8-sig",
    quoting=csv.QUOTE_ALL              
)
print(f"\n✅ SELESAI! Total: {len(hasil)} artikel")
print("📁 File tersimpan: raw_multatuli.csv")