pip-compile ./python/pyproject.toml -o ./python/requirements.txt
pip-compile --extra test ./python/pyproject.toml -o ./python/requirements-tests.txt
pip-compile --extra doc ./python/pyproject.toml -o ./python/requirements-docs.txt
black ./
doctoc README.md