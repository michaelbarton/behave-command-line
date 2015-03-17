build := dist/behave_command_line-$(shell cat VERSION).tar.gz

deploy: $(build)
	curl \
	  --form package=@$< \
	  'https://8w9pcGeJPCmAGrxTL_Ze@push.fury.io/michaelbarton/'

$(build): $(shell find more_assertive_nose) requirements.txt
	python setup.py sdist
