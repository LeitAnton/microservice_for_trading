FROM python:3.10.12-alpine as builder

WORKDIR /usr/src/microservice

COPY Pipfile.lock Pipfile ./

RUN apk --no-cache add \
    gcc\
    libc-dev\
    libffi-dev\
    musl-dev\
    python3-dev\
    zlib-dev\
    && pip3 install pipenv\
    && pipenv requirements > requirements.txt\
    && pip wheel --no-cache-dir --no-deps --wheel-dir /usr/src/microservice/wheels -r requirements.txt

FROM python:3.10.12-alpine

ENV USER=microservice_for_trading \
    PYTHONFONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

RUN addgroup -S $USER && adduser -S $USER -G $USER

ENV HOME=/home/$USER
ENV APP_HOME=/home/$USER/microservice
RUN mkdir -p $APP_HOME
WORKDIR $APP_HOME

COPY --from=builder /usr/src/microservice/wheels /wheels
COPY --from=builder /usr/src/microservice/requirements.txt .
RUN pip install --no-cache-dir /wheels/*

COPY . $APP_HOME

RUN chown -R $USER:$USER $APP_HOME
USER $USER

RUN chmod +x $APP_HOME/microservice-entrypoint.sh

ENTRYPOINT sh $APP_HOME/microservice-entrypoint.sh
