# PDS Colab Teaching Assistant
**AI-powered Socratic tutor for Python for Data Science · REVA University, School of CSE**

---

## Overview

PDS Colab Teaching Assistant is a Google Colab-based AI tutor for the course **Python for Data Science Lab (B25CS0102)**. It assigns lab exercises, guides you through problems using **Socratic questioning**, and grades your submissions against a professional rubric — all without requiring any local installation or API keys.

> **The tutor will NEVER give you the answer.** It will ask you questions that help you find it yourself.

---

## Quick Start — Open in Colab

Click the badge for the lab you want to work on. Each notebook opens directly in Google Colab.

| Lab | Title | Open in Colab |
| :--- | :--- | :--- |
| Lab 1 | Python Basics | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/sanchitnis/PDSTeachingAssistant/blob/main/pds/notebooks/Lab_01_Python_Basics.ipynb) |
| Lab 2 | Control Structures & Functions | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/sanchitnis/PDSTeachingAssistant/blob/main/pds/notebooks/Lab_02_Control_Structures_Functions.ipynb) |
| Lab 3 | Data Structures | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/sanchitnis/PDSTeachingAssistant/blob/main/pds/notebooks/Lab_03_Data_Structures.ipynb) |
| Lab 4 | File Handling | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/sanchitnis/PDSTeachingAssistant/blob/main/pds/notebooks/Lab_04_File_Handling.ipynb) |
| Lab 5 | NumPy Array Operations | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/sanchitnis/PDSTeachingAssistant/blob/main/pds/notebooks/Lab_05_NumPy_Arrays.ipynb) |
| Lab 6 | Pandas Data Manipulation | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/sanchitnis/PDSTeachingAssistant/blob/main/pds/notebooks/Lab_06_Pandas_Data_Manipulation.ipynb) |
| Lab 7 | Matplotlib & Seaborn | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/sanchitnis/PDSTeachingAssistant/blob/main/pds/notebooks/Lab_07_Matplotlib_Seaborn.ipynb) |
| Lab 8 | Exploratory Data Analysis | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/sanchitnis/PDSTeachingAssistant/blob/main/pds/notebooks/Lab_08_EDA.ipynb) |
| Lab 9 | Scikit-learn Predictive Models | [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/sanchitnis/PDSTeachingAssistant/blob/main/pds/notebooks/Lab_09_Scikit_Learn_Models.ipynb) |

---

## How Each Notebook Works

Every lab notebook has **9 cells** in a fixed order:

| Cell | Purpose | You Edit? |
| :--- | :--- | :--- |
| 1 — Setup | Mounts Drive, downloads tutor, creates your `tutor` object | ✅ Set your 4 details |
| 2 — Lab Header | Title, CO mapping, estimated time | ❌ |
| 3 — Problem Statement | Full problem description with sample I/O | ❌ |
| 4 — Starter Code | Write your solution here; assign to `student_answer` | ✅ |
| 5 — Instructions | How to use cells 6–9 | ❌ |
| 6 — Self-Check | `tutor.evaluate_answer(student_answer)` → Socratic hint | ✅ Run |
| 7 — Hint | `tutor.give_hint(1)` → change 1–5 for more guidance | ✅ Change level |
| 8 — Submit | `tutor.grade_exercise(student_answer)` → rubric scorecard | ✅ Run |
| 9 — Progress | `tutor.show_progress()` → all lab scores | ✅ Run anytime |

---

## Getting Started — Step by Step

### Step 1: Open a Notebook
Click the "Open in Colab" badge for your lab above.

### Step 2: Fill in Your Details (Cell 1)
Edit **only these 4 lines** in the Setup Cell:

```python
STUDENT_ID = "arjun22cs001"  # Your REVA student ID
NAME       = "Arjun Sharma"  # Your full name
SECTION    = "BTech-CS-1A"   # Your section
FACULTY_ID = "F001"          # Ask your faculty for this
```

Then run Cell 1. Your Google Drive will be mounted (click Allow), and the tutor will load.

### Step 3: Read the Problem
Read Cells 2 and 3 carefully. Note the sample input/output and constraints.

### Step 4: Write Your Solution (Cell 4)
Write your solution in the starter code cell. Always assign your final answer to `student_answer`:

```python
def celsius_to_fahrenheit(celsius):
    """Convert Celsius to Fahrenheit."""
    return round((celsius * 9 / 5) + 32, 2)

student_answer = celsius_to_fahrenheit   # ← always assign here
```

### Step 5: Get Guidance (Cell 6)
Stuck? Run Cell 6. The AI tutor will ask you a Socratic question — **not give you the answer**.

### Step 6: Get Hints (Cell 7)
Need more help? Run Cell 7. Change the number `1 → 2 → 3 → 4 → 5` for progressively deeper hints.

### Step 7: Submit (Cell 8)
When ready, run Cell 8. You'll get a full rubric scorecard with per-dimension marks and AI feedback.

### Step 8: Check Progress (Cell 9)
Run Cell 9 anytime to see your scores across all 9 labs.

---

## Grading Rubric

All labs are graded out of **10 marks**:

| Dimension | Marks | How Checked |
| :--- | :--- | :--- |
| Correctness | 4 | Automated test cases |
| Style & Pythonic Quality | 2 | P01–P10 style rules |
| Completeness & Robustness | 2 | Edge cases + no hardcoding |
| Documentation | 1 | Docstrings present |
| Efficiency & Design | 1 | AI qualitative assessment |

See the full [Python Style Guide](docs/pds_style_guide.md) for P01–P10 rules.

---

## The Tutor's Principles

> The agent is your guide — not your ghostwriter.

**The tutor will NEVER:**
- Write code for you
- Tell you exactly what is wrong
- Give you the corrected version
- Award marks for hardcoded answers

**The tutor WILL:**
- Ask questions that lead you to the answer
- Give analogies and partial pseudocode (at deeper hint levels)
- Provide specific, actionable feedback on your grade
- Track your progress across all 9 labs

---

## Troubleshooting

| Problem | Solution |
| :--- | :--- |
| Drive mount fails | Click "Allow" when Colab asks for Drive access |
| Tutor doesn't load | Run Cell 1 again (check internet connection) |
| `student_answer` not recognized | Make sure you assigned your solution to `student_answer` |
| AI not responding | Colab AI may be temporarily unavailable — the tutor will use cached hints |
| Progress not saved | Check if Drive was mounted; progress falls back to `/content/` if not |

---

## File Structure

```
pds/
├── pds_ai_tutor.py                    ← Shared AI tutor kernel
├── exercises/
│   └── pds_lab_exercises.json        ← All 9 lab definitions
├── notebooks/
│   ├── Lab_01_Python_Basics.ipynb
│   └── ... (Labs 2–9)
├── README_PDS.md                      ← This file
└── docs/
    ├── PDS_IMPLEMENTATION_SPEC.md    ← Technical spec
    └── pds_style_guide.md            ← Python coding style rules P01–P10
```

---

## Legal Notice

> **Copyright**: © 2026 REVA University. All Rights Reserved.  
> **Authorized Access**: Restricted to authorized REVA University students and employees.  
> **Confidentiality**: All materials are proprietary. External sharing requires written approval.

---

*REVA University | School of Computer Science and Engineering | AY 2025–26*
