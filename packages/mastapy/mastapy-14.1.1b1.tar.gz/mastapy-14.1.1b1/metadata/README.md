<h1 align="center">
<img src="https://documentation.smartmt.com/MastaAPI/14.1.1/images/smt_logo.png" width="150" alt="SMT"><br>
<img src="https://documentation.smartmt.com/MastaAPI/14.1.1/images/MASTA_14_logo.png" width="400" alt="Mastapy">
</h1><br>

[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff) [![Poetry](https://img.shields.io/endpoint?url=https://python-poetry.org/badge/v0.json)](https://python-poetry.org/) [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Mastapy is the Python scripting API for MASTA.

- **Website**: https://www.smartmt.com/
- **Support**: https://support.smartmt.com/
- **Documentation**: https://documentation.smartmt.com/MastaAPI/14.1.1/


### Features

- Powerful integration with MASTA with the ability to run Python scripts from the MASTA interface directly.
- Ability to use MASTA functionality external to the MASTA software in an independent script.
- An up-to-date and tight integration with Python. This is not a lightweight wrapper around the C# API. It is specifically designed for Python and works great in tandem with other common scientific Python packages (e.g. SciPy, NumPy, Pandas, Matplotlib, Seaborn, etc.)
- Extensive backwards compatibility support. Scripts written in older versions of mastapy will still work with new versions of MASTA.
- Full support for Linux and .NET 6 versions of the MASTA API.

### Release Information

#### Major Changes

- Added support for Python 3.13.
- Dropped support for Python 3.7.
- Added support for `ListWithSelectedItem` in scripted properties.

#### Minor Changes

- Replaced `ptvsd` with `debugpy` as a dependency for Python 3.13 onwards. MASTA will now choose `debugpy` over `ptvsd` for debugging if it is available.
- Removed the `start_debugging` method and `DebugEnvironment` enum.
- Replaced the `Range` type with `tuple[float, float]`.
- Replaced the `IntegerRange` type with `tuple[int, int]`.
- Various improvements and bug fixes.

#### List With Selected Items

This release includes a new `ListWithSelectedItem` type that can be used to add drop down menus to your custom editors in MASTA. It supports a variety of basic types (`bool`, `float`, `int`, `str` and `complex`) as well as API types (e.g. `Design`.)

The easiest way of creating a list with selected item scripted property is to specify the return type as a `ListWithSelectedItem`.

```python
from mastapy import masta_property, ListWithSelectedItem

@masta_property(...)
def my_property(...) -> ListWithSelectedItem:
    return 5.0
```

If the return type of a scripted property is `ListWithSelectedItem` then the returned value will be automatically promoted to a list with selected item.

To get correct typing information, you can use one of the built-in types. The following example demonstrates this for a `float`:

```python
@my_property.setter
def my_property(..., value: ListWithSelectedItem.Float) -> None:
    ...
```

To populate the drop-down list with values, you will need to instantiate one of the available list with selected item types yourself.

```python
from mastapy import masta_property, ListWithSelectedItem

@masta_property(...)
def my_property(...) -> ListWithSelectedItem.Float:
    return ListWithSelectedItem.Float(5.0, [1.0, 2.0, 3.0, 4.0])
```

You cannot instantiate `ListWithSelectedItem` directly. If your selected value (`5.0` in this example) is not in the list of available values, it will be automatically appended.

To get typing information for a list with selected item API type, you need to create a class stub that subclasses both your API type and `ListWithSelectedItem`. The following example shows how to do this for a `Design` list with selected item:

```python
class ListWithSelectedItemDatum(Design, ListWithSelectedItem):
    pass

@my_property.setter
def my_property(..., value: ListWithSelectedItemDesign) -> None:
    ...
```

You can also instantiate your custom type.

```python
from mastapy import masta_property, ListWithSelectedItem

class ListWithSelectedItemDatum(Design, ListWithSelectedItem):
    pass

@masta_property(...)
def my_property(...) -> ListWithSelectedItemDesign:
    ...
    return ListWithSelectedItemDesign(design0, [design1, design2])
```