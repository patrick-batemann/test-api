FROM python:3.13.1

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

CMD ["sh", "-c", "sleep 5 && uvicorn main:app --host 0.0.0.0 --port 8000"]