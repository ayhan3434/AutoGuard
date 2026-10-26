# AutoGuard - Ikinci El Arac Dedektifi
# Open Agent Hackathon 2026

import os
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()  # .env dosyasindaki anahtari yukle

from ilanlar import ORNEK_ILANLAR


def sazan_sarmasi_kontrol(model, year, telefon="", foto_id="", metin=""):
    """
    Girilen araci ornek ilan veritabaninda arar.
    Ayni arac farkli isim/fiyatla birden fazla ilanda cikiyorsa uyarir.
    """
    model = model.lower().strip()
    eslesmeler = []

    for ilan in ORNEK_ILANLAR:
        skor = 0
        nedenler = []

        # Ayni model + yil mi?
        if ilan["model"].lower() == model and ilan["year"] == year:
            skor += 1

        # Ayni telefon mu? (en guclu sinyal)
        if telefon and telefon.strip() == ilan["telefon"]:
            skor += 3
            nedenler.append("ayni telefon numarasi")

        # Ayni fotograf mi?
        if foto_id and foto_id.strip() == ilan["foto_id"]:
            skor += 2
            nedenler.append("ayni fotograf")

        # Ilan metni cok benziyor mu? (basit benzerlik)
        if metin and ilan["metin"]:
            ortak = set(metin.lower().split()) & set(ilan["metin"].lower().split())
            if len(ortak) >= 4:
                skor += 1
                nedenler.append("benzer ilan metni")

        if skor >= 2:
            eslesmeler.append({
                "ilan": ilan,
                "nedenler": nedenler,
            })

    # Ayni telefon farkli isimlerle mi? (klasik sazan sarmasi)
    isimler = set(e["ilan"]["satici"] for e in eslesmeler)
    telefonlar = set(e["ilan"]["telefon"] for e in eslesmeler)

    riskli = False
    uyari = ""
    if len(eslesmeler) >= 2 and len(telefonlar) == 1 and len(isimler) >= 2:
        riskli = True
        uyari = "Ayni telefon numarasi farkli isimlerle birden fazla ilanda kullanilmis. Bu, sazan sarmali dolandiriciliginin en net isaretidir."
    elif len(eslesmeler) >= 2:
        riskli = True
        uyari = "Ayni arac birden fazla ilanda farkli bilgilerle gorunuyor."

    return {
        "riskli": riskli,
        "uyari": uyari,
        "eslesmeler": eslesmeler,
    }

app = FastAPI(title="AutoGuard")
templates = Jinja2Templates(directory="templates")

# NVIDIA Nemotron baglantisi
NVIDIA_API_KEY = os.environ.get("NVIDIA_API_KEY", "")
ai_client = None
if NVIDIA_API_KEY:
    ai_client = OpenAI(
        base_url="https://integrate.api.nvidia.com/v1",
        api_key=NVIDIA_API_KEY,
    )


def ai_comment(model, year, price, description):
    """Nemotron ile ilan metnini yorumlar. Hata olursa None doner."""
    if not ai_client:
        return None
    try:
        prompt = (
            "Sen ikinci el arac dolandiriciligi konusunda uzman bir danismansin. "
            "Asagidaki ilan bilgilerini incele ve alici icin kisa, net bir degerlendirme yaz. "
            "Supheli noktalari ve dikkat edilmesi gerekenleri 3-4 madde halinde belirt. "
                        "SADECE Turkce son degerlendirmeyi yaz. Dusunme surecini, aciklamani veya "
            "Ingilizce metni ASLA yazma. Dogrudan madde madde degerlendirme ile basla.\n\n"
            f"Arac: {model} {year}\n"
            f"Fiyat: {price} TL\n"
            f"Ilan metni: {description}\n"
        )
        completion = ai_client.chat.completions.create(
            model="nvidia/nemotron-3.5-lightning-30b-a3b",
            messages=[
                {"role": "system", "content": "detailed thinking off"},
                {"role": "user", "content": prompt},
            ],
            temperature=0.3,
            max_tokens=1200,
        )
        content = completion.choices[0].message.content
        if content:
            return content.strip()
        return None
    except Exception as e:
        print("AI hatasi:", e)
        return None


# --- Ornek veri tabani (demo icin) ---
# Gercek projede bu veriler resmi kaynaklardan gelecek.
SAMPLE_RECALLS = {
    "corolla": ["2014-2015 Takata hava yastigi geri cagirma"],
    "focus": ["2012-2014 sanziman yazilim guncellemesi"],
}

MARKET_PRICES = {
    "corolla": 650000,
    "focus": 520000,
    "clio": 480000,
    "golf": 720000,
}

SCAM_KEYWORDS = [
    "kapora", "kaparo", "yurt disi", "yurtdisi", "kargo ile",
    "hemen gonder", "acil satilik", "vekalet", "noter masrafi",
    "deposit", "shipping", "western union",
]


# --- Analiz mantigi ---
def analyze_car(model: str, year: int, price: int, description: str):
    model = model.lower().strip()
    description = description.lower()
    findings = []
    risk_score = 0

    # 1. Geri cagirma kontrolu
    if model in SAMPLE_RECALLS:
        for recall in SAMPLE_RECALLS[model]:
            findings.append({
                "type": "uyari",
                "title": "Geri cagirma kaydi bulundu",
                "detail": recall,
            })
            risk_score += 20
    else:
        findings.append({
            "type": "ok",
            "title": "Geri cagirma kaydi yok",
            "detail": "Bu model icin kayitli geri cagirma bulunamadi.",
        })

    # 2. Fiyat kontrolu
    if model in MARKET_PRICES:
        avg = MARKET_PRICES[model]
        if price < avg * 0.6:
            findings.append({
                "type": "uyari",
                "title": "Fiyat supheli derecede dusuk",
                "detail": f"Piyasa ortalamasi ~{avg:,} TL, ilan {price:,} TL. Cok dusuk fiyat dolandiricilik isareti olabilir.",
            })
            risk_score += 30
        else:
            findings.append({
                "type": "ok",
                "title": "Fiyat makul araligda",
                "detail": f"Piyasa ortalamasi ~{avg:,} TL ile uyumlu.",
            })

    # 3. Ilan metninde dolandiricilik isaretleri
    found_keywords = [k for k in SCAM_KEYWORDS if k in description]
    if found_keywords:
        findings.append({
            "type": "tehlike",
            "title": "Ilan metninde riskli ifadeler",
            "detail": "Supheli kelimeler: " + ", ".join(found_keywords),
        })
        risk_score += 35

        # Sonuc karari
    if risk_score >= 50:
        verdict = "ALMA / DON'T BUY"
        verdict_color = "red"
    elif risk_score >= 20:
        verdict = "DIKKATLI OL / CAUTION"
        verdict_color = "orange"
    else:
        verdict = "ALINABILIR / SAFE TO BUY"
        verdict_color = "green"

    return {
        "verdict": verdict,
        "verdict_color": verdict_color,
        "risk_score": risk_score,
        "findings": findings,
    }


# --- Web sayfalari ---
@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(request, "index.html", {"result": None})


@app.post("/analyze", response_class=HTMLResponse)
def analyze(
    request: Request,
    model: str = Form(...),
    year: int = Form(...),
    price: int = Form(...),
    description: str = Form(""),
    telefon: str = Form(""),
    foto_id: str = Form(""),
):
    result = analyze_car(model, year, price, description)
    # Nemotron yapay zeka yorumu ekle
    result["ai_comment"] = ai_comment(model, year, price, description)
    # Sazan sarmasi kontrolu
    result["sazan"] = sazan_sarmasi_kontrol(model, year, telefon, foto_id, description)
    # Sazan sarmali yakalandiysa genel karari ALMA yap
    if result["sazan"]["riskli"]:
        result["verdict"] = "ALMA / DON'T BUY"
        result["verdict_color"] = "red"
        result["risk_score"] = 100
    return templates.TemplateResponse(request, "index.html", {"result": result})
    