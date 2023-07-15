.PHONY: help setup dev

help:
	@grep -E '^[a-zA-Z._-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

setup: ## Install dependencies and stuff
	pip3 install -r requirements.txt

dev: ## run a local webserver
	httpwatcher

raylib.wasm: ## build the raylib wasm from C
	docker run -it --rm -v $$(pwd):/src -v /tmp/emscripten-cache:/emsdk/upstream/emscripten/cache/ -u $$(id -u):$$(id -g) emscripten/emsdk ./tools/build.sh
