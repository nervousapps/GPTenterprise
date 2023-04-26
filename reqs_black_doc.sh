pip-compile ./python/setup.py -o ./python/requirements.txt
pip-compile ./python/requirements-tests.in -o ./python/requirements-tests.txt
pip-compile ./python/requirements-docs.in -o ./python/requirements-docs.txt
black ./
doctoc README.md