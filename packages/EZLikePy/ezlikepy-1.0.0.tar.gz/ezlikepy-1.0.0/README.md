# EZLikePy

**Makes Python EZ**  

EZLikePy is a simple Python package that simplifies working with lists and execution time measurement.

## Features
- **EListz**: Easily create, modify, and manage multiple lists.
- **eTime**: Measure execution time and introduce delays.

## Installation
```sh
pip install EZLikePy
```

## Usage

### Working with `EListz`
```python
from EZLikePy import EListz

lists = EListz()
lists.create("my_list")
lists.append("my_list", 10)
lists.insert("my_list", 0, 5)
print(EZLists["my_list"])  # Output: [5, 10]
```

### Using `eTime`
```python
from EZLikePy import eTime

timer = eTime()
timer.start()
# Your code here
timer.end()
print(timer.total(), "seconds elapsed")
```

## License
This project is licensed under the MIT License.

---
Developed by **Roshan D Roy** 🚀
