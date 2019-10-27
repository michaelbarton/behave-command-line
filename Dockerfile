FROM python:3.6
WORKDIR /usr/local/src/behave_command_line
ADD ./requirements ./requirements
RUN pip3 install -r  requirements/default.txt -r  requirements/dev.txt
ENTRYPOINT []