# nocamel
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Coverage Status](https://coveralls.io/repos/github/jchar32/nocamel/badge.svg?branch=main&kill_cache=1)](https://coveralls.io/github/jchar32/nocamel?branch=main)

A simple command-line utility to convert camelCase or PascalCase strings to other more acceptable formats.

## Description

`nocamel` is a Python-based CLI tool that aims to kill the camel case. Are there other ways to do this? **Yes**. Did I learn something while making it? **Also Yes**.

## Installation

### From PyPI

```bash
pip install nocamel
```

### From Source

```bash
git clone https://github.com/jchar32/nocamel.git
cd nocamel
pip install -e .
```
Verify installation:
```python
import nocamel
print(nocamel.__version__)
```

## Usage

### Command Line Interface

Basic usage:

```bash
nocamel "Your Camel Case String"
```

This will output: `Your camel case string`

### Options
Convert from camel or pascal case to...
- `-snake`: to snake case "like_this"
- `--sentence (default)`: to sentence case and inject spaces "Like this"
- `--lower`: to all lower case "like this" or "likethis"
- `-h, --help`: Show the help message

### Examples

Convert camelCase to lower case:
```bash
$ nocamel "helloWorldExample"
helloworldexample
```

Convert to kebab-case:
```bash
$ nocamel "Hello World Example" --kebab
hello-world-example
```

Convert to snake_case:
```bash
$ nocamel "hello World Example" --snake
hello_world_example
```
Convert sentence case:
```bash
$ nocamel "hello World Example" --sentence
Hello world example
```

### As a Python Module

You can also use `nocamel` as a Python module in your projects:

```python
from nocamel import converters

result = converters.to_snake("helloWorldExample")
print(result)  # Output: hello_world_example

result_kebab = converters.to_kebob("Hello World Example")
print(result_kebab)  # Output: hello-world-example
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.