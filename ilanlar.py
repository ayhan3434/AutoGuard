# Ornek ilan veritabani (DEMO)
# Gercek projede bu veriler platformun kendi arsivinden gelir.
# Buradaki tum isim, telefon ve bilgiler uydurmadir.

ORNEK_ILANLAR = [
    {
        "id": "IL-1001",
        "site": "ornekoto.com",
        "model": "Corolla",
        "year": 2015,
        "km": 145000,
        "renk": "beyaz",
        "price": 640000,
        "telefon": "0532 111 2233",
        "satici": "Ahmet Y.",
        "foto_id": "foto_A",
        "metin": "2015 Corolla, bakimli, orjinal, tramersiz, gorulebilir.",
    },
    {
        "id": "IL-1002",
        "site": "ornekoto.com",
        "model": "Clio",
        "year": 2018,
        "km": 90000,
        "renk": "gri",
        "price": 470000,
        "telefon": "0541 222 3344",
        "satici": "Zeynep K.",
        "foto_id": "foto_B",
        "metin": "Clio 2018, tek elden, hatasiz boyasiz.",
    },
    # --- SAZAN SARMASI SENARYOSU ---
    # Ayni arac (foto_X, ayni telefon) iki farkli isim ve fiyatla.
    {
        "id": "IL-2001",
        "site": "ornekoto.com",
        "model": "Golf",
        "year": 2019,
        "km": 72000,
        "renk": "siyah",
        "price": 760000,
        "telefon": "0555 987 6543",
        "satici": "Murat D.",
        "foto_id": "foto_X",
        "metin": "2019 Golf, hayalet, cam tavan, servis bakimli.",
    },
    {
        "id": "IL-2002",
        "site": "baskaoto.com",
        "model": "Golf",
        "year": 2019,
        "km": 72000,
        "renk": "siyah",
        "price": 540000,
        "telefon": "0555 987 6543",
        "satici": "Selin A.",
        "foto_id": "foto_X",
        "metin": "2019 Golf, hayalet, cam tavan, servis bakimli. Acil, kapora ile.",
    },
]