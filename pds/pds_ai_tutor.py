"""
pds_ai_tutor.py — PDS Colab Teaching Assistant Kernel
=======================================================
REVA University | Python for Data Science Lab (B25CS0102)
Version : 1.0
Author  : Sanjay Chitnis & Claude AI

Usage (from exercise notebook):
    %run /content/pds_ai_tutor.py
    tutor = PDS_Tutor(lab_no=1, student_id="arjun22cs001",
                      name="Arjun Sharma", section="BTech-CS-1A",
                      faculty_id="F001")
"""

import json
import os
import ast
import re
import datetime
import inspect
import urllib.request
from IPython.display import display, HTML, Markdown
import pandas as pd

# ── Colab AI Setup ─────────────────────────────────────────────────────────────
try:
    from google.colab import ai as _colab_ai
    _AI_AVAILABLE = True
except ImportError:
    _AI_AVAILABLE = False

# ── Constants ──────────────────────────────────────────────────────────────────
_REPO_RAW = (
    "https://raw.githubusercontent.com/sanchitnis"
    "/PDSTeachingAssistant/main/pds"
)
_EXERCISE_JSON_URL  = f"{_REPO_RAW}/exercises/pds_lab_exercises.json"
_EXERCISE_JSON_PATH = "/content/pds_lab_exercises.json"
_DRIVE_PROGRESS_DIR = "/content/drive/MyDrive/PDS_Progress"
_LOCAL_PROGRESS_DIR = "/content/PDS_Progress"

# ── Load Exercise Library (once at import time) ────────────────────────────────
def _load_exercises() -> dict:
    """Download (if needed) and parse the exercise JSON; return {lab_no: lab}."""
    if not os.path.exists(_EXERCISE_JSON_PATH):
        try:
            urllib.request.urlretrieve(_EXERCISE_JSON_URL, _EXERCISE_JSON_PATH)
        except Exception as exc:
            raise RuntimeError(
                f"[PDS Tutor] Could not download exercise library: {exc}\n"
                "Check your internet connection and try re-running the Setup Cell."
            ) from exc

    with open(_EXERCISE_JSON_PATH, encoding="utf-8") as fh:
        data = json.load(fh)

    return {lab["lab_no"]: lab for lab in data["labs"]}


_EXERCISES: dict = _load_exercises()

# ══════════════════════════════════════════════════════════════════════════════
# Display Helpers
# ══════════════════════════════════════════════════════════════════════════════

def _html_banner(title: str, body: str,
                 bg: str = "#0f3460", accent: str = "#e94560") -> None:
    """Render a styled HTML banner in the notebook output."""
    html = f"""
<div style="
    background:{bg};
    border-left:5px solid {accent};
    padding:14px 18px;
    margin:8px 0;
    border-radius:8px;
    font-family:'Google Sans',Roboto,sans-serif;
    color:#f0f0f0;
    line-height:1.6;
">
  <div style="
      font-size:1.05em;
      font-weight:700;
      color:{accent};
      margin-bottom:6px;
      letter-spacing:0.02em;
  ">{title}</div>
  <div style="font-size:0.93em;">{body}</div>
</div>
""".strip()
    display(HTML(html))


def _score_bar(label: str, score: float, max_score: float, colour: str) -> str:
    """Return an HTML string for a single rubric score bar (used inside a banner)."""
    pct   = int((score / max_score) * 100) if max_score else 0
    width = max(pct * 1.8, 4)          # px, minimum visible
    return (
        f'<div style="margin:3px 0;display:flex;align-items:center;gap:8px;">'
        f'<span style="display:inline-block;width:180px;font-weight:600;'
        f'font-size:0.88em;">{label}</span>'
        f'<div style="background:#333;border-radius:4px;height:12px;width:200px;">'
        f'<div style="background:{colour};border-radius:4px;height:12px;'
        f'width:{width}px;"></div></div>'
        f'<span style="font-size:0.9em;">{score}/{max_score}</span>'
        f'</div>'
    )


# ══════════════════════════════════════════════════════════════════════════════
# PDS_Tutor Class
# ══════════════════════════════════════════════════════════════════════════════

class PDS_Tutor:
    """
    Socratic AI teaching assistant for the PDS Lab.

    Public methods:
        evaluate_answer(student_answer)   → displays a Socratic hint
        give_hint(level=1)                → displays a scaffolded hint
        grade_exercise(student_answer)    → runs tests + displays scorecard
        log_session(scorecard)            → saves progress to Drive
        show_progress()                   → displays progress table across labs
    """

    # Scaffold tier labels (mirrored in spec §3.3)
    _TIER_LABELS = {
        1: "Conceptual Question",
        2: "Analogy + Trace",
        3: "Partial Pseudocode",
        4: "Structural Approach",
        5: "Step Back & Review",
    }

    # Score-band motivational messages
    _BANDS = [
        (9.0, "#1b5e20", "🏆 Excellent — clean, correct, Pythonic. Every dimension satisfied."),
        (7.0, "#2e7d32", "💪 Strong work. You're one or two refinements away from full marks."),
        (5.5, "#f9a825", "🔧 Solid foundation — the algorithm is there. Let's polish it."),
        (3.0, "#e65100", "🌱 Good start — here is a clear path to 7+."),
        (0.0, "#c62828", "📖 Let's revisit the core concept. A warm-up example follows."),
    ]

    # ── Constructor ─────────────────────────────────────────────────────────────
    def __init__(self, lab_no: int, student_id: str, name: str,
                 section: str, faculty_id: str) -> None:
        """
        Initialise the tutor for a specific lab and student.

        Args:
            lab_no     : Lab number 1–9.
            student_id : Student's REVA ID (e.g. 'arjun22cs001').
            name       : Student's full name.
            section    : Class section (e.g. 'BTech-CS-1A').
            faculty_id : Faculty identifier for cohort tracking.
        """
        if lab_no not in _EXERCISES:
            raise ValueError(
                f"Lab {lab_no} not found in exercise library. "
                f"Available: {sorted(_EXERCISES.keys())}"
            )

        self.lab_no     = lab_no
        self.student_id = student_id.strip().lower()
        self.name       = name.strip()
        self.section    = section.strip()
        self.faculty_id = faculty_id.strip()
        self._lab       = _EXERCISES[lab_no]

        self._progress_dir, self._progress_file = self._resolve_paths()
        self._progress = self._load_progress()

        self._display_welcome()

    # ── Path resolution ─────────────────────────────────────────────────────────
    def _resolve_paths(self) -> tuple[str, str]:
        """Return (directory, file_path) for the student's progress JSON."""
        drive_ok = os.path.isdir("/content/drive/MyDrive")
        base     = _DRIVE_PROGRESS_DIR if drive_ok else _LOCAL_PROGRESS_DIR
        os.makedirs(base, exist_ok=True)
        return base, os.path.join(base, f"pds_progress_{self.student_id}.json")

    # ── Progress I/O ────────────────────────────────────────────────────────────
    def _load_progress(self) -> dict:
        """Load or initialise the student's progress JSON."""
        if os.path.exists(self._progress_file):
            with open(self._progress_file, encoding="utf-8") as fh:
                return json.load(fh)

        return {
            "student_id" : self.student_id,
            "name"       : self.name,
            "section"    : self.section,
            "faculty_id" : self.faculty_id,
            "course_code": "B25CS0102",
            "created"    : datetime.datetime.utcnow().isoformat(),
            "last_active": datetime.datetime.utcnow().isoformat(),
            "labs"       : {},
        }

    def _save_progress(self) -> None:
        """Persist the progress dict to Drive (or /content/ fallback)."""
        self._progress["last_active"] = datetime.datetime.utcnow().isoformat()
        with open(self._progress_file, "w", encoding="utf-8") as fh:
            json.dump(self._progress, fh, indent=2, ensure_ascii=False)

    def _lab_progress(self) -> dict:
        """Return (and auto-initialise) this lab's entry in the progress dict."""
        key = str(self.lab_no)
        if key not in self._progress["labs"]:
            self._progress["labs"][key] = {
                "status"         : "not_started",
                "score"          : None,
                "help_requests"  : 0,
                "attempts"       : 0,
                "last_submission": None,
                "scorecard"      : {},
            }
        return self._progress["labs"][key]

    # ── Code extraction ─────────────────────────────────────────────────────────
    @staticmethod
    def _code_snippet(student_answer, max_lines: int = 60) -> str:
        """Extract a token-safe code snippet from the student's answer."""
        try:
            if callable(student_answer):
                src = inspect.getsource(student_answer)
            else:
                src = repr(student_answer)
        except Exception:
            src = str(student_answer)

        lines = src.splitlines()
        if len(lines) > max_lines:
            lines = lines[:max_lines] + [
                f"# [...{len(lines) - max_lines} more lines truncated for brevity]"
            ]
        return "\n".join(lines)

    # ── Forbidden-pattern check ─────────────────────────────────────────────────
    def _check_forbidden(self, code_str: str) -> list[str]:
        """Return list of matched forbidden patterns in student code."""
        return [
            pat for pat in self._lab.get("forbidden_patterns", [])
            if re.search(pat, code_str, re.IGNORECASE)
        ]

    # ── Style check (P01–P10) ───────────────────────────────────────────────────
    @staticmethod
    def _check_style(code_str: str) -> list[str]:
        """Run P01–P10 style checks; return list of violation strings."""
        issues: list[str] = []

        # P04 — bare except
        if re.search(r'\bexcept\s*:', code_str):
            issues.append("P04: Bare `except:` — catch a specific exception (e.g. `except ValueError:`)")

        # P07 — wildcard imports
        if re.search(r'from\s+\w+\s+import\s+\*', code_str):
            issues.append("P07: Wildcard import `from ... import *` — import only what you need")

        # P10 — tab characters
        if '\t' in code_str:
            issues.append("P10: Tab characters found — use 4 spaces for indentation")

        # P05 — %-formatting or .format()
        if re.search(r'%[sdif]', code_str) or re.search(r'\.format\(', code_str):
            issues.append("P05: Prefer f-strings over `%` formatting or `.format()`")

        # P03 — missing docstrings on functions
        try:
            tree = ast.parse(code_str)
            for node in ast.walk(tree):
                if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    first = node.body[0] if node.body else None
                    has_doc = (
                        isinstance(first, ast.Expr)
                        and isinstance(getattr(first, "value", None), ast.Constant)
                        and isinstance(first.value.value, str)
                    )
                    if not has_doc:
                        issues.append(
                            f"P03: Function `{node.name}` is missing a docstring"
                        )
        except SyntaxError:
            issues.append("Syntax error — cannot fully check style rules")

        return issues

    # ── Colab AI call ───────────────────────────────────────────────────────────
    def _ask_ai(self, prompt: str, fallback: str) -> str:
        """
        Call Colab AI with a token-optimised prompt.
        Falls back to a cached Socratic question if AI is unavailable.
        """
        if _AI_AVAILABLE:
            try:
                return _colab_ai.ask(prompt)
            except Exception:
                pass  # fall through to cached fallback

        return fallback

    # ── Prompt builders ─────────────────────────────────────────────────────────
    def _eval_prompt(self, code_snippet: str, tier: int) -> str:
        """Build a token-optimised Socratic evaluation prompt."""
        lab     = self._lab
        concept = lab.get("concept_under_test", "the current concept")
        base    = (
            f"Socratic tutor. Python Data Science. "
            f"Lab {self.lab_no}: {lab['title']}. "
            f"Concept: {concept}. "
            f"RULE: NEVER write code or reveal the solution. "
        )
        snippet = f"Student code:\n```python\n{code_snippet}\n```\n"

        if tier <= 1:
            return (
                base +
                "Ask exactly ONE Level-1 (Recall) or Level-2 (Comprehension) "
                "Socratic question. No hints beyond a question.\n" + snippet
            )
        elif tier == 2:
            return (
                base +
                "Give ONE real-world analogy relevant to the concept, "
                "then ask ONE memory-trace question. No code.\n" + snippet
            )
        elif tier == 3:
            constraints = "; ".join(lab.get("constraints", [])[:3])
            return (
                base +
                f"Constraints: {constraints}. "
                "Write partial pseudocode ONLY (no Python syntax). "
                "End with ONE question asking the student to fill in the next step.\n"
                + snippet
            )
        else:
            return (
                base +
                "Describe the overall structural approach in plain English. "
                "Do NOT write any code. "
                "End with ONE question prompting the student to start writing.\n"
                + snippet
            )

    def _grade_prompt(self, code_snippet: str, pass_count: int,
                      total_tests: int, style_issues: list[str],
                      score_band: str) -> str:
        """Build a token-optimised grading qualitative feedback prompt."""
        style_str = "; ".join(style_issues) if style_issues else "None"
        return (
            f"PDS grader. Lab {self.lab_no}: {self._lab['title']}. "
            f"Automated tests: {pass_count}/{total_tests} passed. "
            f"Style issues: {style_str}. Score band: {score_band}. "
            f"Grading notes: {self._lab.get('grading_notes', '')}. "
            "Give: 1 concise sentence per dimension (style/docs/efficiency). "
            "Then 1 specific, actionable improvement. "
            "Then 1 motivational closing sentence. "
            "DO NOT rewrite or show corrected code.\n"
            f"Student code:\n```python\n{code_snippet}\n```"
        )

    # ── Welcome banner ──────────────────────────────────────────────────────────
    def _display_welcome(self) -> None:
        """Render the lab welcome banner with student info and status."""
        lab  = self._lab
        lp   = self._lab_progress()
        co   = ", ".join(lab.get("co_mapping", []))
        mins = lab.get("estimated_time_minutes", 45)

        status_map = {
            "not_started": "🔵 Not Started",
            "in_progress": "🟡 In Progress",
            "submitted"  : "🟢 Submitted",
        }
        status_txt = status_map.get(lp.get("status", "not_started"), "—")
        score_txt  = (f"{lp['score']}/10"
                      if lp.get("score") is not None else "—")

        body = (
            f"<b>Student:</b> {self.name} ({self.student_id}) &nbsp;|&nbsp; "
            f"<b>Section:</b> {self.section}<br>"
            f"<b>CO Mapping:</b> {co} &nbsp;|&nbsp; "
            f"<b>Est. Time:</b> {mins} min<br>"
            f"<b>Status:</b> {status_txt} &nbsp;|&nbsp; "
            f"<b>Best Score:</b> {score_txt}<br><br>"
            f"<b>🎯 Concept Under Test:</b> {lab.get('concept_under_test', '')}<br><br>"
            f"<span style='font-size:0.88em;color:#aaa;'>"
            f"▸ <code>tutor.evaluate_answer(student_answer)</code> — get Socratic guidance<br>"
            f"▸ <code>tutor.give_hint(1)</code> — scaffolded hint (change 1→5)<br>"
            f"▸ <code>tutor.grade_exercise(student_answer)</code> — submit & get score<br>"
            f"▸ <code>tutor.show_progress()</code> — view all lab scores</span>"
        )
        _html_banner(f"🐍 PDS Lab {self.lab_no} — {lab['title']}", body,
                     bg="#0a1628", accent="#4fc3f7")

        if not os.path.isdir("/content/drive/MyDrive"):
            _html_banner(
                "⚠️ Google Drive Not Mounted",
                "Your progress will <b>not persist</b> across sessions. "
                "Run <code>drive.mount('/content/drive')</code> in a new cell to save your work.",
                bg="#2a1400", accent="#ff8c00"
            )

    # ══════════════════════════════════════════════════════════════════════════
    # Public API
    # ══════════════════════════════════════════════════════════════════════════

    def evaluate_answer(self, student_answer) -> None:
        """
        Evaluate student's answer and display a Socratic question.

        Does NOT reveal the solution — always responds with a question
        that guides the student to discover the issue themselves.

        Args:
            student_answer: The student's solution — a function, value, or object.
        """
        if student_answer is None:
            _html_banner(
                "🤔 Nothing to Evaluate Yet",
                "Write your solution in the starter code cell and assign it to "
                "<code>student_answer</code>, then run this cell again.",
                bg="#1a1a2e", accent="#e94560"
            )
            return

        # Update progress
        lp = self._lab_progress()
        lp["help_requests"] = lp.get("help_requests", 0) + 1
        lp["status"] = "in_progress"
        self._save_progress()

        tier    = min(lp["help_requests"], 5)
        snippet = self._code_snippet(student_answer)
        prompt  = self._eval_prompt(snippet, tier)

        mistakes = self._lab.get("common_mistakes", [])
        fallback = (
            mistakes[0]["socratic_probe"] if mistakes else
            "Before we look at anything specific — tell me in one sentence: "
            "what do you think your code is currently doing?"
        )

        response   = self._ask_ai(prompt, fallback)
        tier_label = self._TIER_LABELS.get(tier, "Hint")

        _html_banner(
            f"💡 Hint #{lp['help_requests']} — {tier_label}",
            response.replace("\n", "<br>"),
            bg="#0d2818", accent="#66bb6a"
        )

    # ────────────────────────────────────────────────────────────────────────────

    def give_hint(self, level: int = 1) -> None:
        """
        Display a scaffolded hint at the specified level.

        Level 1 = shallowest (conceptual question only).
        Level 5 = deepest (step-back redirect with mental model checkpoint).

        Args:
            level: Hint depth 1–5 (int).
        """
        level = max(1, min(5, int(level)))
        lab   = self._lab

        if level == 5:
            checkpoints = lab.get("mental_model_checkpoints", [])
            tip = checkpoints[0] if checkpoints else (
                "Re-read the lab problem statement. Can you describe "
                "the expected output for the sample input in plain English?"
            )
            _html_banner(
                "📖 Level 5 — Step Back & Review",
                f"Take a breath. Before writing more code, answer this question "
                f"on paper first:<br><br>"
                f"<i style='color:#ffcc80;'>'{tip}'</i><br><br>"
                f"If you can answer that clearly, you're ready to code again.",
                bg="#1c1000", accent="#ffab40"
            )
            return

        prompt = (
            f"Socratic tutor. Python Data Science. "
            f"Lab {self.lab_no}: {lab['title']}. "
            f"Concept: {lab.get('concept_under_test', '')}. "
            f"Provide a Level-{level} hint ({self._TIER_LABELS[level]}). "
            f"No solution code. End with ONE question."
        )

        mistakes = lab.get("common_mistakes", [])
        fallback = (
            mistakes[min(level - 1, len(mistakes) - 1)]["socratic_probe"]
            if mistakes else
            "What is the expected output of your function for the sample input?"
        )

        response = self._ask_ai(prompt, fallback)
        _html_banner(
            f"💡 Level {level} Hint — {self._TIER_LABELS[level]}",
            response.replace("\n", "<br>"),
            bg="#160a28", accent="#ce93d8"
        )

    # ────────────────────────────────────────────────────────────────────────────

    def grade_exercise(self, student_answer) -> dict:
        """
        Grade the student's solution against automated test cases.

        Steps:
          1. Forbidden-pattern check (hardcode detection).
          2. Style analysis (P01–P10).
          3. Run each test_case in a sandboxed exec() scope.
          4. Compute rubric scores (Correctness, Style, Completeness, Docs).
          5. Call ai.ask() once for qualitative Efficiency + overall feedback.
          6. Display formatted scorecard.
          7. Persist to progress JSON.

        Args:
            student_answer: The student's solution.

        Returns:
            dict: Scorecard with per-dimension scores and total (0–10).
        """
        if student_answer is None:
            _html_banner(
                "❌ Nothing to Grade",
                "Assign your solution to <code>student_answer</code> "
                "in the starter code cell, then run this cell.",
                bg="#200000", accent="#f44336"
            )
            return {}

        lab      = self._lab
        snippet  = self._code_snippet(student_answer)
        try:
            code_str = (inspect.getsource(student_answer)
                        if callable(student_answer) else repr(student_answer))
        except Exception:
            code_str = str(student_answer)

        # ── 1. Forbidden patterns ──────────────────────────────────────────────
        forbidden_hits = self._check_forbidden(code_str)
        hardcode_flag  = bool(forbidden_hits)

        # ── 2. Style check ─────────────────────────────────────────────────────
        style_issues = self._check_style(code_str)

        # ── 3. Run test cases ──────────────────────────────────────────────────
        test_cases    = lab.get("test_cases", [])
        total_points  = sum(tc.get("points", 1) for tc in test_cases)
        earned_points = 0
        test_results  = []          # (label, passed, pts, err_msg)

        for tc in test_cases:
            label     = tc.get("label", "Test")
            setup     = tc.get("setup_code", "")
            assertion = tc.get("assertion", "True")
            pts       = tc.get("points", 1)
            ns        = {"student_answer": student_answer}

            try:
                if setup:
                    exec(setup, ns)           # noqa: S102
                passed = bool(eval(assertion, ns))  # noqa: S307
                if passed:
                    earned_points += pts
                test_results.append((label, passed, pts, ""))
            except Exception as exc:
                test_results.append((label, False, pts, str(exc)[:100]))

        # ── 4. Compute rubric scores ───────────────────────────────────────────
        ratio = earned_points / total_points if total_points else 0.0

        # Correctness (0–4)
        if hardcode_flag:
            correctness = 0.0
        else:
            correctness = round(ratio * 4, 1)

        # Style (0–2)
        n_style     = len(style_issues)
        style_score = 2.0 if n_style == 0 else (1.0 if n_style <= 2 else 0.0)

        # Completeness / Robustness (0–2)
        has_bare_except = any("P04" in i for i in style_issues)
        completeness = (
            2.0 if (not hardcode_flag and not has_bare_except and ratio >= 0.75) else
            1.0 if ratio >= 0.5 else
            0.0
        )

        # Documentation (0–1)
        doc_issues  = [i for i in style_issues if "P03" in i]
        documentation = 0.0 if doc_issues else 1.0

        # ── 5. AI qualitative feedback ─────────────────────────────────────────
        running_total = correctness + style_score + completeness + documentation
        score_band = (
            "10"  if running_total >= 9   else
            "8-9" if running_total >= 7   else
            "6-7" if running_total >= 5.5 else
            "4-5" if running_total >= 3   else
            "≤3"
        )

        grade_prompt = self._grade_prompt(
            snippet, sum(1 for _, p, _, _ in test_results if p),
            len(test_cases), style_issues, score_band
        )
        fallback_feedback = (
            ("⚠️ Hardcoded answer detected — this will not generalise. "
             "Your solution must work for any valid input.\n\n") if hardcode_flag else ""
        ) + (
            f"Tests passed: {earned_points}/{total_points} points. "
            + ("Fix missing docstrings. " if doc_issues else "")
            + ("Fix bare except. "        if has_bare_except else "")
            + ("Great job on style! "     if not style_issues else "")
        )

        ai_feedback = self._ask_ai(grade_prompt, fallback_feedback)
        efficiency  = 1.0 if ai_feedback and not fallback_feedback in ai_feedback else 0.5

        total = min(10.0, round(
            correctness + style_score + completeness + documentation + efficiency, 1
        ))

        scorecard = {
            "correctness"  : correctness,
            "style"        : style_score,
            "completeness" : completeness,
            "documentation": documentation,
            "efficiency"   : efficiency,
            "total"        : total,
            "hardcode_flag": hardcode_flag,
            "tests_passed" : sum(1 for _, p, _, _ in test_results if p),
            "tests_total"  : len(test_cases),
            "style_issues" : style_issues,
            "ai_feedback"  : ai_feedback,
        }

        # ── 6. Display ─────────────────────────────────────────────────────────
        self._display_scorecard(test_results, scorecard, ai_feedback)

        # ── 7. Persist ─────────────────────────────────────────────────────────
        self.log_session(scorecard)

        return scorecard

    # ────────────────────────────────────────────────────────────────────────────

    def _display_scorecard(self, test_results: list, sc: dict,
                           ai_feedback: str) -> None:
        """Render the full grade report as a styled HTML banner."""

        # Test-case results table
        rows = ""
        for label, passed, pts, err in test_results:
            icon  = "✅" if passed else "❌"
            pts_s = f"+{pts}" if passed else f"0/{pts}"
            err_s = (f' <span style="color:#ff6b6b;font-size:0.82em;">({err})</span>'
                     if err else "")
            rows += (
                f'<tr style="border-bottom:1px solid #333;">'
                f'<td style="padding:3px 6px;">{icon}</td>'
                f'<td style="padding:3px 8px;">{label}{err_s}</td>'
                f'<td style="padding:3px 6px;text-align:right;">{pts_s} pt</td>'
                f'</tr>'
            )
        test_table = (
            f'<table style="width:100%;border-collapse:collapse;'
            f'margin:8px 0;font-size:0.88em;">'
            f'<tr style="background:#1e3a5f;font-weight:700;">'
            f'<th style="padding:4px 6px;">✓</th>'
            f'<th style="padding:4px 8px;text-align:left;">Test Case</th>'
            f'<th style="padding:4px 6px;">Points</th>'
            f'</tr>{rows}</table>'
        )

        # Rubric bars
        bars = (
            _score_bar("Correctness (4)",    sc["correctness"],   4, "#4caf50") +
            _score_bar("Style P01–P10 (2)",  sc["style"],         2, "#2196f3") +
            _score_bar("Completeness (2)",   sc["completeness"],  2, "#ff9800") +
            _score_bar("Documentation (1)",  sc["documentation"], 1, "#9c27b0") +
            _score_bar("Efficiency (1)",     sc["efficiency"],    1, "#00bcd4")
        )

        # Score colour + band message
        total = sc["total"]
        band_colour, band_msg = "#4caf50", ""
        for threshold, colour, msg in self._BANDS:
            if total >= threshold:
                band_colour, band_msg = colour, msg
                break

        hc_warning = (
            '<div style="color:#ff6b6b;font-weight:bold;margin:6px 0;">'
            '⚠️ Hardcoded answer detected — Correctness score is 0/4. '
            'Your solution must work for any valid input.</div>'
            if sc["hardcode_flag"] else ""
        )

        body = (
            hc_warning
            + test_table
            + bars
            + f'<div style="font-size:1.3em;font-weight:700;'
            f'color:{band_colour};margin:12px 0 8px;">'
            f'Total: {total} / 10</div>'
            + f'<div style="font-size:0.88em;color:#aaa;">{band_msg}</div>'
            + '<hr style="border:none;border-top:1px solid #333;margin:10px 0;"/>'
            + f'<div style="font-size:0.9em;">'
            + ai_feedback.replace("\n", "<br>")
            + "</div>"
        )

        _html_banner(f"📊 Grade Report — Lab {self.lab_no}", body,
                     bg="#0d1b2a", accent="#4fc3f7")

    # ────────────────────────────────────────────────────────────────────────────

    def log_session(self, scorecard: dict) -> None:
        """
        Save the session scorecard to the student's progress JSON.

        Args:
            scorecard: The dict returned by grade_exercise().
        """
        lp                    = self._lab_progress()
        lp["attempts"]        = lp.get("attempts", 0) + 1
        lp["status"]          = "submitted"
        lp["score"]           = scorecard.get("total", 0)
        lp["last_submission"] = datetime.datetime.utcnow().isoformat()
        lp["scorecard"]       = {
            k: v for k, v in scorecard.items() if k != "ai_feedback"
        }
        self._save_progress()

        storage = ("Google Drive" if os.path.isdir("/content/drive/MyDrive")
                   else "/content/ (local — not persistent)")
        _html_banner(
            "💾 Progress Saved",
            f"Lab {self.lab_no} score <b>{scorecard.get('total', 0)}/10</b> "
            f"saved to <i>{storage}</i>.",
            bg="#0a2e0a", accent="#81c784"
        )

    # ────────────────────────────────────────────────────────────────────────────

    def show_progress(self) -> None:
        """Display a summary progress table across all 9 labs and save as CSV."""
        rows = []
        for lab_no in sorted(_EXERCISES.keys()):
            lab_data = _EXERCISES[lab_no]
            key      = str(lab_no)
            lp       = self._progress["labs"].get(key, {})

            status_map = {
                "not_started": "🔵 Not Started",
                "in_progress": "🟡 In Progress",
                "submitted"  : "🟢 Submitted",
            }
            rows.append({
                "Lab"         : lab_no,
                "Title"       : lab_data["title"],
                "CO"          : ", ".join(lab_data.get("co_mapping", [])),
                "Status"      : status_map.get(lp.get("status", "not_started"), "🔵 Not Started"),
                "Score"       : (f"{lp['score']}/10"
                                 if lp.get("score") is not None else "—"),
                "Help Reqs"   : lp.get("help_requests", 0),
                "Attempts"    : lp.get("attempts", 0),
                "Last Active" : (lp.get("last_submission") or "—")[:16].replace("T", " "),
            })

        df = pd.DataFrame(rows)

        csv_path = os.path.join(
            self._progress_dir,
            f"pds_progress_{self.student_id}_report.csv"
        )
        df.to_csv(csv_path, index=False)

        submitted = sum(1 for r in rows if "Submitted" in r["Status"])
        display(Markdown(
            f"## 📈 Progress Report — {self.name}\n"
            f"**{submitted}/9 labs submitted** | Section: {self.section}"
        ))
        display(df)
        _html_banner(
            "✅ Report Saved",
            f"CSV saved to <code>{csv_path}</code>",
            bg="#0a2e0a", accent="#81c784"
        )


# ── Module-level confirmation ──────────────────────────────────────────────────
print(f"✅ PDS AI Tutor loaded — {len(_EXERCISES)} lab(s) available "
      f"{'| Colab AI: ON' if _AI_AVAILABLE else '| Colab AI: OFF (fallback hints active)'}")
