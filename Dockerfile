FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt
COPY . .
RUN chmod +x remediation/*.sh
EXPOSE 8000
ENV REMEDIATION_TOKEN="secret-key-123"
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
