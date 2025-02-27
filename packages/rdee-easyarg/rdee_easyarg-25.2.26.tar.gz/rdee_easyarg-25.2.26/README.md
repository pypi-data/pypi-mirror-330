# rdee-python-easyarg

+ This package is primarily designed to automatically generate command-line interfaces for functions.
+ Inspired by typer and fire, they aim to achieve comprehensive functionality but requires the insertion of specific code snippets into the codebase.
+ This project intends to generate command-line interfaces for functions without intruding into the function code (using the decorator pattern) or even the entire script (using the `pyfexe` executable).
+ The trade-off is that all function parameters must have type annotations, and at least one must be of a primitive type (float, int, str, or bool).

# Install

+ `pip install rdee-easyarg`

# Examples

## CLI-app mode

+ In this mode, we use a decorator to declare CLI interface

```python
import easyarg

ea = easyarg.EasyArg()

# @ea.command()
# @ea.command(desc="manual description rather than docstring")
@ea.command(name="func1", alias="f", defaults={"y": 3}, choicess={"x": (1,2,3)})
def f1(x: int, y: int, flag1: bool, flag2: bool = False):
    """


    :param x: this info will be read as argument description in -h, --help
    :param y: {3,4,5} the leading {...} will be parsed into choices if not specified
    """
    print(x+y)


if __name__ == "__main__":
    ea.parse()
```

+ You can run the script directly, such as `./a.py f1 --x 1 --y 2`, and get 3
+ `-h/--help` for app level and function level are both supported

## CLI-executor mode

+ In this mode, we can execute a function in CLI without INSERTING any code
+ For instance, given the `funcs.py`

```python
def add(x: int, y: int = 0) -> int:
    print(x + y)

def failfunc(x, y):
    pass

def mul(a: float, B: float, c: float = 1.0) -> float:
    print(a * B * c)
```

+ run `pyfexe funcs.py -h` to check valid functions to execute
+ then run `pyfexe funcs.py add -h` to check usage of target function
+ then run `pyfexe funcs.py add -x 1` execute the function "add", with `x=1, y=0`
