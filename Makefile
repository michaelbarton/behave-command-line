DOCKER = docker-compose run build_image

all: build

build: $(shell find behave_command_line) requirements.txt Dockerfile
	$(DOCKER) python3 setup.py sdist
