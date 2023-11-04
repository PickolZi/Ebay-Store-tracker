FROM python:3.11-alpine3.17
WORKDIR /usr/backend
COPY . .
RUN pip install -r requirements.txt
CMD ["python", "run.py"]