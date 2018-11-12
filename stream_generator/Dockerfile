FROM python:3.7.0

# Install build dependencies
RUN apt-get -qq update \
  && apt install -y netcat net-tools tcpdump \
  && apt-get -y install debconf-utils \
  && pip3 install --upgrade pip \
  && mkdir -p /app

# Ensure that Python outputs everything that's printed inside
# the application rather than buffering it.
ENV PYTHONUNBUFFERED 1

ENV APP_PATH "/app"

WORKDIR /app
VOLUME ["/app"]


ENTRYPOINT ["/bin/bash", "/app/everlast.sh"]
