# Online Bank Service

This repository contains the code for Bank API backend.

---

## Documentation

This project has been developed using [Django][django] and [Django Ninja][djangoninja], [Postgres][postgres] as relational database, [Yandex Object Storage][storage] as Object storage S3.

Code structure implementation follows a [Clean Architecture][cleanarchitecture] approach, emphasizing on code readability, responsibility decoupling and unit testing.

Also, in addition to REST API, it uses [python-telegram-bot][bot] library, asynchronous interface for the [Telegram Bot API][apitelegram].

## Setup

Download source code cloning this repository:
```
git clone https://github.com/bigcrazyfrog/bank-service.git
```

## Run the API backend:

Create `.env` file from `.env.example`.

Create docker images and execute the containers for development. Use commands from `Makefile`:
```
make build
make up
```


[//]: # (Links)

[apitelegram]: <https://core.telegram.org/bots/api>
[bot]: <https://python-telegram-bot.org/>
[cleanarchitecture]: <https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html>
[django]: <https://www.djangoproject.com>
[djangoninja]: <https://django-ninja.rest-framework.com/>
[postgres]: <https://www.postgresql.org>
[storage]: <https://cloud.yandex.ru/docs/storage/>
