# displayhooks

[![Downloads](https://static.pepy.tech/badge/displayhooks/month)](https://pepy.tech/project/displayhooks)
[![Downloads](https://static.pepy.tech/badge/displayhooks)](https://pepy.tech/project/displayhooks)
[![codecov](https://codecov.io/gh/pomponchik/displayhooks/graph/badge.svg?token=UXXTj1AIcT)](https://codecov.io/gh/pomponchik/displayhooks)
[![Lines of code](https://sloc.xyz/github/pomponchik/displayhooks/?category=code)](https://github.com/boyter/scc/)
[![Hits-of-Code](https://hitsofcode.com/github/pomponchik/displayhooks?branch=main)](https://hitsofcode.com/github/pomponchik/displayhooks/view?branch=main)
[![Test-Package](https://github.com/pomponchik/displayhooks/actions/workflows/tests_and_coverage.yml/badge.svg)](https://github.com/pomponchik/metronomes/actions/workflows/tests_and_coverage.yml)
[![Python versions](https://img.shields.io/pypi/pyversions/displayhooks.svg)](https://pypi.python.org/pypi/displayhooks)
[![PyPI version](https://badge.fury.io/py/displayhooks.svg)](https://badge.fury.io/py/displayhooks)
[![Checked with mypy](http://www.mypy-lang.org/static/mypy_badge.svg)](http://mypy-lang.org/)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)


It's a micro library for manipulating [`sys.displayhook`](https://docs.python.org/3/library/sys.html#sys.displayhook).

When you need to change the standard behavior of `displayhook`, with this library you will do it:

- declaratively
- compactly
- beautifully


## Table of contents

- [**Quick start**](#quick-start)
- [**Change the displayed value**](#change-the-displayed-value)
- [**Prohibiting the display of certain types of values**](#prohibiting-the-display-of-certain-types-of-values)
- [**Automatic recovery of the default hook**](#automatic-recovery-of-the-default-hook)


## Quick start

Install it:

```bash
pip install displayhooks
```

And use:

```python
import sys
from displayhooks import not_display

not_display(int)

sys.displayhook('Most of the adventures recorded in this book really occurred; one or two were experiences of my own, the rest those of boys who were schoolmates of mine.')
#> 'Most of the adventures recorded in this book really occurred; one or two were experiences of my own, the rest those of boys who were schoolmates of mine.'
sys.displayhook(666)
# [nothing!]
```

## Change the displayed value

You can declaratively declare a converter function for the printed values. What it returns will be used to call the original `displayhook` function.

```python
import sys
from displayhooks import converted_displayhook

@converted_displayhook
def new_displayhook(value):
    return value.lower()

sys.displayhook("What’s gone with that boy, I wonder? You TOM!")
#> 'what’s gone with that boy, i wonder? you tom!'
```

If your function returns `None`, nothing will be printed.


## Prohibiting the display of certain types of values

You can disable the display of certain data types, similar to how [`NoneType`](https://docs.python.org/3/library/types.html#types.NoneType) values are ignored by default.

You could already see a similar example above, let's look at it again:

```python
import sys
from types import FunctionType
from displayhooks import not_display

not_display(FunctionType)

sys.displayhook('Nothing! Look at your hands. And look at your mouth. What is that truck?')
#> 'Nothing! Look at your hands. And look at your mouth. What is that truck?'
sys.displayhook(lambda x: x)
# [nothing!]
```

In this example, you can see that we have disabled the display for functions, but all other data types are displayed unchanged.


## Automatic recovery of the default hook

You can limit the impact on [`sys.displayhook`](https://docs.python.org/3/library/sys.html#sys.displayhook) only to the code inside a function. If you hang the `autorestore_displayhook` decorator on it, after exiting the function, the displayhook that was installed before it was called will be automatically restored:

```python
import sys
from types import FunctionType
from displayhooks import not_display, autorestore_displayhook

@autorestore_displayhook
def do_something_dangerous():
    not_display(FunctionType)
    sys.displayhook(do_something_dangerous)
    # [nothing!]

do_something_dangerous()

sys.displayhook(do_something_dangerous)
#> <function do_something_dangerous at 0x104c980e0>
```
