# Pytest-retry-class


Pytest rerun/retry class if any test inside the class fails 

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)

>pytest retry failure 


https://pypi.org/project/pytest-retry-class/0.1/

## how to install 
```sh
pip install pytest-retry-class
```

## how to run with pytest
```sh
pytest --maxretry 2 test.py
```

## how to run examples 
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
