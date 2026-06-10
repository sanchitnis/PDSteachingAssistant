# PDS Colab Teaching Assistant — Implementation Specification

> **Version**: 1.1 | **Status**: Approved | **Author**: Sanjay Chitnis
> **Course**: Python for Data Science (B25CS0101 / B25CS0102) | REVA University
> **Companion**: `reva-c-tutor-agent.md` (Advanced C Programming spec — preserved unchanged)

---

## 1. EXECUTIVE SUMMARY & TARGET STATE

* **Context**: Extends the existing REVA C Programming Teaching Assistant to support "Python for Data Science" (PDS). All existing C-tutor files are **preserved and unchanged**; PDS coexists under `pds/`.
* **Core Objective**: AI-guided, Socratic teaching assistant for PDS that runs entirely on **Google Colab**. Uses Colab's built-in AI (`from google.colab import ai` → `ai.ask()`). Delivers Labs 1–9 as individual `.ipynb` notebooks importing a single shared `pds_ai_tutor.py` kernel. Saves structured progress data per student (section + faculty_id) for future faculty dashboards.
* **Agent Operational Rule**: Do not write code outside the boundaries defined in this document. The AI tutor must NEVER produce the solution. It must always guide via Socratic questions.

---

## 2. RESOLVED DESIGN DECISIONS

| # | Question | Decision | Rationale |
| :--- | :--- | :--- | :--- |
| Q1 | Colab AI method | `ai.ask(prompt: str) → str` | Single stateless call; no session overhead; minimal tokens |
| Q2 | Shared kernel format | **`.py` module** (not `.ipynb`) | `.ipynb` JSON adds ~60–80% overhead; `.py` loads faster |
| Q3 | Student code capture | **`student_answer` named variable** | Zero magic, most beginner-friendly, no extra tokens |
| Q4 | Lab 10 Mini-Project | **Deferred** | Excluded from initial scope |
| Q5 | Faculty section tracking | **Yes — data saved, dashboard later** | `section` + `faculty_id` baked into every progress JSON |

---

## 3. ARCHITECTURE

### Stack

| Layer | Technology |
| :--- | :--- |
| Runtime | Google Colab (Python 3.x) |
| Exercise format | `.ipynb` (9-cell mandatory layout) |
| Shared kernel | `pds_ai_tutor.py` (downloaded via `urllib` in Setup Cell) |
| AI interface | `from google.colab import ai` → `ai.ask()` — no API key |
| Student code capture | `student_answer = ...` named variable |
| Progress storage | `pds_progress_<student_id>.json` on Google Drive (fallback: `/content/`) |

### Deployment

GitHub → student opens notebook via "Open in Colab" badge. Setup Cell auto-downloads `pds_ai_tutor.py` and `pds_lab_exercises.json` from GitHub raw URL. Zero local setup.

### C-Tutor Preservation

Zero files outside `pds/` are modified. All existing `exercises/`, `agents/`, `scripts/`, `rubrics/` remain untouched.

---

## 4. TOKEN OPTIMIZATION STRATEGY

| Call Type | Target Tokens (in + out) |
| :--- | :--- |
| `evaluate_answer()` Tier 1 | ≤ 400 tokens |
| `evaluate_answer()` Tier 4 | ≤ 800 tokens |
| `grade_exercise()` qualitative | ≤ 600 tokens |
| `give_hint(level)` | ≤ 350 tokens |

**Rules**: No full syllabus in prompt. Only `concept_under_test`, `constraints`, `forbidden_patterns`. Truncate student code at 60 lines. Stateless calls. Automated tests run in `exec()` — AI called only for qualitative feedback.

---

## 5. DATA SCHEMAS

### 5.1 Exercise Library (`pds/exercises/pds_lab_exercises.json`)

```json
{
  "schema_version": "1.0",
  "course_code": "B25CS0102",
  "labs": [
    {
      "lab_no": 1,
      "title": "string",
      "co_mapping": ["CO1"],
      "unit": "I",
      "bloom_level": "Apply (L3)",
      "concept_under_test": "string",
      "problem_statement": "string",
      "starter_code": "string",
      "sample_input": "string",
      "sample_output": "string",
      "test_cases": [
        {
          "label": "string",
          "setup_code": "string (exec'd before assertion)",
          "assertion": "string (eval'd, must be truthy to pass)",
          "points": 1
        }
      ],
      "constraints": ["string"],
      "forbidden_patterns": ["regex string"],
      "mental_model_checkpoints": ["string"],
      "common_mistakes": [
        { "mistake": "string", "socratic_probe": "string" }
      ],
      "grading_notes": "string",
      "estimated_time_minutes": 45
    }
  ]
}
```

### 5.2 Student Progress (`pds_progress_<student_id>.json`)

```json
{
  "student_id": "string",
  "name": "string",
  "section": "BTech-CS-1A",
  "faculty_id": "F001",
  "course_code": "B25CS0102",
  "created": "ISO datetime",
  "last_active": "ISO datetime",
  "labs": {
    "1": {
      "status": "not_started | in_progress | submitted",
      "score": 8.5,
      "help_requests": 2,
      "attempts": 1,
      "last_submission": "ISO datetime",
      "scorecard": {
        "correctness": 3.5, "style": 2.0, "completeness": 1.5,
        "documentation": 1.0, "efficiency": 0.5,
        "hardcode_flag": false
      }
    }
  }
}
```

---

## 6. PDS_TUTOR PUBLIC API

| Method | Signature | Description |
| :--- | :--- | :--- |
| Constructor | `PDS_Tutor(lab_no, student_id, name, section, faculty_id)` | Loads exercise + progress; displays welcome banner |
| Evaluate | `.evaluate_answer(student_answer)` | Socratic question via `ai.ask()` |
| Hint | `.give_hint(level: int = 1)` | Scaffold hint Tier 1–5 |
| Grade | `.grade_exercise(student_answer) → dict` | `exec()` tests + AI qualitative feedback + scorecard |
| Log | `.log_session(scorecard)` | Writes progress JSON to Drive |
| Progress | `.show_progress()` | DataFrame of all 9 labs; saves CSV |

---

## 7. NOTEBOOK CELL STRUCTURE (9-Cell Standard)

| Cell # | Type | Purpose | Editable |
| :--- | :--- | :--- | :--- |
| 1 | Code | Setup: Drive mount + download + `PDS_Tutor` init | ✅ (4 vars only) |
| 2 | Markdown | Lab header: title, CO, time, objectives | ❌ |
| 3 | Markdown | Problem statement + sample I/O | ❌ |
| 4 | Code | Starter code + `student_answer = None` | ✅ |
| 5 | Markdown | How-to instructions for cells 6–9 | ❌ |
| 6 | Code | `tutor.evaluate_answer(student_answer)` | ✅ (run) |
| 7 | Code | `tutor.give_hint(1)` — change level 1–5 | ✅ (change level) |
| 8 | Code | `tutor.grade_exercise(student_answer)` | ✅ (run) |
| 9 | Code | `tutor.show_progress()` | ✅ (run) |

### Canonical Cell 1

```python
# ─── STUDENT CONFIGURATION — Edit the 4 lines below ─────────────────────────
STUDENT_ID = "arjun22cs001"  # Your REVA student ID
NAME       = "Arjun Sharma"  # Your full name
SECTION    = "BTech-CS-1A"   # Your section (e.g. BTech-CS-1A)
FACULTY_ID = "F001"          # Your faculty's ID (ask your faculty)
# ─────────────────────────────────────────────────────────────────────────────

LAB_NO = 1  # ← DO NOT CHANGE

from google.colab import drive
drive.mount('/content/drive', force_remount=False)

import os, urllib.request
_BASE = "https://raw.githubusercontent.com/sanchitnis/PDSTeachingAssistant/main/pds"
for _url, _path in [
    (f"{_BASE}/pds_ai_tutor.py",              "/content/pds_ai_tutor.py"),
    (f"{_BASE}/exercises/pds_lab_exercises.json", "/content/pds_lab_exercises.json"),
]:
    if not os.path.exists(_path):
        urllib.request.urlretrieve(_url, _path)

%run /content/pds_ai_tutor.py
tutor = PDS_Tutor(lab_no=LAB_NO, student_id=STUDENT_ID,
                  name=NAME, section=SECTION, faculty_id=FACULTY_ID)
```

---

## 8. GRADING RUBRIC

| Dimension | Max | Evaluated By |
| :--- | :--- | :--- |
| Correctness | 4 | `exec()` — test_case assertions |
| Style & Pythonic | 2 | `ast.parse()` + regex (P01–P10) |
| Completeness & Robustness | 2 | Forbidden patterns + edge case tests |
| Documentation | 1 | Docstring regex check |
| Efficiency & Design | 1 | Colab AI qualitative (single `ai.ask()` call) |

### Python Style Rules P01–P10

| Rule | Description |
| :--- | :--- |
| P01 | `snake_case` variables/functions; `UPPER_SNAKE_CASE` constants |
| P02 | No magic numbers — assign to named constants |
| P03 | Every function must have a docstring |
| P04 | No bare `except:` — catch specific exceptions |
| P05 | Use f-strings (not `%` or `.format()`) |
| P06 | No hardcoded test data |
| P07 | No `from library import *` |
| P08 | One logical operation per line |
| P09 | Use list comprehensions where appropriate |
| P10 | 4-space indentation; no mixed tabs/spaces |

---

## 9. DIRECTORY LAYOUT

```
PDSTeachingAssistant/
├── [EXISTING C-TUTOR — UNTOUCHED]
│   ├── reva-c-tutor-agent.md
│   ├── SKILL.md, agents/, exercises/, scripts/, rubrics/, config/, docs/
│
└── pds/
    ├── pds_ai_tutor.py                         ← Shared tutor kernel
    ├── exercises/
    │   └── pds_lab_exercises.json              ← All 9 lab definitions
    ├── notebooks/
    │   ├── Lab_01_Python_Basics.ipynb
    │   ├── Lab_02_Control_Structures_Functions.ipynb
    │   ├── Lab_03_Data_Structures.ipynb
    │   ├── Lab_04_File_Handling.ipynb
    │   ├── Lab_05_NumPy_Arrays.ipynb
    │   ├── Lab_06_Pandas_Data_Manipulation.ipynb
    │   ├── Lab_07_Matplotlib_Seaborn.ipynb
    │   ├── Lab_08_EDA.ipynb
    │   └── Lab_09_Scikit_Learn_Models.ipynb
    ├── README_PDS.md
    └── docs/
        ├── PDS_IMPLEMENTATION_SPEC.md          ← This file
        └── pds_style_guide.md
```

---

## 10. LAB MAPPING (Labs 1–9)

| Lab | Title | CO | Unit |
| :--- | :--- | :--- | :--- |
| 1 | Basic Python Programs | CO1 | I |
| 2 | Control Structures & Functions | CO1, CO2 | I |
| 3 | Lists, Tuples, Sets, Dictionaries | CO2 | II |
| 4 | File Handling: Text & CSV | CO3 | II |
| 5 | NumPy Array Operations | CO3, CO4 | II |
| 6 | Pandas: Data Manipulation & Cleaning | CO4 | II |
| 7 | Data Visualization (Matplotlib + Seaborn) | CO5 | III |
| 8 | Exploratory Data Analysis (EDA) | CO5, CO6 | III |
| 9 | Simple Predictive Models (scikit-learn) | CO7 | IV |

---

## 11. VERIFICATION PLAN

1. `pds_lab_exercises.json` validates against schema (Python `jsonschema`)
2. Each `test_case.assertion` executes without `SyntaxError` in sandboxed `exec()`
3. `python -c "import sys; exec(open('pds/pds_ai_tutor.py').read())"` — no import errors
4. All 9 notebooks open top-to-bottom in a fresh Colab session
5. `tutor.evaluate_answer(None)` shows "nothing to evaluate" gracefully
6. `tutor.grade_exercise(correct_fn)` produces scorecard with all 5 dimensions
7. Progress JSON written correctly to Drive with `section` + `faculty_id` fields
8. `reva-c-tutor-agent.md` byte-for-byte unchanged after PDS build
