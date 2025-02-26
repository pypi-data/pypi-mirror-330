# Deep-Dummy-Maths

A dummy library for mathematical functions created by Deependu Jha.

## Installation

```bash
pip install deep-dummy-maths
```

## Usage

```python
from deep_dummy_maths import my_sum, my_diff, my_pro, my_div, my_factorial, hello_from_bin

my_sum(1, 2)  # Output: 3
my_diff(1, 2)  # Output: -1
my_pro(1, 2)  # Output: 0.5
my_div(1, 2)  # Output: 0.5
my_factorial(10)  # Output: 120
hello_from_bin()
```

---

## For future reference

### Using **Poetry** with `src/`

https://browniebroke.com/blog/convert-existing-poetry-to-src-layout/

```toml
[tool.poetry]
# ... other metata
packages = [
     { include = "my_package" },
     { include = "my_package", from = "src" },
  ]



[tool.pytest.ini_options]
pythonpath = ["src"]
```
