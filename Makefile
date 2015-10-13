install:
	pip install .
clean:
	rm -rf build
test:
	pip install .
	pip install nose --upgrade
	nosetests
push: clean install
	git push
	git push --tags
