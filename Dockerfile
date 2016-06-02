FROM gliderlabs/alpine:3.3

RUN apk-install \
    python3 \
    python3-dev \
    py-pip \
    supervisor \
    build-base \
  && mkdir -p /app

COPY requirements.txt lib/marathon-autoscaler/ /app/
COPY supervisord.conf /etc/supervisor.d/marathon_autoscaler.ini
RUN pip install -r /app/requirements.txt
RUN apk del build-base python3-dev
CMD ["/usr/bin/supervisord"]
