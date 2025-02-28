# Folder Reserved for the `duc` Python package.


## Install

1. **Build the package**:
```sh
python setup.py sdist bdist_wheel
```

2. **Install locally**:
```sh
pip install dist/duc_py-0.1.0-py3-none-any.whl
```

## Usage

```python

```

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