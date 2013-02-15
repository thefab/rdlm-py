default: all

all:
	python setup.py build

install: all
	python setup.py install

clean:
	rm -f *.pyc
	cd tests && rm -f *.pyc
	cd rdlmpy && rm -f *.pyc
	cd tests && rm -Rf htmlcov 
	rm -Rf rdlm_py.egg-info
	rm -f .coverage tests/.coverage
	rm -f MANIFEST
	rm -Rf build
	rm -Rf dist
	rm -f *.rst
	rm -Rf rdlmpy.egg-info
	rm -Rf rdlmpy/__pycache__
	rm -Rf tests/__pycache__

sdist: clean
	python setup.py sdist

test:
	cd tests && nosetests

rst:
	cat README.md |pandoc --from=markdown --to=rst >README.rst

upload: rst
	python setup.py sdist register upload

coverage:
	cd tests && coverage run `which nosetests` && coverage html --include='*/rdlmpy/*' --omit='test_*'

release: test coverage clean upload clean 
