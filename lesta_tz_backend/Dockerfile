FROM python

COPY . /app

WORKDIR /app

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload", "--forwarded-allow-ips=*"]

EXPOSE 8003