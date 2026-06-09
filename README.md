# REVA C Tutor

**AI-powered Socratic teaching assistant for C programming � REVA University, School of CSE**

---

## Overview

REVA C Tutor is a VS Code�integrated system designed to help you master C programming. It assigns exercises, guides you through debugging via **Socratic questioning**, and grades your submissions based on a professional 10-point rubric.

The tutor's goal is to build your mental execution model. It will **never** give you the answer or write code for you�instead, it helps you find the bugs yourself.

---

## Prerequisites

Before starting, ensure you have the following tools installed and available in your system path:

### Required Tools (All Platforms)

| Tool | Install command (Ubuntu/WSL) | Windows Recommendation |
|---|---|---|
| GCC | `sudo apt install gcc` | [MinGW-w64](https://www.mingw-w64.org/) or [Choco](https://chocolatey.org/) |
| cppcheck | `sudo apt install cppcheck` | `choco install cppcheck` |
| Python 3 | `sudo apt install python3` | [Python.org](https://www.python.org/downloads/windows/) |

## Installation

> **Legal Notice**
>
> - **Copyright**: Copyright (c) 2026 REVA University. All Rights Reserved.
> - **Authorized Access**: Use is restricted to authorized REVA University students and employees only.
> - **Confidentiality**: All materials in this repository are proprietary. External sharing without official written approval from REVA University is strictly prohibited.
> - **Attribution**: You must retain the original copyright notice and creator attribution in all copies or substantial portions of the software.
> - **Agreement Clause**: Installing, deploying, or using any assets, plugins, or components from this repository constitutes your agreement to the terms in the [LICENSE](LICENSE) file.

To install ACPTeachingAssistant on your computer, follow these simple steps:

1. **Download**: Download the latest release source code ZIP from the [latest Release](https://github.com/sanchitnis/ACPTeachingAssistant/releases/latest).
2. **Extract**: Unzip the downloaded `.zip` file to any folder on your computer.
3. **Open in VS Code**: Open the root folder of this repository as a workspace in VS Code.

---

## Getting Started

You can interact with REVA C Tutor in three ways: **Antigravity CLI / 2.0 (Automated)**, **VS Code Tasks**, or **Terminal (Manual)**.

### Option A: Antigravity CLI / Antigravity 2.0 (Automated & Recommended)
If you are using Antigravity CLI or Antigravity 2.0, the agent has command execution and file reading capabilities. You can simply ask the agent to perform the actions for you:

1. **Register**: Ask the agent: *"Register student: ID <id>, Name <Name>, Section <Section>, Grade <Grade>"*. The agent will run the setup and configure your profile.
2. **Get Next Exercise**: Ask the agent: *"Give me my next exercise"* or *"assign next"*. The agent will assign it and create the template `.c` file.
3. **Get Help**: When stuck on an exercise, ask the agent: *"I need help with my C file"*. The agent will automatically extract the context and guide you Socrates-style.
4. **Grade Code**: When ready, ask the agent: *"Grade my code"*. The agent will compile, run tests, assess style, and give your scorecard.

---

### Option B: VS Code Tasks
Press `Ctrl+Shift+P` (Windows/Linux) or `Cmd+Shift+P` (macOS), type **Tasks: Run Task**, and select the task.

1. **Register**: Run the task **`REVA: Register Student`** and follow the prompt inputs.
2. **Get Exercise**: Run the task **`REVA: Next Exercise`** to generate your `.c` file in the `student_data/` folder.
3. **Get Help**: Open your `.c` file, run the task **`REVA: Get Help`**, and attach the generated `student_data/help_context.txt` to your agent chat.
4. **Grade Code**: Open your `.c` file, run the task **`REVA: Grade My Code`**, and attach the generated `student_data/grade_context.txt` to the agent.

---

### Option C: Terminal / Command Line (Manual)
Run these commands from the root directory of the repository:

1. **Register**:
   ```bash
   python scripts/init_student.py <id> "<Name>" "<Section>" "<1st Sem Grade>"
   ```
2. **Get Exercise**:
   ```bash
   python scripts/next.py <id>
   ```
3. **Get Help**:
   ```bash
   python scripts/help.py student_data/<filename>.c
   ```
   *(Pasted context or output from `student_data/help_context.txt` goes to the agent chat)*
4. **Grade Code**:
   ```bash
   python scripts/grade.py student_data/<filename>.c
   ```
   *(Pasted context or output from `student_data/grade_context.txt` goes to the agent chat)*

---

## The Tutor's Principles

The agent is your guide, not your ghostwriter.

**The agent will NEVER:**
- Write code for you.
- Tell you exactly which line is wrong.
- Give you the corrected version of your code.

**The agent WILL:**
- Ask questions that lead you to the answer.
- Provide analogies and partial code traces.
- Give targeted feedback on your grade and style violations.

---

## Troubleshooting

- **File Naming**: Exercises must follow `TOPIC_Ln_variant_studentid.c`. If you rename them manually, scripts may fail.
- **Active File**: Always keep the exercise `.c` file active in your editor when running **Get Help** or **Grade My Code**.
- **Tool Errors**: If the help/grade tasks fail, ensure `gcc` and `cppcheck` are correctly installed and in your PATH.

---

## Professional Standards
Code quality is as important as correctness. Refer to the [Coding Style Guide](docs/coding_style_guide.md) for rules on indentation, naming conventions, and documentation.

---

For technical details, architecture, and contribution guidelines, see [CONTRIBUTING.md](CONTRIBUTING.md).

---

*REVA University | School of Computer Science and Engineering | AY 2025-26*
