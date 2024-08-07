# colabinput

A utility package for Google Colab that includes a custom input function.

## Installation

You can install this package using pip:

```bash
pip install git+https://github.com/raufoon/colabinput.git
```

## Usage

```python
from colabinput import *

# Collect gender and age inputs
gender, age = coinput(
    gender=dict(
        label="Gender:",
        type="radio",
        options=["Male", "Female"]
    ),
    age=dict(
        label="Age:",
        type="number"
    )
)

# Collect name input
name = coinput(
    label="Name:",
    type="text"
)

# Collect a blank input (default input)
blank = coinput()

# Print provided values
print(f"Name: {repr(name)}, Gender: {repr(gender)}, Age: {repr(age)}, Blank Input: {repr(blank)} provided.")

# Alternative method to collect inputs
gender, age, name = (
    inputradio(
        label="Gender:<br> ",
        options=["Male" + "<br>", "Female"],
        checked=["Female"]
    ),
    inputnumber(
        label="Age:",
        step=0.5,
        value="20"
    ),
    inputselect(
        label="Name:",
        options=["Footu", "Batu"],
        selected="Batu"
    )
)

# Collect long text input
textlong = inputtextarea(
    label="Text:",
    value="Halle\nluija"
)

# Collect favorite colors input
colors = inputcheckbox(
    label="Favorite<br>Colors:",
    options=["Red", "Blue" + "<br>", "Green", "White" + "<br>", "Black"],
    checked=["Red", "Green"]
)

# Print provided values
print(f"Text: {textlong}, Gender: {gender}, Age: {age}, Favorite Colors: {colors} provided.")

```
