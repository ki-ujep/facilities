# Facilities

## About project
This application is designed to manage devices used by members of Czech academy of science from UJEP institute. Currently running at [equipment.ujep.cz](https://equipment.ujep.cz).

## Used technologies
- [Django](https://www.djangoproject.com/)

## Requirements
- Web browser (works without JavaScript)

## Installation
- Pull this repository
- Change environment variables in `docker-compose-prod.yml` file
- Run `./setup.sh`
- Use Nginx (we provide sample `nginx.conf`) or any other server as reverse proxy to serve `./media` directory and provide TLS offloading
