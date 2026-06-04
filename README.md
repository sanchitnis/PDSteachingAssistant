# REVA C Tutor

**AI-powered Socratic teaching assistant for C programming — REVA University, School of CSE**

---

## What This Is

A VS Code–integrated system that assigns C programming exercises, guides students through debugging via Socratic questioning, and grades submissions against a 10-point rubric — **without ever giving them the answer**.

The agent asks questions that make students find bugs themselves. This builds the mental execution model that separates programmers from typists.

---

## Directory Structure

```
reva-c-tutor/
├── SKILL.md                    ← Master agent router (read this first)
├── reva-c-tutor-agent.md       ← Full specification and pedagogy
│
├── agents/
│   ├── help_agent.md           ← Socratic help specialist
│   └── grade_agent.md          ← Grading specialist
│
├── scripts/                    ← Data layer (no LLM calls)
│   ├── init_student.sh         ← Register a new student
│   ├── next.sh                 ← Assign next exercise
│   ├── help.sh                 ← Generate help context block
│   ├── grade.sh                ← Generate grade context block
│   ├── parse_exercise_filename.sh
│   ├── compile_check.sh
│   ├── check_style.sh
│   └── make_template.py
│
├── exercises/
│   ├── prerequisites.json       ← Prerequisite exercises
│   ├── practice.json            ← Extra practice exercises (syllabus-aligned)
│   ├── advanced.json            ← Advanced practice exercises
│   └── lab_programs.json        ← 10 mandatory lab programs
│
├── student_data/                ← Consolidated folder for student runtime data (git-ignored)
│   ├── progress/                ← Per-student progress JSON
│   └── sessions/                ← Session logs per student
│
├── config/
│   └── agent_config.json
├── rubrics/
│   └── rubric_master.md
├── docs/
│   ├── how_to_use.md           ← Student quick-start
│   └── coding_style_guide.md   ← S01–S10 rules with examples
└── .vscode/
    └── tasks.json              ← VS Code task runner shortcuts
```

---

## Quick Start (Students)

See **`docs/how_to_use.md`** for the full guide. The recommended workflow is:

1. **Register Yourself** (once): Run VS Code task **`REVA: Register Student`** and follow the prompts.
2. **Get Exercise**: Run VS Code task **`REVA: Next Exercise`** and input your Student ID. This creates your exercise file under `student_data/` (e.g. `student_data/INTRO_L1_a_raj22cs045.c`).
3. **Get Help**: Open your active exercise `.c` file and run VS Code task **`REVA: Get Help`**. In your agent chat, attach the file `student_data/help_context.txt` (type `@help_context.txt` or click `+`) and ask for support.
4. **Submit for Grading**: Run VS Code task **`REVA: Grade My Code`** with the exercise file open. Attach the generated file `student_data/grade_context.txt` in your chat and ask the agent to grade your code.

---

## Agent Architecture

```
Student attaches context file
          │
          ▼
    SKILL.md (router)
     /           \
    HELP          GRADE
     │              │
help_agent.md  grade_agent.md
(Socratic       (10-point
 protocol)       rubric)
```

**Token efficiency design**: The master `SKILL.md` is ~250 tokens. Only the relevant specialist agent is loaded per invocation (~500 tokens). The full 1300-line spec is never loaded during normal operation.

---

## Syllabus Coverage (8 Units, 20 Topics)

| Unit | Topics |
|---|---|
| 1 — Basics | INTRO, DTYPES, OPS, IO |
| 2 — Control Flow | COND, LOOP, JUMP |
| 3 — Functions | FUNC, SCOPE, RECUR |
| 4 — Arrays & Strings | ARRAY, STRING |
| 5 — Pointers | PTR, PTRARR, PTRF |
| 6 — Structures | STRUCT, UNION, ENUM |
| 7 — File I/O | FILE |
| 8 — Dynamic Memory | DYNMEM |

Topics unlock progressively: a unit must be mastered (demonstrated_level=3 for all topics) before the next unit's topics become available.

---

## For Faculty

- Student progress is in `student_data/progress/<student_id>.json`
- Session logs (Socratic dialogue history) are in `student_data/sessions/<student_id>/`
- Add exercises to `exercises/practice.json` (or `prerequisites.json` / `advanced.json`) following the schema in §6 of the spec
- The grading rubric is in `rubrics/rubric_master.md`
- Full pedagogical rationale is in `reva-c-tutor-agent.md`

---

## Dependencies

| Tool | Version | Purpose |
|---|---|---|
| gcc | ≥ 9.0 | Compile student code |
| cppcheck | ≥ 2.0 | Style checking (S01, S04, S05, S07, S09) |
| jq | ≥ 1.6 | JSON parsing in bash scripts |
| python3 | ≥ 3.8 | Exercise template generation |
| bash | ≥ 4.0 | All shell scripts |

---

*REVA University | School of Computer Science and Engineering | AY 2025-26*
