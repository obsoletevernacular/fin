PYTHON_SOURCES = tests/*.py report.py fin.py utils.py

test:
	py.test

coverage: .coverage

.coverage: $(PYTHON_SOURCES)
	py.test --cov=fin --cov=utils --cov=report

dev: venv 
	pip install -e .

venv: 
	. venv/bin/activate

.PHONY: test coverage init dev

