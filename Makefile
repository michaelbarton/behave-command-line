version := $(shell python setup.py --version)
build   := dist/behave_command_line-$(version).tar.gz

build: $(build)

$(build): $(shell find behave_command_line) requirements.txt
	python setup.py sdist
