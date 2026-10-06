# 🍽 Spice Garden — Restaurant Billing System
### BBAT104 TQM Project | Quality Goal: **Q09 – Reduce Bugs**

---

## 📌 Project Overview

A fully functional **Restaurant Billing System** built with Python + CustomTkinter,
demonstrating how **Total Quality Management (TQM)** principles — specifically **Q09:
Reduce Bugs** — are applied systematically through five concrete software quality features.

---

## 🏗 Technology Stack

| Layer          | Technology             |
|----------------|------------------------|
| GUI            | Python + CustomTkinter |
| Backend        | Python 3.11+           |
| Database       | SQLite3                |
| Testing        | pytest                 |
| Data Analysis  | Pandas                 |
| TQM Charts     | Matplotlib             |
| Version Control| Git + GitHub           |

---

## 🎯 Q09 Quality Features (5 Implemented)

| # | Feature              | Description                                          |
|---|----------------------|------------------------------------------------------|
| 1 | **Strict Validation**   | Poka-Yoke: rejects negative prices, invalid phones, empty fields |
| 2 | **Exception Handling**  | DB errors caught, logged, user shown friendly message — never crashes |
| 3 | **Module Testing**      | 40+ pytest tests across Validation, Menu, Order, Billing |
| 4 | **Bug Tracker**         | CRUD module + DB table for tracking & resolving defects |
| 5 | **Error Logging**       | Dual log (file + DB) for every error and warning event |

---

## 📂 Project Structure

```
Restaurant-Billing-TQM/
│
├── app.py                  ← Main entry point
├── requirements.txt
├── restaurant.db           ← Auto-created on first run
│
├── database/
│   ├── db.py               ← Connection, init, seed
│   └── schema.sql          ← All table definitions
│
├── modules/
│   ├── menu.py             ← Menu CRUD
│   ├── customers.py        ← Customer CRUD
│   ├── orders.py           ← Order management
│   └── billing.py          ← GST billing + stats
│
├── quality/                ← Q09 Feature implementations
│   ├── validator.py        ← Strict Validation (Feature 1)
│   ├── exception_handler.py← Exception Handling (Feature 2)
│   ├── bug_tracker.py      ← Bug Tracker (Feature 4)
│   └── error_logger.py     ← Error Logging (Feature 5)
│
├── gui/
│   ├── theme.py            ← Design tokens
│   ├── login_page.py
│   ├── main_window.py
│   └── pages/
│       ├── dashboard_page.py
│       ├── menu_page.py
│       ├── customers_page.py
│       ├── orders_page.py
│       ├── billing_page.py
│       ├── bugs_page.py    ← Bug Tracker UI
│       ├── reports_page.py ← TQM Charts UI
│       └── logs_page.py    ← Error Logs UI
│
├── tests/                  ← Q09 Feature 3 – Module Tests
│   ├── conftest.py
│   ├── test_validation.py  ← 30+ validation tests
│   ├── test_menu.py
│   ├── test_orders.py
│   └── test_billing.py
│
├── reports/
│   ├── defect_analysis.py  ← Pareto, Fishbone, PDCA, FMEA
│   └── output/             ← Generated chart images
│
└── logs/
    └── error.log           ← Application error log file
```

---

## 🚀 Running the Application

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Launch the application
python app.py
```

**Default login:** `username: admin` | `password: admin123`

---

## 🧪 Running Tests (Q09 Feature 3)

```bash
pytest tests/ -v
```

Expected output:
```
========================= test session starts ==========================
tests/test_validation.py   ✅ PASSED  (30 tests)
tests/test_menu.py         ✅ PASSED  (11 tests)
tests/test_orders.py       ✅ PASSED  (12 tests)
tests/test_billing.py      ✅ PASSED  (10 tests)
========================= 63 passed in X.XXs ===========================
```

---

## 📊 TQM Analysis Tools

All charts are generated from the **TQM Reports** page inside the application:

| Chart             | TQM Tool              | Purpose                                    |
|-------------------|-----------------------|--------------------------------------------|
| Pareto Chart      | 80/20 Analysis        | Identify top bug-contributing modules      |
| Fishbone Diagram  | Ishikawa / Root Cause | Analyse why billing errors occur           |
| PDCA Chart        | Continuous Improvement| Before/after defect comparison (73% drop)  |
| FMEA Chart        | Risk Priority Number  | Rank failure modes by S×O×D               |
| Severity Pie      | SQC Analysis          | Bug distribution by severity               |

---

## 📋 CTQ Parameters

| CTQ               | Requirement                                        |
|-------------------|----------------------------------------------------|
| Billing Accuracy  | Total = Subtotal + 5% GST (mathematically correct) |
| Input Accuracy    | Invalid values must be rejected before DB write    |
| Reliability       | Application must not crash on any input/DB error   |
| Error Recovery    | Every error handled gracefully with friendly msg   |
| Test Coverage     | All critical modules must have passing unit tests  |

---

## 📈 PDCA Results

| Phase  | Action                                                 |
|--------|--------------------------------------------------------|
| PLAN   | Identify frequent billing and validation defects       |
| DO     | Implement strict validation, exception handling, tests |
| CHECK  | Before: **67 defects** → After: **18 defects**        |
| ACT    | Standardise improved validation and testing process    |

> **Result: 73% reduction in software defects**

---

## 📄 FMEA Summary

| Failure Mode             | S | O | D | RPN |
|--------------------------|---|---|---|-----|
| Wrong bill total         | 9 | 4 | 4 | 144 |
| DB failure               | 8 | 3 | 5 | 120 |
| Empty bill generated     | 8 | 3 | 4 | 96  |
| Negative quantity        | 7 | 5 | 3 | 105 |
| Invalid phone accepted   | 5 | 6 | 2 | 60  |

---

*BBAT104 TQM Project — Q09: Reduce Bugs*
