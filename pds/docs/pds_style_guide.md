## Python PDS Style Guide — P01 to P10
**REVA University | B25CS0102 Python for Data Science Lab**

All PDS lab submissions are automatically checked against these ten rules during grading. Violations deduct from the **Style (2 marks)** and **Documentation (1 mark)** rubric dimensions.

---

### P01 — Naming Conventions
Use `snake_case` for variables and functions. Use `UPPER_SNAKE_CASE` for constants.

```python
# ✅ Correct
def calculate_area(radius):
    PI = 3.14159
    return PI * radius ** 2

# ❌ Wrong
def CalculateArea(Radius):
    pi = 3.14159
    return pi * Radius ** 2
```

---

### P02 — No Magic Numbers
Assign meaningful names to all numeric literals (except 0 and 1 in obvious contexts).

```python
# ✅ Correct
BOILING_POINT_C = 100
FREEZING_POINT_C = 0

# ❌ Wrong
if temp > 100:  # What does 100 mean?
    print("boiling")
```

---

### P03 — Docstrings on Every Function
Every function must have a docstring explaining its purpose, arguments, and return value.

```python
# ✅ Correct
def celsius_to_fahrenheit(celsius):
    """
    Convert temperature from Celsius to Fahrenheit.

    Args:
        celsius (float): Temperature in degrees Celsius.

    Returns:
        float: Temperature in degrees Fahrenheit, rounded to 2 decimal places.
    """
    return round((celsius * 9 / 5) + 32, 2)

# ❌ Wrong
def celsius_to_fahrenheit(celsius):
    return round((celsius * 9 / 5) + 32, 2)
```

---

### P04 — No Bare `except:`
Always catch a specific exception. Bare `except:` silently swallows all errors.

```python
# ✅ Correct
try:
    result = int(user_input)
except ValueError:
    print("Please enter a valid integer.")

# ❌ Wrong
try:
    result = int(user_input)
except:           # catches SystemExit, KeyboardInterrupt, everything!
    print("Error")
```

---

### P05 — Use f-strings
Use f-strings for string formatting. Avoid `%` formatting and `.format()`.

```python
# ✅ Correct
name = "Arjun"
score = 8.5
print(f"Student: {name} | Score: {score}/10")

# ❌ Wrong
print("Student: %s | Score: %.1f/10" % (name, score))
print("Student: {} | Score: {}/10".format(name, score))
```

---

### P06 — No Hardcoded Answers
Your solution must work for **any** valid input, not just the sample provided.

```python
# ✅ Correct — works for any temperature
def celsius_to_fahrenheit(celsius):
    """Convert Celsius to Fahrenheit."""
    return round((celsius * 9 / 5) + 32, 2)

# ❌ Wrong — hardcoded for just one input
def celsius_to_fahrenheit(celsius):
    return 212.0   # only works when celsius == 100!
```

---

### P07 — No Wildcard Imports
Import only what you need. Wildcard imports pollute the namespace.

```python
# ✅ Correct
import numpy as np
from pandas import DataFrame

# ❌ Wrong
from numpy import *      # imports everything, including names that clash
from pandas import *
```

---

### P08 — One Operation Per Line
Do not chain multiple operations on a single line when it harms readability.

```python
# ✅ Correct
squared = [x ** 2 for x in numbers]
even_squares = [s for s in squared if s % 2 == 0]

# ❌ Wrong (hard to read and debug)
result = [x**2 for x in numbers if x**2 % 2 == 0]  # acceptable for simple cases
a = b = c = 0   # avoid chained assignment for different variables
```

---

### P09 — Use List Comprehensions (Where Appropriate)
Prefer list comprehensions over explicit loops for simple transformations.

```python
# ✅ Pythonic
squares = [x ** 2 for x in range(10)]
even_numbers = [n for n in data if n % 2 == 0]

# ❌ Verbose (acceptable for complex logic, not simple cases)
squares = []
for x in range(10):
    squares.append(x ** 2)
```

---

### P10 — 4-Space Indentation (No Tabs)
Use exactly 4 spaces per indentation level. Never mix tabs and spaces.

```python
# ✅ Correct
def my_function():
    if True:
        for i in range(10):
            print(i)

# ❌ Wrong (tab characters)
def my_function():
	if True:          # ← TAB here — causes IndentationError in mixed files
		print("bad")
```

---

## Grading Impact

| Violations | Style Score |
| :--- | :--- |
| 0 violations | 2/2 |
| 1–2 minor violations | 1/2 |
| 3+ violations OR P04/P06 violation | 0/2 |

Missing docstrings (P03): **−1 from Documentation dimension (separately)**

---

*REVA University | School of Computer Science and Engineering | AY 2025–26*
