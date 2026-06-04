# REVA C Tutor — Grading Rubric
*Full detail version — mirrors §12 of the Agent Specification*

All exercises are graded out of **10 marks**.

**Design principles:**
- A student who writes working but unexplained, unstyled code **cannot score above 7**.
- A score of 10 requires clean, correct, well-styled, documented code that handles edge cases.
- Partial credit is granular — students always see exactly which sub-criterion they missed.

---

## Rubric Overview

| Dimension | Max Marks |
|---|---|
| Correctness | 4 |
| Code Quality & Style | 2 |
| Robustness & Edge Cases | 2 |
| Documentation & Readability | 1 |
| Efficiency & Design | 1 |
| **Total** | **10** |

---

## Correctness (4 marks)

| Mark | Criterion |
|---|---|
| **4/4** | Correct output for all test cases (published + any hidden faculty tests). No undefined behaviour. |
| **3/4** | Correct for published test cases; fails 1 hidden edge case. |
| **2/4** | Correct for most inputs; fails 2–3 edge cases OR has a logic error affecting a common case. |
| **1/4** | Program compiles and produces some correct output, but has a fundamental logic error. |
| **0/4** | Does not compile, produces completely wrong output, or is a hardcoded solution. |

> **Hardcoded output**: Any program that produces correct output without implementing the required
> algorithm receives **0/4 on Correctness** and a hardcoded flag in the session log.

---

## Code Quality & Style (2 marks)

| Mark | Criterion |
|---|---|
| **2/2** | Zero violations of rules S01–S10. Code is visually clean and readable. |
| **1/2** | 1–3 violations of minor rules (e.g. S08, S09). No violations of major rules S02 or S06. |
| **0/2** | 4 or more violations OR any violation of **S02** (declarations) or **S06** (main return type). |

Major rules S02 and S06 are non-negotiable — a single violation of either results in 0/2.

---

## Robustness & Edge Cases (2 marks)

| Mark | Criterion |
|---|---|
| **2/2** | All documented edge cases handled (N=0, empty input, negative values, maximum value) AND no undefined behaviour (no array out-of-bounds, no uninitialized reads). |
| **1/2** | At least one edge case handled; program does not crash on boundary input. |
| **0/2** | Crashes, produces undefined behaviour, or silently gives wrong output on edge cases. |

---

## Documentation & Readability (1 mark)

| Mark | Criterion |
|---|---|
| **1/1** | Every function has a comment block (purpose, params, return); variable names are meaningful; non-obvious logic has inline comments. |
| **0/1** | Missing function comments OR unintelligible variable names across more than 2 variables. |

---

## Efficiency & Design (1 mark)

| Mark | Criterion |
|---|---|
| **1/1** | No obviously wasteful operations (e.g. searching the same array twice when once suffices; nested O(n²) loops when O(n) is possible; allocated memory never freed). |
| **0/1** | One or more obviously inefficient constructs that a slightly more careful design would eliminate. |

---

## Score Interpretation

| Score | Agent Framing |
|---|---|
| **10/10** | "Excellent — this is publication-quality student code. Every dimension is satisfied." |
| **8–9/10** | "Strong work. You're one or two refinements away from full marks." |
| **6–7/10** | "Solid foundation — the algorithm is there. Let's make it something to be proud of." |
| **4–5/10** | "Good start — you've got [working part] working. Here is a clear path to 7+." |
| **≤3/10** | "This exercise is worth doing properly. Let's go back to the drawing board on [specific concept]." |

---

## Promotion Rules (for Faculty Reference)

| Condition | Effect |
|---|---|
| score ≥ 7 | `demonstrated_level` = `assigned_level`; `assigned_level` = min(assigned+1, 3) |
| score 5–6 | No change — student reattempts same level, different variant |
| score ≤ 4 | `assigned_level` = max(assigned-1, 1) — one level back for remediation |

---

*Pedagogical basis: Vygotsky (1978) ZPD — exercises always target one level beyond demonstrated competence.*
