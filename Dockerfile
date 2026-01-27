FROM python:3.12
WORKDIR /app

COPY req.txt req.txt
RUN pip install -r req.txt

COPY . .


CMD ["sh", "-c", "alembic upgrade head && python src/main.py"]