format:
	black enelvo/ tests/

lint:
	python3 -m pylint enelvo/ tests/

test:
	pytest tests/

checklist: format lint test

.PHONY: format lint test checklist