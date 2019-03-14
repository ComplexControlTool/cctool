FROM python:3.6-alpine

MAINTAINER Nicholas Elia <me@nichelia.com>

# Environment variables
ENV REFRESHED_AT 2018-11-11
ENV PYTHONUNBUFFERED 1
ENV DEV_DIR="/Developer"
ENV CODE_DIR="${DEV_DIR}/cctool"
ENV BACKEND_CODE_DIR="${CODE_DIR}/backend/"
ENV SCRIPTS_CODE_DIR="${CODE_DIR}/scripts/"
ENV CELERY_CODE_DIR="${CODE_DIR}/celery/"

# Set working directory
RUN mkdir -p $BACKEND_CODE_DIR
RUN mkdir -p $SCRIPTS_CODE_DIR
RUN mkdir -p $CELERY_CODE_DIR
WORKDIR $BACKEND_CODE_DIR

# Install dependencies
RUN apk update \
  # psycopg2 dependencies
  && apk add --virtual build-deps gcc python3-dev musl-dev \
  && apk add postgresql-dev \
  # Pillow dependencies
  && apk add jpeg-dev zlib-dev freetype-dev lcms2-dev openjpeg-dev tiff-dev tk-dev tcl-dev \
  # CFFI dependencies
  && apk add libffi-dev py-cffi \
  # Translations dependencies
  && apk add gettext \
  # https://docs.djangoproject.com/en/dev/ref/django-admin/#dbshell
  && apk add postgresql-client \
  # Graph dependencies
  && apk add graphviz \
  # Admin tools
  && apk add bash git vim

# Copy needed files
COPY ./backend/requirements "${SCRIPTS_CODE_DIR}/requirements"
RUN pip install -r "${SCRIPTS_CODE_DIR}/requirements/local.txt"

COPY ./docker/logo "${SCRIPTS_CODE_DIR}/logo"
RUN sed -i 's/\r//' "${SCRIPTS_CODE_DIR}/logo"
RUN chmod +x "${SCRIPTS_CODE_DIR}/logo"

COPY ./docker/compose/local/django/entrypoint "${SCRIPTS_CODE_DIR}/entrypoint"
RUN sed -i 's/\r//' "${SCRIPTS_CODE_DIR}/entrypoint"
RUN chmod +x "${SCRIPTS_CODE_DIR}/entrypoint"

COPY ./docker/compose/local/django/start "${SCRIPTS_CODE_DIR}/start"
RUN sed -i 's/\r//' "${SCRIPTS_CODE_DIR}/start"
RUN chmod +x "${SCRIPTS_CODE_DIR}/start"

COPY ./docker/compose/local/django/celery/worker/start "${SCRIPTS_CODE_DIR}/start-celeryworker"
RUN sed -i 's/\r//' "${SCRIPTS_CODE_DIR}/start-celeryworker"
RUN chmod +x "${SCRIPTS_CODE_DIR}/start-celeryworker"

COPY ./docker/compose/local/django/celery/beat/start "${SCRIPTS_CODE_DIR}/start-celerybeat"
RUN sed -i 's/\r//' "${SCRIPTS_CODE_DIR}/start-celerybeat"
RUN chmod +x "${SCRIPTS_CODE_DIR}/start-celerybeat"

COPY ./docker/compose/local/django/celery/flower/start "${SCRIPTS_CODE_DIR}/start-flower"
RUN sed -i 's/\r//' "${SCRIPTS_CODE_DIR}/start-flower"
RUN chmod +x "${SCRIPTS_CODE_DIR}/start-flower"


ENTRYPOINT ["/Developer/cctool/scripts/entrypoint"]
