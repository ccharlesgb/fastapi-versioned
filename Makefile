.PHONY: test
test:
	pytest --cov=fastapi_versioned -s

test-pdb:
	pytest --cov=fastapi_versioned --pdb

