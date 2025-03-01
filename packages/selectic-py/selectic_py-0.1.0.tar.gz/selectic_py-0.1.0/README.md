# selectic-py

Python bindings for the `selectic` Rust library, providing cross-platform access to user selections.

## Installation

```bash
pip install selectic
```

Or install from source:

```bash
git clone https://github.com/zibo-chen/selectic-py.git
cd selectic-py
pip install -e .
```

## Requirements

- Python 3.7+
- Rust compiler (for installation from source)
- [setuptools-rust](https://github.com/PyO3/setuptools-rust) (for installation from source)

## Usage

### Getting the Current Selection

```python
import selectic_py

try:
    # Get the currently selected text
    text = selectic_py.get_text()
    print(f"Selected text: {text}")
except Exception as e:
    print(f"Error getting text: {e}")
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details
