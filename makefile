py_target=main

all: py clean

py:
	python $(py_target).py

clean:
	@rm -f *.pyc
