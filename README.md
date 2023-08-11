<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/jeertmans/varscope/main/static/logo_dark_transparent.png">
  <source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/jeertmans/varscope/main/static/logo_light_transparent.png">
  <img alt="VarScope Logo" height="256px" align="right" src="https://raw.githubusercontent.com/jeertmans/varscope/main/static/logo.png">
</picture>

# VarScope

[![Documentation][documentation-badge]][documentation-url]
[![codecov][codecov-badge]][codecov-url]

Ultra simple module for creating local scopes in Python.

## Installation

VarScope can be installed with `pip`:

```bash
pip install varscope
```

## Usage

```python
>>> from varscope import scope
>>>
>>> a = 1
>>> with scope():  # Everything defined after will only apply inside the scope
...     a = 2
...     b = 3
...
>>> a
1
>>> b  # Not defined, because outside of scope
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
NameError: name 'b' is not defined
>>>
>>> with scope() as s:  # We can choose to keep some variables
...     a = 2
...     b = 3
...     s.keep("b")
...
>>> b
3
>>> with scope("a"):  # We can also move variables inside scope
...     a = 2
...
>>> a  # Not defined, because outside of scope
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
NameError: name 'a' is not defined
>>>
>>> d = {}
>>> with scope():  # Scope can mutate object from outside
...     d["a"] = 1
...
>>> d["a"]
1
```

[documentation-badge]: https://img.shields.io/website?down_color=lightgrey&down_message=offline&label=documentation&up_color=green&up_message=online&url=https%3A%2F%2Feertmans.be%2Fvarscope%2F
[documentation-url]: https://eertmans.be/varscope/
[codecov-badge]: https://codecov.io/gh/jeertmans/varscope/branch/main/graph/badge.svg?token=1dJ1AKWMR5
[codecov-url]: https://codecov.io/gh/jeertmans/varscope
