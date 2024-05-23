FROM python:3.12.0
EXPOSE 5000
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . . 
CMD ["/bin/sh","/app/docker-entrypoint.sh"]