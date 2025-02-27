# nc_utils

nCompass Library

A Python library providing immutable objects and traits for building robust applications.

## Installation:
```
pip install ncompasslib
```

## Basic Usage:

### 1. Creating an Immutable Object:
The Immutable class prevents attributes from being modified after they are first set.

```
from ncompasslib.immutable import Immutable

class MyClass(Immutable):
    def __init__(self):
        super().__init__()
        self.value = 42

obj = MyClass()
obj.value  # Returns 42
obj.value = 43  # Raises RuntimeError: Cannot change state once created
```

### 2. Using the Mutate Decorator:
When you need to modify an immutable object in a controlled way, use the mutate decorator.

```
from ncompasslib.immutable import Immutable, mutate

class Counter(Immutable):
    def __init__(self):
        super().__init__()
        self.count = 0
        
    @mutate
    def increment(self):
        self.count += 1
```

### 3. Creating Traits:
Traits are abstract base classes that are also immutable.

```
from ncompasslib.trait import Trait

class MyTrait(Trait):
    def __init__(self):
        super().__init__()
        self.trait_value = "example"
```

## Features:
- Immutable objects with controlled mutation
- Trait system for creating abstract interfaces
- Python 3.11+ support
- Comprehensive test suite

For more information, visit:
https://github.com/nCompass-tech/ncompasslib
