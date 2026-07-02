FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /workspace

RUN apt-get update && \
    apt-get install -y --no-install-recommends tk && \
    rm -rf /var/lib/apt/lists/*

COPY requirements ./requirements
COPY setup.py setup.cfg pyproject.toml README.md ./
COPY tabdeal ./tabdeal

RUN pip install --upgrade pip && \
    pip install -r requirements/requirements-dev.txt && \
    pip install -e .

CMD ["sleep", "infinity"]
