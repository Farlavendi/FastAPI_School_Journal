FROM python:3.13

WORKDIR /src

RUN poetry install

COPY ./src /code/src

CMD ["fastapi", "run", "src/main.py", "--port", "80"]