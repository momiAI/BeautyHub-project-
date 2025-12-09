FROM python:3.12.10
WORKDIR /app

COPY req.txt req.txt
RUN pip install -r req.txt

COPY . .


CMD alembic upgrade head;python src/main.py