DOCKER = docker-compose run build_image

all: build

build: $(shell find behave_command_line) setup.py setup.cfg requirements.txt Dockerfile
	$(DOCKER) python3 setup.py sdist bdist
