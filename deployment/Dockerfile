#!/usr/bin/env bash

FROM nginx

ENV NGINX_HOST=localhost
ENV API_URL=/api/

RUN mkdir -p /setup
WORKDIR /setup

# Install node#
RUN apt-get update
RUN apt-get install -y curl
RUN curl -sL https://deb.nodesource.com/setup_6.x | bash -
RUN apt-get install -y nodejs

# Build frontend
RUN apt-get install -y git-core
RUN git clone https://github.com/projectsecure/projectsecure-client.git
WORKDIR /setup/projectsecure-client
RUN npm install
RUN npm install webpack -g
RUN webpack -p
RUN mkdir -p /var/www/projectsecure/public/
RUN mv /setup/projectsecure-client/dist/* /var/www/projectsecure/public/

# Setup NGINX
WORKDIR /setup
COPY nginx.conf /setup

EXPOSE 80 443
