check: typecheck check_style

typecheck:
	pyright

check_style:
	black --check src

build: check
	python3 -m build

format:
	black src

clean:
	rm -rf dist
