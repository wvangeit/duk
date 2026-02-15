install: .venv
	uv pip install .
clean:
	rm -rf dist
	rm -rf build
	rm -rf duk.egg-info
	rm -rf wheelhouse
	rm -rf duk/_version.py
dist: clean .venv
	uv build
install_dist: dist
	uv pip install --force-reinstall dist/duk-*.whl
test: install_dist
	uv pip install pytest
	uv run pytest
push: clean test
	git push
	git push --tags
.venv: .check-uv-installed
	@uv venv --clear $@

.check-uv-installed:
	@echo "Checking if 'uv' is installed..."
	@if ! command -v uv >/dev/null 2>&1; then \
			curl -LsSf https://astral.sh/uv/install.sh | sh; \
	else \
			printf "\033[32m'uv' is installed. Version: \033[0m"; \
			uv --version; \
	fi
	# upgrading uv
	-@uv self --quiet update

