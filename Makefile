VERSION = 1.4.0

.PHONY: all clean test build

all: upload clean;

build:
	python setup.py sdist
	python setup.py bdist_wheel
	rm -rf build

upload: build
	twine upload dist/*${VERSION}*

install:
	pip install -e . --force-reinstall

test:
	python tests/test.py

clean:
	rm -rf *.egg-info .pytest_cache build