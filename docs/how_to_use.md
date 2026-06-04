# REVA C Tutor — Student Quick-Start Guide

Welcome to the REVA C Programming Practice System. This guide gets you up and running in 5 minutes.

---

## Prerequisites

Install these tools before you start:

| Tool | Install command (Ubuntu/WSL) |
|---|---|
| GCC | `sudo apt install gcc` |
| cppcheck | `sudo apt install cppcheck` |
| jq | `sudo apt install jq` |
| Python 3 | `sudo apt install python3` |

Make all scripts executable (run once):
```bash
chmod +x scripts/*.sh
```

---

## Step 1 — Register Yourself (Once)

1. Open the Command Palette in VS Code (`Ctrl+Shift+P` on Windows/Linux or `Cmd+Shift+P` on macOS).
2. Select **Tasks: Run Task** and choose **`REVA: Register Student`**.
3. Follow the prompts at the top of your VS Code window to enter:
   - Your **Student ID** (e.g. `raj22cs045`)
   - Your **Full Name** (e.g. `Raj Kumar`)
   - Your **Section** (e.g. `BTech-CS-2B`)

This registers you in the system and creates `student_data/progress/raj22cs045.json` to track your learning progress.

---

## Step 2 — Get Your Assigned Exercise

1. Open the Command Palette (`Ctrl+Shift+P`).
2. Run task **`REVA: Next Exercise`**.
3. Enter your **Student ID** when prompted.

This automatically creates a new `.c` file inside the `student_data/` directory (e.g. `student_data/INTRO_L1_a_raj22cs045.c`) with your problem description and instructions embedded in comments at the top. Open this file in your editor to begin.

---

## Step 3 — Write Your Solution

1. Open the created `.c` file under the `student_data/` folder.
2. Implement your solution inside the file.
3. Be sure to check `docs/coding_style_guide.md` as code style and quality are graded from Day 1.

---

## Step 4 — Get Help (When Stuck)

1. Keep your exercise `.c` file open and active in the editor.
2. Open the Command Palette (`Ctrl+Shift+P`) and run task **`REVA: Get Help`**.
3. This task compiles, checks code style, and saves a help context block to `student_data/help_context.txt`.
4. In your Claude/agent chat window, attach the file `student_data/help_context.txt` (type `@help_context.txt` or click the `+` icon to select it) and ask for help.

The teaching assistant will ask you Socratic questions to help you trace and fix the issue yourself.

---

## Step 5 — Submit for Grading

1. Keep your exercise `.c` file open and active in the editor.
2. Open the Command Palette (`Ctrl+Shift+P`) and run task **`REVA: Grade My Code`**.
3. This task runs test cases and saves a grading context block to `student_data/grade_context.txt`.
4. In your chat window, attach `student_data/grade_context.txt` (using `@` or `+`) and ask the agent to grade your code.

The agent will assess your submission and return your score (out of 10) across five dimensions.

---

## Step 6 — Get Your Next Exercise

After scoring a passing grade (7/10 or higher), run the task **`REVA: Next Exercise`** again to get your next assignment.

---

## Running with VS Code Tasks

If you are using VS Code, you can run all the scripts directly through VS Code's built-in Task runner without using the terminal manually. This is the recommended workflow.

### How to Run a Task

1. Press `Ctrl+Shift+P` (Windows/Linux) or `Cmd+Shift+P` (macOS) to open the Command Palette.
2. Type `Tasks: Run Task` and press `Enter`.
3. Select the task you want to run from the dropdown list.

### Available Tasks

*   **`REVA: Register Student`**: Registers your profile. When run, VS Code will display prompts at the top of the window asking you to enter:
    1. Your **Student ID** (e.g., `raj22cs045`)
    2. Your **Full Name** (e.g., `Raj Kumar`)
    3. Your **Section** (e.g., `BTech-CS-2B`)
*   **`REVA: Next Exercise`**: Requests your next exercise. It will prompt you for your **Student ID** and automatically create the `.c` file template in the project root.
*   **`REVA: Get Help`**: Gathers compiler outputs, style checking results, and your code from the **currently active C file** in your editor, generating the help context block in the terminal panel.
*   **`REVA: Grade My Code`**: Compiles and runs tests against the **currently active C file**, producing the grading context block in the terminal panel.

> [!IMPORTANT]
> For **`REVA: Get Help`** and **`REVA: Grade My Code`** to work, you must have the exercise `.c` file open and active in your editor when you launch the task.

---

## The Tutor's Principles

The agent will **never**:
- Write code for you
- Tell you which line is wrong
- Give you the corrected version

It **will**:
- Ask you questions that lead you to the answer
- Provide analogies and partial traces
- Give you targeted feedback on your grade
- Tell you exactly which style rule you violated

This is intentional. You learn by figuring it out — the agent is your guide, not your ghostwriter.

---

## File Naming Convention

All exercise files must follow:
```
TOPIC_Ln_variant_studentid.c
```
Example: `LOOP_L2_a_raj22cs045.c`

If you rename a file incorrectly, the scripts will tell you what's wrong.

---

## Getting Help with the System

If `help.sh` fails with a tool error:
- Check that gcc, cppcheck, and jq are installed
- Run the script with `bash -x scripts/help.sh yourfile.c` for debug output
- Contact your instructor if a tool is unavailable on the lab machine

---

*REVA University | School of Computer Science and Engineering*
