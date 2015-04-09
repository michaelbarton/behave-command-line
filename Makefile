version := $(shell python setup.py --version)
build   := dist/behave_command_line-$(version).tar.gz

deploy: $(build)
	curl \
	  --form package=@$< \
	  'https://8w9pcGeJPCmAGrxTL_Ze@push.fury.io/michaelbarton/'

build: $(build)

$(build): $(shell find behave_command_line) requirements.txt
	python setup.py sdist
