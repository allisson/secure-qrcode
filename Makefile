.PHONY: test
test:
	poetry run pytest -v

.PHONY: lint
lint:
	poetry run pre-commit run --all-files

.PHONY: run-api
run-api:
	poetry run uvicorn secure_qrcode.api:app --reload

.PHONY: docker-build
docker-build:
	docker build --rm -t allisson/secure-qrcode .

.PHONY: docker-run
docker-run:
	docker run --rm -p 8000:8000 allisson/secure-qrcode
