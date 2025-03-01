# duc_py

Python library for working with DUC (Ducflair Canvas) files.

## Installation

```bash
pip install duc_py
```

Or install from a local clone:

```bash
git clone https://github.com/your-username/duc_py.git
cd duc_py
pip install -e .
```

## Usage Examples

### Basic Import

```python
# Import duc_py
import duc_py as duc

# Create a point
point = duc.Point(x=10, y=20)

# Access modules directly
something = duc.classes.SomeClass()
result = duc.parse.parse_duc_element(...)
```

### Import Types Directly

```python
# Import specific types
from duc_py import Point, BezierHandle, ElementStroke

# Create and use them
point = Point(x=10, y=20)
```

### Access Module Functions

```python
# Import specific modules
from duc_py import parse, serialize, classes, utils

# Use functions from those modules
element = parse.parse_duc_element(...)
serialized = serialize.serialize_duc_element(...)
```

## Development

To set up for development:

```bash
# Clone the repository
git clone https://github.com/your-username/duc_py.git

# Change to the project directory
cd duc_py

# Install in development mode
pip install -e .
```

## VSCode Configuration

If you're using VSCode with Pylance and having issues with imports, add this to your `.vscode/settings.json`:

```json
{
    "python.analysis.extraPaths": [
        "${workspaceFolder}/venv/lib/python3.x/site-packages",
        "/path/to/duc_py/src"
    ],
    "python.analysis.typeCheckingMode": "basic",
    "python.autoComplete.extraPaths": [
        "${workspaceFolder}/venv/lib/python3.x/site-packages",
        "/path/to/duc_py/src"
    ]
}
```

## License

[Add your license information here]

## Test

```sh
# Add 100 random elements
python -m src.tests.add_100_rand_elements ./src/tests/inputs/input.duc -o ./src/tests/dist/output.duc
```

```sh
# Move elements randomly
python -m src.tests.move_elements_rand ./src/tests/inputs/input.duc -o ./src/tests/dist/output.duc --max-distance 1000 --max-rotation 3.14
```

```sh
# Print the duc file in a readable format
python -m src.tests.pretty_print_duc ./src/tests/inputs/input.duc
```

```sh
# Create a Duc with 100 connected elements
python -m src.tests.create_duc_with_100_connected -o ./src/tests/dist/output.duc
```

## Raw Inspect in JSON

```sh
flatc --json --strict-json --raw-binary --no-warnings -o ./src/tests/dist ../duc.fbs -- ./src/tests/dist/output.duc
```
