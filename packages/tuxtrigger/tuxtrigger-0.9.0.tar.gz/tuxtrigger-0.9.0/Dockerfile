FROM debian:bullseye-slim

COPY run /usr/bin/tuxtrigger
COPY requirements.txt /tmp

RUN apt update && \
    apt install --yes git python3 python3-pip python3-yaml && \
    pip install -r /tmp/requirements.txt && \
    apt clean && \
    rm -rf /var/lib/apt/lists/* && \
    rm -rf /root/.cache/ && \
    find /usr -depth -name __pycache__ -type d -exec rm -rf {} \;

COPY /tuxtrigger/ /usr/lib/python3/dist-packages/tuxtrigger

