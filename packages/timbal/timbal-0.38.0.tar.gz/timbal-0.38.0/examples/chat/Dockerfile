FROM ubuntu:22.04

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV DEBIAN_FRONTEND=noninteractive

WORKDIR /timbal

RUN apt update && \
    apt install -yqq --no-install-recommends \
        curl \
        ca-certificates \
        git && \
    apt clean && \
    rm -rf /var/lib/apt/lists/*

RUN curl -LsSf https://astral.sh/uv/install.sh | sh

ENV PATH="/root/.local/bin:$PATH"

COPY . .

RUN uv sync --python 3.12 --python-preference managed

ENV PATH=".venv/bin:$PATH"

CMD ["tail", "-f", "/dev/null"]
