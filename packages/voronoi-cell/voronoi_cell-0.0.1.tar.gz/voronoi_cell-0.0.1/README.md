

To intsall this package

For this we run
```bash
python3 -m venv myenv
source myenv/bin/activate
pip install -i https://test.pypi.org/simple/voronoi_cell
python3 -m pip install --upgrade build
python3 -m build
python3 -m twine upload --repository testpypi dist/*
```

To install and test the example package
```bash
```
