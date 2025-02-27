# DDX-Python
Rust bindings and utils for use in Python

## decimal
Python bindings for `rust_decimal`. Supports comparison, addition, subtraction, multiplication, division, and remainder. Constructor only supports `str`.

Usage:
```
$ python
>>> from ddx_python.decimal import Decimal
>>> d1 = Decimal("8631989.747461568422879160")
>>> d2 = Decimal("12354.867325583148587639999525")
>>> d3 = Decimal("8644344.6147871515714668000000")
>>> d1+d2 == d3
True
>>> d1+d2
Decimal('8644344.614787151571466800000')
```
