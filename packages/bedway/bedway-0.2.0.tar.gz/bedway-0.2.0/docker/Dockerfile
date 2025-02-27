FROM python:3.11.10-slim-bookworm as builder

RUN pip install hatch
COPY . /source
WORKDIR /source
RUN hatch build

FROM python:3.11.10-slim-bookworm

RUN apt-get update && apt-get install -y --no-install-recommends \
    tini \
    && rm -rf /var/lib/apt/lists/*

COPY --from=builder /source/dist/*.whl /tmp/
RUN pip install --no-cache-dir /tmp/*.whl

ENTRYPOINT ["/usr/bin/tini", "--", "bedway"]
CMD [ "serve" ]

LABEL org.opencontainers.image.source=https://github.com/wh1isper/bedway
