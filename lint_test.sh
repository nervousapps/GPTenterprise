pytest --color=yes --cov=./ --cov-report=term --cov-report=html
pylint $(git ls-files '*.py')