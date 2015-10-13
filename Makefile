install:
	pip install .
clean:
	rm -rf dist
	rm -rf build
	rm -rf duk.egg-info
test:
	pip install .
	pip install nose --upgrade
	nosetests
push: clean install
	git push
	git push --tags
