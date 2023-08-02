# Pytest-retry-class


Pytest rerun/retry class if any test inside the class fails 

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)

>pytest retry failure 


https://test.pypi.org/project/pytest-retry-class/0.2/

## how to install 
```sh
pip install pytest-retry-class
```

## how to run with pytest
```sh
pytest --maxretry 2 --retry_on_exception "[AssertionError, DBError]" test.py

```
Where:
- `--maxretry` is the number of times to retry a failed test [default: 1]
- `--retry_on_exception` is a list of exceptions to retry on [default: all exceptions]

## how to run with pytest.ini
You can also set the retry count and exceptions in pytest.ini file
```text
[pytest]
max_retry = 2
retry_on_exception = AssertionError
                     DBError
```
Warning: CMD line arguments will override the pytest.ini file.
## how to run examples 

```sh
1. **[pytest-xdist](example/pytest-dependency-support/tests)**
```sh
pytest example/pytest-xdist-support/tests
```
2. **[pytest-dependency](example/pytest-xdist-support/tests)**
```
pytest example/pytest-dependency-support/tests
```
3. **[pytest-rerun-class](example/rerun-class/tests)**
```
pytest example/rerun-class/tests
```
