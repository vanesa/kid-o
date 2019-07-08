# Targets that are always out-of-date, and always re-run
.PHONY: install install_test clean black test static

install:
	pip install -r requirements-frozen.txt

install_test:
	pip install -r requirements-test.txt
	npm install -g less

clean:
	rm -r kido/__pycache__

black:
	black --check .

test: install_test
	python test.py

static:
	python -m jac.contrib.flask kido:app
