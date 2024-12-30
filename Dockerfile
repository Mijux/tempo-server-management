FROM python:3.12-alpine
# --platform=<platform>
WORKDIR /app/

ARG USERNAME=tempo  
ARG USER_UID=1617
ARG USER_GID=${USER_UID}

COPY . .

RUN addgroup -g ${USER_GID} ${USERNAME} \
    && adduser -u ${USER_UID} -G ${USERNAME} -D ${USERNAME} \
    && apk update \
    && python3 -m venv .venv \
    && .venv/bin/pip3 install --no-cache-dir -r requirements.txt

USER ${USERNAME}

CMD [ ".venv/bin/python3", "main.py" ]