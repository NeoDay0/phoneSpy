# phoneSpy
Offline phone‑number OSINT helper — zero API keys required, ready for drop‑in use or GUI integration.

# PhoneSpy 📱🔍

> **Offline phone‑number OSINT helper** — zero API keys required, ready for drop‑in use or GUI integration.

---

## 🚀 Features

| Capability           | Details                                                                                  |
| -------------------- | ---------------------------------------------------------------------------------------- |
| **Offline‑first**    | Uses the `phonenumbers` library only – no network needed.                                |
| **Accurate parsing** | Validates numbers & produces E.164, international and national formats.                  |
| **Enrichment**       | Region, carrier (when available), number type (mobile, landline, VoIP…), and time‑zones. |
| **Export**           | Save look‑ups to **JSON** or **CSV** for further analysis.                               |
| **API‑ready stubs**  | Hooks in place for CNAM, spam‑score, Twilio Lookup, etc., when you want them.            |
| **Version‑safe**     | Handles both old & new `phonenumbers` enum APIs – no TypeErrors.                         |

--- ![f7d2f0c0-5718-4e57-9052-1d437e76f04d](https://github.com/user-attachments/assets/c38e8482-bbb9-4781-b89d-fe8c0db44ae4)


## 📂 Directory Layout

```text
phonespy/
├─ phonespy.py        # Main script (see below)
├─ README.md          # You’re reading it
├─ requirements.txt   # Python deps
├─ .gitignore         # House‑keeping
└─ LICENSE            # MIT (default)
```

---

## 🛠️ Installation

```bash
# Clone your repo
git clone https://github.com/<your_username>/phonespy.git && cd phonespy

# Install dependency
pip install -r requirements.txt
```

> **Heads‑up**: if you’re on Kali/Parrot with an "externally‑managed" Python, spin up a venv first (`python3 -m venv venv && source venv/bin/activate`).

---

## ⚡ Quick Usage

```bash
# One‑shot lookup
python3 phonespy.py +12025550123

# Batch lookup + pretty print
python3 phonespy.py +12025550123 +447911123456

# Save to JSON
python3 phonespy.py +17726661230 -o result.json

# Save multiple to CSV
python3 phonespy.py +17726661230 +16175551234 -o results.csv -f csv
```

### CLI Options

| Flag                      | Description                                                            |
| ------------------------- | ---------------------------------------------------------------------- |
| `numbers`                 | One or more phone numbers (E.164 recommended, e.g. `+12025550123`).    |
| `-o, --output FILE`       | Write results to a file. Extension ignored – control format with `-f`. |
| `-f, --format {json,csv}` | Output format (default **json**).                                      |

---

## 📝 requirements.txt

```text
phonenumbers>=8,<9
```

---

## 🙈 .gitignore

```text
# Byte‑compiled / cache
__pycache__/
*.py[cod]

# Exported data
*.json
*.csv
```

---

## 🧩 Extending PhoneSpy

1. **Caller‑ID (CNAM):** Uncomment `OPTIONAL_API_CONFIG` in `phonespy.py` and drop your [OpenCNAM](https://www.opencnam.com/) SID/token.
2. **Spam / reputation:** Pull blocklists (e.g., `phonefraudster.org`) and enrich in `basic_lookup()`.
3. **GUI front‑end:** Import `basic_lookup()` into Tkinter or PySimpleGUI and pretty‑print in a dark‑mode window.
4. **Module reuse:** The function returns a plain `dict`, perfect for integrating into GotYou, DarKsEtoolkiT, etc.

---

## 🏃 Quick‑start: publish to GitHub

```bash
mkdir phonespy && cd phonespy
# — add phonespy.py, README.md, requirements.txt, .gitignore, LICENSE —

git init
git add .
git commit -m "Initial commit – PhoneSpy offline phone lookup tool"
git branch -M main
git remote add origin https://github.com/<your_username>/phonespy.git
git push -u origin main
```

---

## 📜 License (MIT)

```
MIT License

Copyright (c) 2025 NeoDay

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
… (standard MIT text) …
```

