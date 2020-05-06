FROM python:3.7-alpine3.9
WORKDIR /app
RUN apk --update add --no-cache libjpeg \
                                jpeg-dev \
                                tiff-dev \
                                lcms2-dev \
                                libpq \
                                libwebp-dev \
                                libxml2-dev \
                                libxslt-dev \
                                postgresql-dev \
                                musl-dev \
                                gettext \
                                git \
                                gcc \
                                musl-dev \
                                zlib-dev \
                                tk-dev \
                                tcl-dev \
                                libffi-dev \
                                libmagic \
                                py-cffi \

COPY requirements.txt requirements.txt
RUN  pip install -r requirements.txt --src=/root/pip
COPY . .