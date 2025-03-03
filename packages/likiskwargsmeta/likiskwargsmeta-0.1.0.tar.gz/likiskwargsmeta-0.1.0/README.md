# KwargsMeta

KwargsMeta is a Python package that provides a metaclass to automatically handle keyword arguments (`kwargs`) from methods. This metaclass allows you to set values of keyword arguments from methods in the `__init__` method without explicitly specifying them, making your code cleaner and more maintainable.

## Features

- Automatically injects keyword arguments into the `__init__` method.
- Simplifies the initialization of classes with many keyword arguments.
- Reduces boilerplate code.
- Allows to set keyword arguments from methods in the `__init__` method.

## Installation

You can install KwargsMeta using pip:

```sh
pip install likiskwargsmeta
```

## Usage

Here is an example of how to use KwargsMeta:

```py
from likiskwargsmeta import KwargsMeta

class MyClass(metaclass = KwargsMeta):
    def __init__(self, a, b = 12):
        self.a = a
        self.b = b
    
    def method1(self, b = 3, c = 12):
        print(f"{b = }, {c = }")

MyClass(1).method1() # will print b = 12, c = 12
MyClass(12, b = 3).method1(c = 1) # will print b = 3, c = 1
MyClass(1, b = None).method1() # will print b = 3, c = 12
```

## License
This project is licensed under the MIT License. See the LICENSE file for details.

## Contributing
Contributions are welcome! Please open an issue or submit a pull request on GitHub.