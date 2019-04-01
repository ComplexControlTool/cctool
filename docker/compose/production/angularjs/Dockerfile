FROM node:6.12.0-alpine

MAINTAINER Nicholas Elia <me@nichelia.com>

# Environment variables
ENV REFRESHED_AT 2018-11-11
ENV DEV_DIR="/Developer"
ENV CODE_DIR="${DEV_DIR}/cctool"
ENV FRONTEND_CODE_DIR="${CODE_DIR}/frontend/"
ENV SCRIPTS_CODE_DIR="${CODE_DIR}/scripts/"

# Set working directory
RUN mkdir -p $FRONTEND_CODE_DIR
RUN mkdir -p $SCRIPTS_CODE_DIR
WORKDIR $FRONTEND_CODE_DIR

# Install dependencies
RUN apk update \
  # Admin tools
  && apk add bash git vim

RUN npm install -g bower@1.8.4 gulp@3.9.1

# Copy needed files
COPY ./frontend $FRONTEND_CODE_DIR

COPY ./docker/logo "${SCRIPTS_CODE_DIR}/logo"
RUN sed -i 's/\r//' "${SCRIPTS_CODE_DIR}/logo"
RUN chmod +x "${SCRIPTS_CODE_DIR}/logo"

COPY ./docker/compose/production/angularjs/start "${SCRIPTS_CODE_DIR}/start"
RUN sed -i 's/\r//' "${SCRIPTS_CODE_DIR}/start"
RUN chmod +x "${SCRIPTS_CODE_DIR}/start"

# Install node + bower packages
RUN cd $FRONTEND_CODE_DIR && \
    npm install && \
    bower install --config.interactive=false --allow-root
