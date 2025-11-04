PYTHONPATH := ./src

test:
	@PYTHONPATH=$(PYTHONPATH) pytest -v