FROM python:3-alpine
WORKDIR /backend
COPY /src /backend/src
COPY /data /backend/data
COPY requirements.txt /backend
RUN pip install -r requirements.txt
ARG HERE_API_SECRET
ENV HERE_API_SECRET $HERE_API_SECRET
EXPOSE 5000
ENTRYPOINT ["python", "src/main.py"]
