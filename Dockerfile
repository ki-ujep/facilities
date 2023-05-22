FROM python:3.9-alpine

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN mkdir /facility
WORKDIR /facility

COPY ./requirements.txt /facility/.
COPY ./populate_db.sh /.
COPY ./fixtures /fixtures
COPY ./facility /facility

RUN addgroup -S django && adduser -S -G django -u 1000 django && \
    pip install --trusted-host pypi.python.org -r requirements.txt && \
    python manage.py collectstatic --noinput

USER django

EXPOSE 8000

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "3", "facility.wsgi:application"]

