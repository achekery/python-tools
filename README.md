# python-tools

## Create `.venv` for poetry

```python
python -m venv .venv
poetry config --local virtualenvs.create true
poetry config --local virtualenvs.in-project true
```
