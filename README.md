<p align="center">
    <img src="https://raw.githubusercontent.com/exler/verdandi/main/docs/logo.png" width="192">
</p>
<p align="center">
    Class-based benchmarking framework with <code>unittest</code>-style behavior 
</p>
<p align="center">
    <img src="https://github.com/exler/verdandi/actions/workflows/quality.yml/badge.svg">
</p>

## Overview

Verdandi is a small library providing class-based benchmarking functionality with similar interface to Python's [unittest](https://docs.python.org/3/library/unittest.html).

## Requirements

* Python >= 3.6

## Installation
```
$ pip install verdandi
```

## Usage

Verdandi can be used as a command-line both by passing the files containing benchmarks as arguments or by using the discovery functionality:

```bash
# Specifying the files
$ verdandi tests.benchmarks.bench_module1 tests.benchmarks.bench_module2

# Running discovery
$ verdandi
```

## Credits

* [unittest](https://docs.python.org/3/library/unittest.html) - Verdandi is based on `unittest` and wouldn't exist without it!
* [pytest](https://docs.pytest.org/en/6.2.x/) - some improvements over the `unittest` library are inspired by `pytest` or its plugins!

## License

Copyright (c) 2021 by ***Kamil Marut***

`verdandi` is under the terms of the [MIT License](https://www.tldrlegal.com/l/mit), following all clarifications stated in the [license file](LICENSE).
