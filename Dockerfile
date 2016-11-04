FROM python:3.6-onbuild
EXPOSE 8000

COPY requirements.txt /setup/
RUN pip3 install --no-cache-dir --global-option=build_ext --global-option="-I/usr/local/include" \
        -r /setup/requirements.txt \
        -U pip

VOLUME /code
WORKDIR /code
COPY . /code
