# ResearchQ - Validity & Reliability Analysis Tool

**Version:** 1.0  
**Status:** ✅ Production Ready  
**Platform:** Streamlit Web App  
**Language:** Bahasa Indonesia + English  

---

## 🎯 WHAT IS THIS?

**ResearchQ Validity & Reliability Tool** adalah web app yang memungkinkan students untuk:

1. **Upload raw data** mereka (Excel/CSV)
2. **Auto-analyze** validity & reliability:
   - Pearson Correlation Matrix
   - KMO & Bartlett's Test
   - Item-Total Correlation
   - Cronbach's Alpha (per construct)
3. **Validate SmartPLS** outer loading values
4. **Export results** ke PDF + Excel

**Tujuan:** Mahasiswa bisa **tahu apakah data mereka valid/reliable SEBELUM** input ke SPSS/SmartPLS.

---

## 💡 WHY THIS MATTERS

| Activity | Manual Way | With Tool |
|----------|-----------|-----------|
| Upload & analyze data | 30 min manual calculations | 2 min automatic |
| Check if valid | Confusing, error-prone | Clear dashboard + recommendations |
| Get interpretation | Bingung artinya apa | Auto-generated bahasa Indonesia text |
| Export to PDF/Excel | Manual formatting | Click 1x download |

**Result:** Students spend less time on validation, more time on actual analysis.

---

## 🚀 QUICK START

### Access the App

```
https://researchq-validity-tool-YOUR_USERNAME.streamlit.app
```

### Use it in 3 Steps:

#### **Step 1: Upload Data**
- Click "Browse files" di Tab "Upload & Analyze"
- Select Excel (.xlsx) atau CSV file
- File harus punya: respondents sebagai rows, items sebagai columns

#### **Step 2: Specify Constructs**
- Group items by construct
- Example:
  ```
  X1: X1.1, X1.2, X1.3, X1.4, X1.5, X1.6
  X2: X2.1, X2.2, X2.3, X2.4, X2.5, X2.6, X2.7
  Y: Y.1, Y.2, Y.3, Y.4, Y.5, Y.6, Y.7
  ```

#### **Step 3: Run Analysis**
- Click "Run Analysis"
- Tunggu 5-10 detik
- Get instant results!

#### **Step 4 (Optional): SmartPLS Validation**
- Go to Tab "SmartPLS Validation"
- Paste outer loading values dari SmartPLS
- Get instant assessment

#### **Step 5: Export**
- Go to Tab "Reports"
- Download PDF atau Excel

---

## 📊 WHAT YOU GET

### Tab 1: Upload & Analyze

**Outputs:**
- ✅ Pearson Correlation Heatmap (visual)
- ✅ Item-Total Correlation bar chart
- ✅ KMO & Bartlett assessment
- ✅ Cronbach's Alpha per construct
- ✅ All values displayed (numeric)
- ✅ Auto-interpretation text (copy-paste ready)

**Color Coding:**
- 🟢 **Green:** Valid/Excellent
- 🟡 **Yellow:** Acceptable/Marginal  
- 🔴 **Red:** Invalid/Weak

### Tab 2: SmartPLS Validation

**Inputs:**
- Copy-paste outer loading values dari SmartPLS
- Format: `Item_name = loading_value`

**Outputs:**
- ✅ Item-by-item assessment (Valid/Marginal/Invalid)
- ✅ Specific recommendations (KEEP/CONSIDER/DELETE)
- ✅ Model validity summary
- ✅ Visual distribution chart
- ✅ Interpretation

### Tab 3: Reports

**Exports:**
- 📄 **PDF Report** — Professional document with all findings
- 📊 **Excel File** — Full data with calculations & formulas

---

## 📈 DETAILED ANALYSIS EXPLAINED

### 1. Pearson Correlation Matrix
**What it is:** Shows correlation between all items  
**Interpretation:**
- Values 0.30-0.70: Good inter-item correlations
- Values > 0.80: Possible multicollinearity (item terlalu mirip)
- Values < 0.30: Item tidak berkorelasi dengan construct

### 2. KMO & Bartlett's Test
**KMO (Kaiser-Meyer-Olkin):**
- ✅ ≥ 0.70: Excellent (data cocok untuk factor analysis)
- ⚠️ 0.50-0.69: Acceptable (cukup cocok)
- ❌ < 0.50: Poor (tidak cocok)

**Bartlett's Test:**
- ✅ p < 0.05: Significant (variables berkorelasi) — GOOD
- ❌ p > 0.05: Not significant — BAD

### 3. Item-Total Correlation
**What it is:** Korelasi setiap item dengan total score  
**Interpretation:**
- ✅ > 0.40: Excellent (item berkontribusi baik)
- ⚠️ 0.30-0.40: Acceptable (marginal)
- ❌ < 0.30: Weak (item perlu dihapus)

### 4. Cronbach's Alpha
**What it is:** Measures internal consistency/reliability  
**Interpretation:**
- ✅ > 0.80: Excellent (highly reliable)
- ⚠️ 0.70-0.80: Acceptable (adequately reliable)
- ❌ < 0.70: Weak (needs item removal)

### 5. SmartPLS Outer Loading
**What it is:** Measurement model validity  
**Interpretation:**
- ✅ > 0.70: Excellent
- ✅ 0.50-0.70: Good
- ⚠️ 0.40-0.50: Marginal (consider removing)
- ❌ < 0.40: Invalid (DELETE immediately)

---

## 🔍 EXAMPLE WALKTHROUGH

### Data: Student's Thesis Data (N=30, 20 items, 3 constructs)

**Upload:**
- File: `thesis_data.xlsx`
- Contains: 30 responden × 20 items (Likert 1-5)

**Specify Constructs:**
```
X1: X1.1, X1.2, X1.3, X1.4, X1.5, X1.6
X2: X2.1, X2.2, X2.3, X2.4, X2.5, X2.6, X2.7
Y: Y.1, Y.2, Y.3, Y.4, Y.5, Y.6, Y.7
```

**Results:**
```
✅ KMO: 0.6276 (Acceptable)
✅ Bartlett p-value: < 0.001 (Significant)
✅ Cronbach X1: 0.8441 (Excellent)
✅ Cronbach X2: 0.8691 (Excellent)
⚠️ Cronbach Y: 0.7962 (Acceptable)

Recommendation:
Data VALID & RELIABLE. Ready untuk SPSS/SmartPLS analysis.
Item Y.5 & Y.7 marginal (consider removing if α < 0.70 after analysis).
```

**Export:**
- PDF: Professional report dengan semua findings
- Excel: Data + calculations + per-construct analysis

---

## 📋 FILE FORMAT REQUIREMENTS

### Input File Requirements:

**What you NEED:**
- ✅ Excel (.xlsx) atau CSV file
- ✅ Rows = Respondents
- ✅ Columns = Items (questionnaire questions)
- ✅ Values = Numeric (1-5, 1-7, etc. - Likert scale)
- ✅ NO header row OR header row in first row
- ✅ Min n=30 (for reliability testing)

**What you DON'T need:**
- ❌ ID column (remove before upload)
- ❌ Extra sheets (use first sheet only)
- ❌ Merged cells or formatting
- ❌ Missing values (remove rows with NA/blanks)

### Example Format:

```
X1.1  X1.2  X1.3  X1.4  X1.5  X1.6  X2.1  X2.2  ...  Y.7
3     3     4     4     4     3     3     4     ...  4
3     3     3     3     4     3     4     3     ...  3
4     4     4     3     4     4     4     4     ...  3
...
```

---

## ❓ FAQ

### Q: Berapa sample size minimum?
**A:** Minimum 30 (recommended 100+). Untuk SEM-PLS, ideal 100-200+.

### Q: Bisa upload file besar?
**A:** Max 200 MB (Streamlit limit). Biasanya file 100k rows masih OK.

### Q: Kalau data tidak valid, apa yang harus dilakukan?
**A:** 
1. Check KMO value. Jika < 0.50, revisi kuesioner.
2. Check Item-Total Corr. Hapus items dengan r < 0.30.
3. Check Cronbach's α. Kalau < 0.70, hapus weak items dan recalculate.

### Q: Output Excel formatnya apa?
**A:** Multi-sheet Excel:
- Sheet 1: Summary (KMO, Bartlett, n samples)
- Sheet 2: Correlation Matrix (full)
- Sheet 3: Item-Total Correlation
- Sheet 4: Cronbach's Alpha (per construct)
- Sheet 5: SmartPLS results (if applicable)

### Q: Bisa download hasil tanpa export ke PDF/Excel?
**A:** Ya, results visible di screen. Tapi export ke PDF/Excel recommended untuk dokumentasi.

### Q: Data saya rahasia. Apa tidak tersimpan di server?
**A:** ✅ **100% AMAN.** Data uploaded NOT disimpan. Proses in-memory, auto-deleted setelah session.

### Q: Bisa test berapa kali?
**A:** Unlimited (dalam free tier, recommended 10x per hari). Pro tier: truly unlimited.

---

## 🎓 LEARNING VALUE

Students belajar:
1. **Apa itu validity testing** dan kenapa penting
2. **Kapan harus gunakan** KMO & Bartlett
3. **Interpretasi Cronbach's Alpha** dengan benar
4. **Item-total correlation** meaning
5. **SmartPLS outer loading** criteria
6. **Kapan data "ready"** untuk advanced analysis

**Empowerment:** Students tidak bergantung pada statistician untuk validation checks basic.

---

## 🚀 HOW TO DEPLOY YOUR OWN

### Option A: Streamlit Cloud (Recommended)

1. **Create GitHub repo** dengan files:
   - `app.py`
   - `requirements.txt`
   - `README.md`

2. **Push to GitHub:**
   ```bash
   git add .
   git commit -m "Initial commit"
   git push
   ```

3. **Deploy:**
   - Go to https://share.streamlit.io
   - Click "Deploy an app"
   - Select your repo
   - Done! App live in 5 minutes

### Option B: Run Locally

```bash
# Install
pip install -r requirements.txt

# Run
streamlit run app.py

# Open browser
# App di http://localhost:8501
```

---

## 💰 PRICING & MONETIZATION

### Free Model (Recommended):

```
Free App + Lynk.id Purchase Link

Users:
1. Upload data → Analyze (FREE)
2. See results
3. Export to PDF/Excel (FREE)
4. Click "Support ResearchQ" → Lynk.id link
5. Pay Rp 199k-299k for package bundle

Your Revenue:
- Per use: Rp 199-299k
- Monthly subscriptions: Rp 299k/month
- Bundle with playbooks: Rp 449k+
```

### Pricing Tiers:

| Tier | Price | Includes |
|------|-------|----------|
| **Free** | Rp 0 | 1 analysis/month |
| **Basic** | Rp 199.000 | 10 analyses + PDF/Excel |
| **Pro** | Rp 299.000 | Unlimited + SmartPLS |
| **Bundle** | Rp 449.000 | Pro + Playbooks |

---

## 📞 SUPPORT & CONTACT

**WhatsApp:** 0899-1077-795  
**Lynk.id:** lynk.id/resq  
**YouTube:** NotYourLecture  
**Website:** (coming soon)

---

## 🔄 VERSION HISTORY

**v1.0** (May 28, 2026)
- ✅ Pearson Correlation Matrix
- ✅ KMO & Bartlett Test
- ✅ Item-Total Correlation
- ✅ Cronbach's Alpha (per construct)
- ✅ SmartPLS Outer Loading Validation
- ✅ PDF & Excel Export

**v1.1** (Planned)
- [ ] CFA (Confirmatory Factor Analysis)
- [ ] VIF & Multicollinearity
- [ ] Data cleaning recommendations
- [ ] User accounts & saved analyses

**v2.0** (Planned)
- [ ] SPSS API integration
- [ ] SmartPLS API integration
- [ ] Advanced SEM metrics

---

## ✅ PRODUCTION CHECKLIST

Before launch:
- [x] All calculations tested & verified
- [x] Streamlit app deployed
- [x] PDF/Excel export working
- [x] Mobile responsive
- [x] Error handling
- [x] Documentation complete
- [ ] Marketing materials ready
- [ ] Support system set up

---

## 📜 LICENSE & ATTRIBUTION

**ResearchQ.id** - Educational Technology  
**Copyright © 2026**

Built with ❤️ using:
- Streamlit
- Pandas
- NumPy
- SciPy
- Plotly

---

## 🎯 FINAL NOTE

Ini bukan hanya tool, tapi **educational platform** yang:
✅ Saves time (2 min vs 30 min)
✅ Reduces errors (automated calculations)
✅ Improves learning (clear interpretations)
✅ Builds confidence (students know when data is ready)

**Status:** Ready untuk launch! 🚀

---

**Questions?** Hubungi ResearchQ.id  
**Ready to use?** https://researchq-validity-tool.streamlit.app
