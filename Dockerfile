FROM python:3.10-slim
WORKDIR /app

RUN mkdir -p /app/config /app/stats

COPY log_parser.py ./
COPY config/ ./config/

RUN chmod 755 /app/stats

CMD ["python", "log_parser.py"] 