# To deploy steps
1. python3 -m pip install build
2. python3 -m build --sdist
3. python3 -m build --wheel
4. python3 -m twine upload dist/*
