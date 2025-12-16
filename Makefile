PYTHONPATH := ./src

test:
	@PYTHONPATH=$(PYTHONPATH) pytest -v

unit_test:
	@PYTHONPATH=$(PYTHONPATH) pytest -v -m "not slow"

perf_test:
	@PYTHONPATH=$(PYTHONPATH) pytest -v -s -m "slow"

coverage:
	@PYTHONPATH=$(PYTHONPATH) coverage run -m pytest
	@PYTHONPATH=$(PYTHONPATH) coverage report

lint:
	@PYTHONPATH=$(PYTHONPATH) ruff check src/

doc:
	@PYTHONPATH=$(PYTHONPATH) pdoc3 --html --force --output docs src/triangulator