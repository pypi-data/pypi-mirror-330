# doit-sqlite-sync

A SQLite backend for [doit](https://pydoit.org/) that keeps the database file synchronized with doit's state.

## Description

`doit-sqlite-sync` provides a SQLite backend that ensures immediate synchronization between doit's state and the database file on disk. Unlike the default SQLite backend, which only saves changes when closing the connection, this backend commits changes as they occur. This is especially appropriate for long-running tasks, which allows to monitor the progress of the execution in real-time.

## Installation

```bash
pip install doit-sqlite-sync
```

## Usage

To use this backend with doit, set the `--backend` flag in the doit command:

```bash
doit run -f dodo.py --backend=sqlite3sync
```

Alternatively, you can specify it directly in your `dodo.py` file:

```python
DOIT_CONFIG = {'backend': 'sqlite3sync'}
```

## Requirements

- Python >= 3.8
- doit >= 0.36.0
- cloudpickle >= 3.1.1

## License

This project is licensed under the CeCILL-B License - see the `LICENSE` file for details.