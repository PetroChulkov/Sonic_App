FROM python:3.10-slim-buster

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1

ENV PYTHONUNBUFFERED=1

RUN pip install --upgrade pip 

COPY . .

RUN pip install -r requirements.txt

EXPOSE 8000

CMD [ "python", "manage.py", "runserver", "0.0.0.0:8000"]