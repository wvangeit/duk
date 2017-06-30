install:
	pip install .
clean:
	rm -rf dist
	rm -rf build
	rm -rf duk.egg-info
test: install
	pip install nose --upgrade
	nosetests
	duk
push: clean install
	git push
	git push --tags
