# 🌿 Analisis Sentimen Pemberitaan ESG untuk Deteksi Indikasi Greenwashing pada Perusahaan Indonesia Berbasis Natural Language Processing

> Tugas Akhir — Pengolahan Bahasa Alami (A)  
> Departemen Sistem Informasi, Fakultas Teknologi Elektro dan Informatika Cerdas  
> Institut Teknologi Sepuluh Nopember — Semester Genap 2026

---

## 👥 Tim Peneliti

| Nama | NRP |
|------|-----|
| Annisa Nur Fauzi | 5026231228 |
| Harya Raditya Handoyo | 5026231176 |
| Muhammad Raihan Hassan | 5026231108 |
| Nabila Shinta Luthfia | 5026231038 |
| Realasa Femmi Novelika | 5026231113 |

---

## 📌 Deskripsi Penelitian

Penelitian ini membangun pipeline Natural Language Processing (NLP) untuk menganalisis sentimen pemberitaan ESG (Environmental, Social, and Governance) dari portal berita daring Indonesia, dengan tujuan mendeteksi indikasi greenwashing pada perusahaan-perusahaan Indonesia.

Berbeda dari laporan keberlanjutan yang bersifat *self-reported*, artikel berita memuat narasi independen dari jurnalis, pakar, dan kelompok sipil yang secara aktif memverifikasi klaim perusahaan. Pendekatan ini menghasilkan bukti linguistik yang lebih objektif dibandingkan analisis laporan korporasi semata.

### Rumusan Masalah
1. Bagaimana tren pemberitaan ESG perusahaan Indonesia ditinjau dari sumber portal berita, kategori isu, dan distribusi sentimen?
2. Apa kata, frasa, dan terminologi ESG paling dominan berdasarkan analisis TF-IDF dan N-gram?
3. Bagaimana tingkat keselarasan pelabelan sentimen manual dengan validasi otomatis InSet Lexicon dan TextBlob?
4. Bagaimana POS tagging dan NER dapat mengungkap pola linguistik dan pemetaan entitas sebagai indikator greenwashing?

---

## 🗂️ Struktur Repository

```
ESG_SentimentAnalysis/
│
├── data/
│   ├── raw_data.csv               # Dataset link artikel mentah (portal umum)
│   ├── raw_multatuli.csv          # Dataset link artikel Project Multatuli
│   ├── clean_data.csv             # Output setelah preprocessing (468 artikel)
│   ├── test_set_asli.csv          # Test set murni (20%, tidak diaugmentasi)
│   └── train_set_augmented.csv    # Train set setelah augmentasi Gemini API
│
├── notebooks/
│   ├── cleaner_berita.ipynb       # Pipeline A: Preprocessing & ekstraksi tanggal
│   ├── EDA_FeatExt_NER.ipynb      # Pipeline B: EDA, sentimen leksikon, TF-IDF, POS, NER
│   └── klasifikasi.ipynb          # Pipeline C: Augmentasi & fine-tuning IndoBERT
│
├── output/
│   ├── wordcloud_comparison.png
│   ├── top20_kata.png
│   ├── timeline_sentimen_bulanan.png
│   ├── timeline_sentimen_kuartal.png
│   ├── timeline_anomali.png
│   ├── pos_distribusi.png
│   ├── pos_top_kata.png
│   ├── pos_heatmap.png
│   ├── ner_org_loc_indobert.png
│   ├── ner_org_per_tag.png
│   └── output_NER_Lengkap_ORG_LOC_GPE.png
│
└── README.md
```

---

## 🔄 Alur Pipeline

```
Manual Crawling (568 link)
        ↓
Web Scraping (488 artikel berhasil)
        ↓
Filter Token Minimum 50 (468 artikel final)
        ↓
┌─────────────────────────────────────┐
│     cleaner_berita.ipynb            │
│  Ekstraksi Tanggal → Deep Clean     │
│  Header/Footer → Noise Removal →    │
│  Lowercase → Tokenisasi →           │
│  Stopword Removal → Stemming        │
│  Output: clean_data.csv             │
└─────────────────────────────────────┘
        ↓
┌─────────────────────────────────────┐
│     EDA_FeatExt_NER.ipynb           │
│  EDA → Gate B5 → TextBlob →         │
│  InSet Lexicon → TF-IDF →           │
│  N-Gram → POS Tagging → NER + GPE   │
└─────────────────────────────────────┘
        ↓
┌─────────────────────────────────────┐
│     klasifikasi.ipynb               │
│  Train/Test Split (80/20) →         │
│  Augmentasi Gemini API →            │
│  Fine-tune IndoBERT Sentimen →      │
│  Fine-tune IndoBERT Tag →           │
│  Evaluasi di Test Set Asli          │
└─────────────────────────────────────┘
```

---

## 📊 Profil Dataset

### Alur Penyusutan Data

| Tahap | Jumlah |
|-------|--------|
| Link dikumpulkan (manual crawling) | 568 |
| Artikel berhasil di-scrape | 488 |
| Artikel lolos filter (≥ 50 token) | 468 |

### Distribusi per Kategori Tag (468 artikel final)

| Tag | Jumlah |
|-----|--------|
| Social | 128 |
| Investigation | 105 |
| Environment | 89 |
| Finance | 88 |
| Governance | 78 |

### Distribusi Sentimen Manual

| Sentimen | Jumlah | Keterangan |
|----------|--------|------------|
| Negatif | 195 | Kritik, dampak buruk, temuan investigasi greenwashing |
| Positif | 172 | Dukungan, klaim keberhasilan inisiatif ESG |
| Netral | 101 | Pelaporan faktual tanpa keberpihakan |

### Sumber Portal Berita
Portal media arus utama: CNBC Indonesia, Bisnis.com, Kompas, Detik, Kontan, Tribunnews

Media independen & investigasi: Project Multatuli, Mongabay, Greenpeace, Tempo, Validnews

---

## 🛠️ Tech Stack

| Kategori | Library / Tool |
|----------|---------------|
| Web Scraping | `requests`, `BeautifulSoup`, `cloudscraper`, `selenium` |
| Preprocessing | `PySastrawi`, `emoji`, `re`, `json` |
| Stopwords | Sastrawi + `louisowen6/NLP_bahasa_resources` |
| Analisis Sentimen | `TextBlob`, `deep-translator`, InSet Lexicon (`fajri91/InSet`) |
| Feature Extraction | `scikit-learn` (TF-IDF, CountVectorizer) |
| POS Tagging | `w11wo/indonesian-roberta-base-posp-tagger` (IndoBERT) |
| NER | `bryanahusna/my-nergrit-model` (IndoBERT NERGrit) |
| Augmentasi | Gemini API (`gemini-1.5-flash`) |
| Klasifikasi | IndoBERT fine-tuning via `transformers` (Hugging Face) |
| Visualisasi | `matplotlib`, `seaborn`, `wordcloud` |
| Environment | Google Colab, Python 3.10+ |

---

## 🚀 Cara Menjalankan

### 1. Clone Repository
```bash
git clone https://github.com/cafauzi13/ESG_SentimentAnalysis.git
cd ESG_SentimentAnalysis
```

### 2. Jalankan Pipeline A — Preprocessing
Buka `notebooks/cleaner_berita.ipynb` di Google Colab.

Install dependensi:
```python
!pip install PySastrawi emoji wordcloud tqdm requests beautifulsoup4
```

Notebook ini akan:
- Load `raw_data.csv` + `raw_multatuli.csv` dari GitHub
- Ekstraksi tanggal publikasi (dari URL, teks, dan scraping metadata)
- Deep clean header/footer tiap portal berita
- Menjalankan pipeline preprocessing lengkap (noise removal → lowercase → tokenisasi → stopword removal → stemming)
- Menyimpan `clean_data.csv`

### 3. Jalankan Pipeline B — EDA & Analisis Linguistik
Buka `notebooks/EDA_FeatExt_NER.ipynb` di Google Colab.

```python
!pip install deep-translator textblob scikit-learn transformers torch
```

Notebook ini akan:
- EDA distribusi data asli (tanpa augmentasi)
- Gate B5: validasi keseimbangan minimum
- Evaluasi sentimen: TextBlob (via translasi) vs InSet Lexicon (dengan negation handling)
- TF-IDF top 20 kata + N-gram bigram/trigram
- POS Tagging menggunakan IndoBERT pretrained
- NER + GPE menggunakan IndoBERT NERGrit

### 4. Jalankan Pipeline C — Augmentasi & Klasifikasi
Buka `notebooks/klasifikasi.ipynb` di Google Colab.

Sebelum menjalankan, simpan API key Gemini di Colab Secrets:
- Buka [aistudio.google.com/apikey](https://aistudio.google.com/apikey) → buat API key gratis
- Di Colab: klik ikon kunci (🔑) di sidebar → tambah secret `GEMINI_API_KEY`

```python
!pip install google-generativeai transformers torch scikit-learn
```

Notebook ini akan:
- Train/test split 80/20 stratified by Sentiment
- Menyimpan `test_set_asli.csv` (tidak disentuh lagi)
- Augmentasi train set menggunakan Gemini API (parafrase per kelas sentimen)
- Fine-tune IndoBERT untuk klasifikasi sentimen
- Fine-tune IndoBERT untuk klasifikasi tag
- Evaluasi final di test set murni

---

## 📋 Struktur Dataset

### Dataset Link Artikel (`raw_data.csv`, `raw_multatuli.csv`)

| Kolom | Deskripsi |
|-------|-----------|
| `Link` | URL artikel berita yang dikurasi secara manual |
| `Sentiment` | Label sentimen manual: Positif / Negatif / Netral |
| `Penerbit` | Nama portal media asal artikel |
| `Tag` | Kategori dimensi ESG: Environment / Social / Governance / Finance / Investigation |
| `Perusahaan` | Entitas perusahaan yang menjadi subjek utama artikel |

### Dataset Preprocessing (`clean_data.csv`)

| Kolom | Deskripsi |
|-------|-----------|
| `Link` | URL sumber artikel |
| `Sentiment` | Label sentimen manual (ground truth) |
| `Penerbit` | Portal media asal |
| `Tag` | Kategori ESG |
| `Perusahaan` | Perusahaan yang dibahas |
| `Tahun` | Tahun publikasi |
| `tanggal` | Tanggal publikasi lengkap (YYYY-MM-DD) |
| `sumber_tanggal` | Asal perolehan tanggal: `url` / `teks_raw` / `scraping` / `belum_ada` |
| `bulan` | Angka bulan publikasi (1–12) |
| `quarter` | Kuartal publikasi (misal: 2024Q1) |
| `tahun_fix` | Tahun valid (2022–2026) |
| `Isi Berita Clean` | Teks artikel setelah deep clean header/footer dan noise removal |
| `teks_bersih` | Teks setelah lowercase, cleansing, normalisasi (untuk NER & POS) |
| `tokens` | Hasil tokenisasi akhir setelah stopword removal dan stemming (JSON string) |
| `jumlah_token` | Jumlah token per artikel (artikel < 50 token dibuang) |

---

## 🔍 Panduan Label Sentimen

| Label | Kriteria | Contoh |
|-------|----------|--------|
| **Positif** | Memuat apresiasi, dukungan, atau klaim keberhasilan inisiatif ESG tanpa kontradiksi faktual | *"Bank Mandiri berhasil menyalurkan kredit hijau senilai Rp 10 triliun sebagai bentuk komitmen pembiayaan berkelanjutan"* |
| **Negatif** | Memuat kritik, temuan pelanggaran, dampak buruk lingkungan/sosial, atau indikasi greenwashing | *"Operasional tambang nikel PT Vale terbukti mencemari sumber air warga sekitar tanpa kompensasi"* |
| **Netral** | Menyajikan informasi regulasi atau fakta tanpa keberpihakan eksplisit | *"OJK menerbitkan aturan baru mengenai taksonomi hijau yang wajib diterapkan seluruh lembaga keuangan"* |

**Kasus ambigu:** Ditentukan berdasarkan framing dominan (>60% narasi artikel). Jika seimbang, dilabeli Netral.

---

## 📂 Kata Kunci Pencarian per Kategori

| Tag | Kata Kunci |
|-----|-----------|
| **Finance** | "Green Loan", "Pembiayaan Hijau", "Kredit Hijau", "Net Zero Emission", "Sustainable Finance" |
| **Governance** | "Kelapa Sawit Berkelanjutan", "RSPO", "Tata Kelola Perkebunan", "Astra Agro", "ISPO" |
| **Environment** | "Transisi Energi", "Green Mining", "Emisi Karbon", "Energi Terbarukan", "Deforestasi" |
| **Investigation** | "Korupsi Tambang", "Pertambangan Ilegal", "Korupsi Antam", "Weda Bay Nickel", "Greenwashing" |
| **Social** | "Konflik Lahan", "Masyarakat Adat", "Pekerja Tambang", "Pekerja Asing", "Hak Atas Lahan" |

---

## 📈 Ringkasan Hasil

### Analisis Sentimen Leksikon

| Metode | Akurasi | F1-Macro | Catatan |
|--------|---------|----------|---------|
| TextBlob (via translasi) | 29% | 0.26 | Rentan bias terjemahan mesin |
| InSet Lexicon + Negation Handling | 50% | 0.51 | Leksikon lokal lebih andal |

InSet Lexicon menggunakan Statistical Thresholding berbasis Q1/Q3 untuk mengatasi bias leksikal — istilah ESG seperti "emisi" atau "tambang" secara bawaan berbobot negatif di kamus, sehingga threshold statis nol tidak tepat digunakan.

### TF-IDF — Top Kata

Dua kata dengan bobot tertinggi adalah **energi** dan **bank**, mencerminkan dominasi dua sektor utama: perbankan/finansial dan ekstraktif/energi. Kata lain yang menonjol: `sawit`, `antam`, `tambang`, `berkelanjutan`, `lingkungan`, `masyarakat`.

### NER — Entitas Dominan

- **ORG:** Bank Mandiri, Bank BRI, BSI, Antam, PT Vale Indonesia
- **LOC:** Hutan, Tambang, Lahan, Smelter, Pembangkit Listrik
- **GPE:** Indonesia, Jakarta, Kalimantan, Sulawesi, Papua

Pola GPE mengindikasikan wacana regulasi ESG terpusat di Jakarta/Indonesia, namun dampak operasional terkonsentrasi di wilayah sumber daya alam luar Jawa.

---

## ⚠️ Limitasi

- Nilai F1-Macro InSet Lexicon (0.51) mencerminkan kompleksitas semantik teks ESG, bukan kegagalan model — label manual tetap digunakan sebagai ground truth
- Statistical Thresholding berbasis kuartil bersifat adaptif terhadap distribusi dataset ini dan tidak dapat digeneralisasi langsung ke korpus lain
- Fine-tuning IndoBERT untuk klasifikasi (Pipeline C) masih dalam tahap pengembangan

---

## 📚 Referensi Utama

- Koto, F., & Rahmaningtyas, G. Y. (2017). InSet Lexicon. [github.com/fajri91/InSet](https://github.com/fajri91/InSet)
- Davidescu et al. (2026). Detecting greenwashing in ESG disclosure: An NLP-based analysis. *Sustainability*, 18(3).
- Gorovaia et al. (2025). Identifying greenwashing in CSR reports using NLP. *European Financial Management*.
- Thota & Elmasri (2021). Web scraping methodology.
- Kowsari et al. (2019). Text classification algorithms: A survey.
- OJK (2017). POJK No. 51/POJK.03/2017 tentang Keuangan Berkelanjutan.

---

## 📄 Lisensi

Repositori ini dibuat untuk keperluan akademik. Seluruh data artikel berita merupakan milik portal media masing-masing.