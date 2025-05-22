# api/Dockerfile
FROM python:3.10-slim
WORKDIR /app

# now copying the requirements file that lives at api/requirements.txt
COPY requirements.txt           ./requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# copy _everything_ under ./api into /app
COPY . . 

ENV PYTHONPATH=/app
EXPOSE 8080
CMD ["uvicorn", "api.app:app", "--host", "0.0.0.0", "--port", "8080"]
