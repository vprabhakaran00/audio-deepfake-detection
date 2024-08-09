FROM python:3.9-slim

RUN apt update -y && apt install awscli -y

# Set the working directory in the container
WORKDIR /app

COPY . /app
RUN pip install -r requirements.txt

# EXPOSE 5000 # Uncomment for local testing

CMD ["python3", "app.py"]