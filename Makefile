DOCKER = docker-compose run --rm build_image
SRC = $(shell find . -name "*.py")

all: test build

test: fmt_check type_check lint

type_check:
	@$(DOCKER) mypy behave_command_line

lint:
	@$(DOCKER) pylint behave_command_line --rcfile=.pylintrc

fmt:
	@$(DOCKER) black --line-length 100 $(SRC)

fmt_check:
	@$(DOCKER) black --check --line-length 100 $(SRC)

build: $(SRC) setup.cfg requirements.txt Dockerfile
	$(DOCKER) python3 setup.py sdist bdist
