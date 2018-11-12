FROM python:3.7.0


ARG ENDPOINT_PORT

# Install build dependencies
RUN apt-get -qq update \
  && apt install -y netcat net-tools tcpdump \
  && pip3 install --upgrade pip \
  && mkdir -p /app

# Ensure that Python outputs everything that's printed inside
# the application rather than buffering it.
ENV PYTHONUNBUFFERED 1

ENV APP_PATH "/app"

WORKDIR /app
VOLUME ["/app"]

EXPOSE $ENDPOINT_PORT/udp

ENTRYPOINT ["/bin/bash", "/app/run.sh"]
