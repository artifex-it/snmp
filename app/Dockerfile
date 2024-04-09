FROM python:3.11-slim

RUN apt update
RUN apt install sqlite3


ENV PYTHONUNBUFFERED=1

WORKDIR /app
ADD . .
RUN pip install -r requests.txt

# ENTRYPOINT python
# CMD ["main.py"]
CMD ["python", "main.py"]
