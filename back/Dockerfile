FROM python:3.11.1-alpine

WORKDIR /usr/src/back

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev

COPY . .

RUN pip install --upgrade pip

RUN pip install -r requirements.txt

CMD [ "python", "manage.py", "start_bot" ]
