FROM python:3.13-alpine

WORKDIR /app

COPY pyproject.toml README.md LICENSE ./
COPY src ./src

RUN pip install --no-cache-dir ".[docker]"

EXPOSE 5000

CMD ["gunicorn", "--bind=0.0.0.0:5000", "app.app:app"]
