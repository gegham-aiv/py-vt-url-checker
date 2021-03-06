# Python VirusTotal URL Checker

## Usage

To run the program, run the following command:

```shell
py main.py <sources_dir> <limit>
```

- `sources_dir` is the relevant path to the list of files containing the hostnames
- `limit` is the number of entities / hostnames to scan

You can also pass `verbose` option to the command. e.g.

```shell
py main.py --verbose
```

or

```shell
py main.py -V
```

## Installation

This project uses the following 3rd party libraries, so make sure to install them:

- slugify
- requests

```shell
pip install slugify
pip install requests
```