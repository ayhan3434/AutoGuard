# 🚗 AutoGuard

**AI-Powered Used Car Fraud Detective** · Open Agent Hackathon 2026

AutoGuard, ikinci el araç alırken karşılaşılan dolandırıcılıkları tespit eden, yapay zeka destekli bir analiz aracıdır. Bir ilanın güvenli olup olmadığını, nedenleriyle birlikte açıklar.

---

## 🌟 Features / Özellikler

- 🔍 **Recall Check** — Aracın geri çağırma kaydı var mı kontrol eder.
- 💰 **Price Analysis** — İlan fiyatını piyasa ortalamasıyla karşılaştırır.
- 📝 **Scam Keyword Detection** — İlan metnindeki riskli ifadeleri yakalar.
- 🎣 **"Sazan Sarmalı" Detection** — Aynı aracın farklı isim/fiyatla birden fazla ilanda olup olmadığını tespit eder (klasik kapora dolandırıcılığı).
- 🤖 **AI Evaluation (NVIDIA Nemotron)** — İlanı insan gibi yorumlayıp "neden şüpheli" olduğunu açıklar.

---

## 🧠 How It Works / Nasıl Çalışır

Kullanıcı bir ilanın bilgilerini girer (model, yıl, fiyat, açıklama, telefon, fotoğraf). AutoGuard:

1. Kural tabanlı analiz ile bilinen risk işaretlerini kontrol eder.
2. Örnek ilan veritabanında aynı aracı arayarak "sazan sarmalı" senaryosunu tespit eder.
3. NVIDIA Nemotron modeli ile ilanı değerlendirip kanıtlı bir açıklama üretir.
4. Sonucu **ALINABİLİR / DİKKATLİ OL / ALMA** olarak, gerekçeleriyle sunar.

> **Note:** This is a working prototype using sample data. In production, it connects to a platform's real listing archive.
> Bu çalışan bir prototiptir, örnek veriyle çalışır. Gerçek kullanımda platformun kendi ilan arşivine bağlanır.

---

## 🛠️ Tech Stack

- **Backend:** Python, FastAPI
- **AI:** NVIDIA Nemotron (`nemotron-3.5-lightning-30b-a3b`)
- **Frontend:** HTML, Jinja2

---

## 🚀 Setup / Kurulum

```bash
# Sanal ortami aktif et
python -m venv venv
venv\Scripts\activate

# Paketleri kur
pip install fastapi uvicorn httpx python-dotenv jinja2 openai python-multipart

# .env dosyasina NVIDIA API anahtarini ekle
# NVIDIA_API_KEY=nvapi-...

# Calistir
uvicorn main:app --reload
```

Tarayıcıda `http://127.0.0.1:8000` adresini aç.

---

## 👤 Author

Developed by **Ayhan** for the Open Agent Hackathon 2026.