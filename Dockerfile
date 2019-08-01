FROM python:3.7-alpine
WORKDIR /code
ENV HOST 0.0.0.0
EXPOSE 32001
RUN apk add --no-cache gcc musl-dev linux-headers
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY ronarlistener /code
CMD ["python", "ronar_server.py"]