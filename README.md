# colabinput

A utility package for Google Colab that includes a custom input function.

## Installation

You can install this package using pip:

```bash
pip install git+https://github.com/raufoon/colabinput.git
```

## Usage

```python
from colabinput import coinput

inputs = coinput(description="Please provide your input:", input=dict(label="Enter something:", type="text"))
print(inputs)
```
