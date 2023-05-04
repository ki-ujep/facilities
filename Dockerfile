FROM python:3.9-alpine

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN mkdir /app
WORKDIR /app

RUN addgroup -S django && adduser -S -G django -u 1000 django

COPY ./requirements.txt /app/
RUN pip install --trusted-host pypi.python.org -r requirements.txt

COPY ./facility /app

RUN chown -R django:django /app

RUN python manage.py collectstatic --noinput

USER django

EXPOSE 8000

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "3", "facility.wsgi:application"]

