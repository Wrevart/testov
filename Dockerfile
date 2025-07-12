FROM python:3.10-slim
WORKDIR /app
COPY log_parser.py ./
CMD ["python", "log_parser.py"] 