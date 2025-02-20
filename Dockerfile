# Select a minimal base image with Python 3.11 (adjust if needed)
FROM python:3.12-slim
MAINTAINER Narasimhan M.G. github.com/Naras
COPY ./app /usr/local/upanishad/app
COPY ./static /usr/local/upanishad/static
COPY ./tests /usr/local/upanishad/tests
COPY ./env-production /usr/local/upanishad/.env
COPY ./requirements.txt /usr/local/upanishad/requirements.txt
EXPOSE 8000
WORKDIR /usr/local/upanishad/
RUN pip3 install -r requirements.txt
CMD fastapi run
