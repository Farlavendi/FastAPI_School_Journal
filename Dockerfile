FROM python:3.13-slim

WORKDIR /src

RUN apt update;

COPY ./src /code/src

RUN python3 -m pip install --upgrade pip

RUN pip3 install -r requirements.txt --no-cache-dir
# RUN poetry install

CMD ["fastapi", "run", "src/main.py", "--port", "80"]