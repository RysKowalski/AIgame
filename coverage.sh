coverage run -m pytest
coverage html --omit tests/*.py
xdg-open htmlcov/index.html
