install:
	pip install .
clean:
	rm -rf dist
	rm -rf build
	rm -rf duk.egg-info
	rm -rf wheelhouse
wheel: clean
	pip wheel -w wheelhouse .
install_wheel: wheel
	pip install --force-reinstall wheelhouse/duk-*.whl
test: install_wheel
	pytest
push: clean test
	git push
	git push --tags
