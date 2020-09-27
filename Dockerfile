FROM python:3.7-alpine

RUN adduser -D desnos

WORKDIR /home/desnos

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN chown -R desnos:desnos ./
USER desnos

EXPOSE 8000

CMD ["gunicorn", "--workers=4", "--bind=0.0.0.0:8000", "app:app"]

