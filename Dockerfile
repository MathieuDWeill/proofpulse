FROM python:3.12-slim
WORKDIR /app
COPY apps/api/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
COPY apps/api /app/apps/api
ENV PYTHONPATH=/app/apps/api
EXPOSE 8080
CMD ["uvicorn", "proofpulse_api.main:app", "--host", "0.0.0.0", "--port", "8080"]
