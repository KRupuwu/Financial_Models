# Fama French 3-Factor Model – Event Study

This repository implements a **Fama-French 3-Factor Model** to estimate abnormal returns around a specific event date for a given stock. It includes regression modeling, abnormal return calculation, confidence intervals, and visualization of **Abnormal Returns (AR)** and **Cumulative Abnormal Returns (CAR)**.

---

## 📌 Features
- **Automatic Fama-French data download** from Kenneth French’s data library.
- **Daily stock returns retrieval** via Yahoo Finance (`yfinance`).
- **OLS regression** using Fama-French 3 factors (Mkt-RF, SMB, HML).
- **Abnormal Return (AR)** calculation around an event date.
- **Cumulative Abnormal Return (CAR)** calculation.
- **Confidence intervals** for AR and CAR.
- **Event window plotting** for clear visualization.

---

## 📊 Example Analysis
This example uses:
- **Ticker:** `NVDA`
- **Event Date:** `2025-02-01`
- **Estimation Window:** 200 trading days before the event.
- **Event Window:** 10 days before and after the event.

---

## 📦 Requirements
Install the required Python packages:
```bash
pip install -r requirements.txt
```

---

## ⚙️ Usage
1. **Clone the repository**
```bash
git clone https://github.com/YOUR_USERNAME/fama-french-3factor-event-study.git
cd fama-french-3factor-event-study
```

2. **Run the script**
```bash
python farma_french_3factor_(event_studies).py
```

3. **Modify parameters**
   - Change the **ticker** in the script (default `NVDA`).
   - Update `event_date` to your target event.
   - Adjust estimation/event window lengths as needed.

---

## 📂 Output
- Regression summary of the Fama-French 3-factor model.
- CSV file of merged returns and factors.
- Plot of **Abnormal Returns (AR)** with 95% confidence intervals.
- Plot of **Cumulative Abnormal Returns (CAR)** with 95% confidence intervals.

Example plots are saved in the `sample_output/` folder.

---

## 📜 Data Sources
- [Fama-French Factors – Kenneth French Data Library](https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/data_library.html)
- [Yahoo Finance API](https://pypi.org/project/yfinance/)

---

## 📝 License
This project is licensed under the MIT License – see the [LICENSE](LICENSE) file for details.

---

## 👤 Author
**Your Name** – [LinkedIn](https://linkedin.com/in/YOUR_LINKEDIN)
