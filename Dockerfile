FROM gliderlabs/alpine:3.4

RUN apk-install \
    python \
    supervisor && \
    python -m ensurepip && \
    rm -r /usr/lib/python*/ensurepip && \
    pip install --upgrade pip setuptools && \
    rm -r /root/.cache

RUN mkdir -p /app

COPY requirements.txt lib/marathon_autoscaler/ /app/
COPY supervisord.conf /etc/supervisor.d/marathon_autoscaler.ini
RUN pip install -r /app/requirements.txt
CMD ["/usr/bin/supervisord"]
