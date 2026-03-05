FROM ubuntu:24.04 AS runtime

WORKDIR /code

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        ca-certificates \
        curl \
        jq \
        libhamlib-utils \
        python3 \
        python3-fastapi \
        python3-hamlib \
        python3-serial \
        uvicorn \
    && rm -rf /var/lib/apt/lists/*

COPY ./lib ./lib
COPY ./schemas.py ./schemas.py
COPY ./main.py ./main.py
COPY ./openapi.yaml ./openapi.yaml
COPY ./README.md ./README.md

EXPOSE 8080

CMD ["uvicorn", "--host", "0.0.0.0", "--port", "8080", "main:app"]


FROM runtime AS test

RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        python3-httpx \
        python3-pytest \
    && rm -rf /var/lib/apt/lists/*

COPY ./pytest.ini ./pytest.ini
COPY ./tests ./tests

CMD ["pytest"]
