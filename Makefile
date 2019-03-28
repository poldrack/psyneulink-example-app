docker-build:
	docker build -t pnl-example .

run:
	docker run -i --rm -v ${PWD}:/example pnl-example -j /example/example.json -s /example/stimulus.tsv

shell:
	docker run -v ${PWD}:/example -it --entrypoint=bash pnl-example
