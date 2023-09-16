.PHONY: help setup dev

help: ## Show this help
	@grep -E '^[a-zA-Z/._-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'

dev: ## Run a local webserver
	 python3 -m http.server -d docs

demo/raylib.wasm: ## Build the raylib wasm from C
	docker run -it --rm -v $$(pwd):/src -v /tmp/emscripten-cache:/emsdk/upstream/emscripten/cache/ -u $$(id -u):$$(id -g) emscripten/emsdk ./tools/build.sh

clean: ## Delete built files
	rm -f demo/raylib.js demo/raylib.wasm

