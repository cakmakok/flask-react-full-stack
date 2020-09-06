FROM python:3-alpine
WORKDIR /app
COPY /src /app
COPY requirements.txt /app
RUN pip install -r requirements.txt
EXPOSE 5000
ENTRYPOINT ["python", "main.py"]
