FROM python:3.13-slim

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
WORKDIR /src

RUN pip install --upgrade pip
COPY requirements.txt .
RUN pip install -r requirements.txt --no-cache-dir && pip install "fastapi[standard]"

COPY . .

EXPOSE 8000

CMD ["uvicorn", "./main:app", "--host", "0.0.0.0", "--port", "8000"]
#CMD ["fastapi", "run", "src/main.py", "--port", "80"]