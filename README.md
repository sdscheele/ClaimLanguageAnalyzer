# Claim Language Analyzer

A lightweight patent claim analysis tool built for pre-law students, engineers, or anyone interested in patent drafting. Built using **Streamlit**, it automatically highlights legal language, scores claim breadth, and compares two claims side by side. Supports `.txt` and `.pdf` file uploads.

---

## 🚀 Features

* ✍️ Paste patent claims or upload `.txt` / `.pdf` files
* 🔦 Highlights key legal phrases (e.g. "comprising", "means for", "substantially")
* 🧮 Calculates a **Breadth Score** based on language strength and vagueness
* 📊 Extracts structural stats: word count, transition type, dependency
* ⚖️ Compares two claims to see which is broader
* 💡 Designed for legal clarity, not legal advice

---

## 📂 File Support

* `.txt` files: One claim per file
* `.pdf` files: Multi-page support (plain text PDFs only, not scans)

---

## 🛠 How to Use

1. Clone or download this repo
2. Create a Python virtual environment and activate it
3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```
4. Run locally:

   ```bash
   streamlit run app.py
   ```
5. Open the browser link provided in the terminal

---

## 📦 Technologies

* Python 3.11+
* Streamlit
* PyMuPDF (`pymupdf`)
* Regular expressions (`re`)

---

## 📸 Screenshot

*(Optional: Add a screenshot here showing the UI with some highlighted claim text)*

---

## 🙋‍♂️ Why This Exists

Patent law rewards precise language. This tool helps:

* Future law students identify functional vs. structural language
* Engineers see how phrasing affects breadth
* Interns or junior analysts quickly triage claim structure

---

## 📬 Future Ideas

* Export analyzed reports to PDF
* Add glossary tooltips
* Detect claim dependencies (claim 2 depending on claim 1, etc.)
* Visualize claim trees or limitation structure

---

## ⚖️ Disclaimer

This tool is for educational/demonstration purposes only. It does not provide legal advice or substitute for professional patent analysis.

---

## 👤 Author

Built by a sophomore Computer Science student at MSOE exploring the intersection of tech and law.
