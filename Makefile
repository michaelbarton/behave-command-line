DOCKER = docker-compose run --rm build_image
SRC = $(shell find . -name "*.py")

all: test build

test: fmt_check type_check unit_test lint

unit_test:
	@$(DOCKER) pytest

type_check:
	@$(DOCKER) mypy behave_command_line

lint:
	@$(DOCKER) pylint behave_command_line tests --rcfile=.pylintrc

fmt:
	@$(DOCKER) black --line-length 100 $(SRC)

fmt_check:
	@$(DOCKER) black --check --line-length 100 $(SRC)

build: $(SRC) setup.cfg requirements.txt Dockerfile
	$(DOCKER) python3 setup.py sdist bdist

# Create a local environment with depdendencies
.venv:
	python3 -m venv $@
	$@/bin/pip3 install -r  requirements/default.txt -r  requirements/dev.txt
