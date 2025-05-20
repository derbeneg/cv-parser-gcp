FROM python:3.10-slim
WORKDIR /app

# Pull in the requirements file from api/
COPY api/requirements.txt ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy everything (including the 'api/' folder) into /app
COPY . /app

# Ensure Python can import the 'api' package
ENV PYTHONPATH=/app

EXPOSE 8080
CMD ["uvicorn", "api.app:app", "--host", "0.0.0.0", "--port", "8080"]
