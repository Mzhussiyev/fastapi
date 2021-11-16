FROM python:3.9-slim as builder
WORKDIR /install
COPY requirements.txt .
RUN pip install --prefix=/install --no-cache-dir -r requirements.txt

FROM python:3.9-slim
WORKDIR /reporting-app
COPY --from=builder /install /usr/local
COPY . .
EXPOSE 8080
CMD ["gunicorn", "-k", "uvicorn.workers.UvicornWorker", "-w", "6", "-b", "0.0.0.0:8080", "--access-logfile", "-", "--error-logfile", "-", "reporting.main:app"]
