FROM python:3.5
WORKDIR /usr/local/src/behave_command_line
ADD ./requirements.txt .
RUN pip3 install -rrequirements.txt