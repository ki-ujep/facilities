FROM python:3.9-alpine

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN mkdir /facility
WORKDIR /facility

COPY ./requirements.txt /facility/.
COPY ./facility /facility

COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

RUN addgroup -S django && adduser -S -G django -u 1000 django && \
    pip install --trusted-host pypi.python.org -r requirements.txt && \
    python manage.py collectstatic --noinput

USER django

EXPOSE 8000

ENTRYPOINT ["/entrypoint.sh"]
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "3", "facility.wsgi:application"]

