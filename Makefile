docker-build:
	docker build -t pnl-example .

run:
	docker run -i --rm pnl-example

shell:
	docker run -v -it --entrypoint=bash pnl-example
