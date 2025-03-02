# Ibhax - The Ultimate Decorator Toolkit

[![PyPI](https://img.shields.io/pypi/v/ibhax.svg)](https://pypi.org/project/ibhax/)
[![Python Version](https://img.shields.io/pypi/pyversions/ibhax.svg)](https://pypi.org/project/ibhax/)
[![License](https://img.shields.io/pypi/l/ibhax.svg)](https://opensource.org/licenses/MIT)

`ibhax` is a powerful and versatile Python library that provides **100 production-grade decorators** to enhance your development workflow. It includes decorators for **logging, debugging, caching, performance monitoring, security, error handling, and much more**.

## Features

✅ **100+ Ready-to-Use Decorators**  
✅ **Production-Grade Implementation**  
✅ **Performance & Debugging Tools**  
✅ **Error Handling & Security Enhancements**  
✅ **Logging & Monitoring Support**  
✅ **Simple and Flexible API**  

## Installation

Install `ibhax` using pip:

```bash
pip install ibhax
```

## Quickstart

Import `DecoratorFactory` and start using decorators right away:

```python
from ibhax.decorators import DecoratorFactory

factory = DecoratorFactory()

@factory.deprecated("Use `new_function()` instead.")
def old_function():
    print("This function is deprecated.")

old_function()
```

### Example Output:
```
============================================================
                  DEPRECATION NOTICE                     
Function       : old_function
Location       : example.py:8
Reason         : Use `new_function()` instead.
Recommendation : Please update your code accordingly.
============================================================
This function is deprecated.
```

---

## Available Decorators (Highlights)

The `DecoratorFactory` class provides **100 powerful decorators**. Here are a few:

| Decorator Name          | Description |
|-------------------------|------------|
| `@factory.deprecated`   | Marks a function as deprecated with a custom warning. |
| `@factory.log_execution_time` | Logs the execution time of a function. |
| `@factory.retry`        | Retries a function multiple times if it fails. |
| `@factory.suppress_errors` | Suppresses and logs exceptions instead of breaking the program. |
| `@factory.cache_results` | Caches function results to improve performance. |
| `@factory.debug`        | Logs function calls and arguments for debugging. |
| `@factory.thread_safe`  | Ensures a function is thread-safe. |
| `@factory.rate_limit`   | Limits the rate at which a function can be called. |
| `@factory.trace`        | Traces execution step-by-step for debugging. |
| `@factory.timeout`      | Sets a time limit on function execution. |

---

## Usage Examples

### 1. Logging Execution Time

```python
@factory.log_execution_time
def slow_function():
    import time
    time.sleep(2)
    print("Finished")

slow_function()
```
**Output:**
```
Execution time of slow_function: 2.0000 seconds
Finished
```

---

### 2. Retrying a Function on Failure

```python
@factory.retry(attempts=3, delay=1)
def unstable_function():
    import random
    if random.random() < 0.7:
        raise ValueError("Random failure!")
    print("Success!")

unstable_function()
```

---

### 3. Suppressing Errors

```python
@factory.suppress_errors(default="Error occurred!")
def risky_function():
    raise ValueError("Oops!")

print(risky_function())  # Output: Error occurred!
```

---

### 4. Debugging Function Calls

```python
@factory.debug
def add(a, b):
    return a + b

add(2, 3)
```
**Output:**
```
DEBUG: add called with args: (2, 3), kwargs: {}
DEBUG: add returned 5
```

---

### 5. Rate Limiting Function Calls

```python
@factory.rate_limit(calls=2, period=5)
def limited_function():
    print("Executed")

limited_function()
limited_function()
limited_function()  # This call may be blocked if made too soon.
```

---

### 6. Enforcing Thread Safety

```python
@factory.thread_safe
def safe_function():
    print("Thread-safe function running.")
```

---

### 7. Tracing Function Execution

```python
@factory.trace
def traced_function():
    x = 5
    y = x * 2
    return y

traced_function()
```

---

## Listing All Decorators

To see all available decorators with descriptions:

```python
factory.list_decorators()
```

---

## Contributing

We welcome contributions! Feel free to:

- Report issues
- Request new decorators
- Submit pull requests

Clone the repository and install the package in development mode:

```bash
git clone https://github.com/ibhax/decorator_factory.git
cd decorator_factory
pip install -e .
```

---

## License

`ibhax` is licensed under the MIT License.

---

## Links

- **PyPI:** [https://pypi.org/project/ibhax/](https://pypi.org/project/ibhax/)
- **GitHub:** [https://github.com/ibhax/decorator_factory](https://github.com/ibhax/decorator_factory)
