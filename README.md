# ChartWizard

<p>
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python" />
  <img src="https://img.shields.io/badge/PyQt5-41CD52?style=for-the-badge&logo=qt&logoColor=white" alt="PyQt5" />
  <img src="https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white" alt="Pandas" />
  <img src="https://img.shields.io/badge/Matplotlib-11557C?style=for-the-badge" alt="Matplotlib" />
  <img src="https://img.shields.io/badge/Seaborn-4C72B0?style=for-the-badge" alt="Seaborn" />
</p>

## 🇬🇧 Overview

A PyQt5 GUI for quick chart exploration: load a CSV file, choose the X/Y columns and optional size, colour and marker columns, and draw a Seaborn scatter plot inside the window.

**Quick start:** `pip install -r requirements.txt && python main.py`

## 🇹🇷 Proje hakkında

CSV dosyası yükleyip sütun seçerek grafik çizdiren PyQt5 arayüzü. Seaborn ile saçılım grafiği çizer; boyut, renk ve işaretçi için ayrı sütun seçilebilir. Örnek veri olarak penguen veri seti kullanılır.

## ✨ Özellikler

- Dosya seçme penceresiyle CSV yükleme
- X, Y, boyut, renk ve işaretçi sütunu seçimi
- Grafik ve lejantı pencere içinde gösterme
- `01.ipynb`: veri temizleme adımları (`temizlenmis_penguins_size.csv` üretir)

## ⚙️ Kurulum ve çalıştırma

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

```bash
python main.py
```

## 📁 Dosya yapısı

```text
ChartWizard/
├── 01.ipynb
├── graphWidget.py
├── gui.py
├── gui.ui
├── main.py
├── penguins_size.csv
└── temizlenmis_penguins_size.csv
```
