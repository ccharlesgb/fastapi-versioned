.PHONY: test
test:
	pytest --cov=fastapi_versioned -s

.PHONY: test-pdb
test-pdb:
	pytest --cov=fastapi_versioned --pdb

.PHONY: run-example
run-example:
	python ./example/run.py