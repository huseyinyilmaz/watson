# Base Project image
# This image has requirements of
# generic environment.
FROM python:3.7.0b5-alpine3.7

WORKDIR /usr/src/app

# graphviz is needed for graph_models call.
RUN apk update && \
    apk add --update \
        alpine-sdk \
        libjpeg \
        zlib-dev \
        tiff-dev \
        freetype-dev \
        lcms2-dev \
        libwebp-dev \
        openjpeg-dev \
        pngquant \
        graphviz && \
    rm -rf /var/cache/apk/* ;

# Copy requirements folder.
COPY ./requirements.txt ./requirements.txt

RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt
