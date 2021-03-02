# A simple Django project to illustrate the use of Celery

> I created this project to accompany my blog post at <https://importthis.tech/djangocelery-from-development-to-production>

[![forthebadge](https://forthebadge.com/images/badges/made-with-python.svg)](https://forthebadge.com)

[![CircleCI](https://circleci.com/gh/engineervix/django-celery-sample.svg?style=svg)](https://circleci.com/gh/engineervix/django-celery-sample)
[![codecov](https://codecov.io/gh/engineervix/django-celery-sample/branch/master/graph/badge.svg?token=SFRBRZB8BJ)](https://codecov.io/gh/engineervix/django-celery-sample)

[![python3](https://img.shields.io/badge/python-3.6%20%7C%203.7%20%7C%203.8-brightgreen.svg)](https://python3statement.org/#sections50-why)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![code style: prettier](https://img.shields.io/badge/code%20style-prettier-ff69b4.svg)](https://prettier.io/)
[![Commitizen friendly](https://img.shields.io/badge/commitizen-friendly-brightgreen.svg)](http://commitizen.github.io/cz-cli/)
[![Conventional Changelog](https://img.shields.io/badge/changelog-conventional-brightgreen.svg)](http://conventional-changelog.github.io)
[![Conventional Commits](https://img.shields.io/badge/Conventional%20Commits-1.0.0-yellow.svg)](https://conventionalcommits.org)

<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->
**Table of Contents**  *generated with [DocToc](https://github.com/thlorenz/doctoc)*

- [Prerequisites](#prerequisites)
- [Project Setup](#project-setup)
- [Run the project](#run-the-project)
  - [without celery](#without-celery)
  - [with celery](#with-celery)
- [Tests](#tests)
- [Production-ready](#production-ready)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

## Prerequisites

- A [\*nix](https://en.wikipedia.org/wiki/Unix-like) environment.
- [Python 3.6+](https://www.python.org/). I use [virtualenvwrapper](https://virtualenvwrapper.readthedocs.io/en/latest/) for managing python virtual environments.
- [Node.js 12+](https://nodejs.org/) with the following packages installed **globally** (depending on your Node.js setup, you might need to install as superuser):
  - [gulp](https://gulpjs.com/) – `npm install -g gulp-cli`
  - [concurrently](https://github.com/kimmobrunfeldt/concurrently): `npm install -g concurrently`
  - [MailDev](https://github.com/maildev/maildev) – `npm install -g maildev`
  - [Sass](https://sass-lang.com): `npm install -g sass`
  - [prettier](https://github.com/prettier/prettier/): `npm install prettier -g`
  - [Browsersync](https://browsersync.io/): `npm install -g browser-sync`
  - [commitizen](https://github.com/commitizen/cz-cli) – `npm install -g commitizen`
  - [DocToc](https://github.com/thlorenz/doctoc): `npm install -g doctoc`
- [yarn](https://yarnpkg.com/): See [installation instructions for your platform](https://classic.yarnpkg.com/en/docs/install#debian-stable).
- [redis](https://redis.io/) must be installed and configured on your development machine.

## Project Setup

First, clone the project and `cd` into the cloned directory:

```sh
git clone https://github.com/engineervix/django-celery-sample.git
cd django-celery-sample
```

Then, assuming that you have created and activated your virtual environment, install the python dependencies. This project uses [pip-tools](https://github.com/jazzband/pip-tools) to manage python dependencies.

```sh
pip install pip-tools && pip-sync
# or you could just `pip install -r requirements.txt`
```

Install the Node.js dependencies and copy the vendor libraries to the `static` directory:

```sh
yarn install && gulp cp
```

Create a postgres database and user for the project. If you are using tools such as [PGAdmin](https://www.pgadmin.org/) or [Postgres.app](https://postgresapp.com/), you please feel free to use them according to their documentation. If you are using the CLI like me, you could do it as follows:

```sh
# assuming your DATABASE is my_DB
# assuming USER is my_user
# assuming your PASSWORD is my_password
psql -c "CREATE USER my_user PASSWORD 'my_password'" \
&& psql -c "CREATE DATABASE my_DB OWNER my_user" \
&& psql -c "GRANT ALL PRIVILEGES ON DATABASE my_DB TO my_user"
```

> In order to simplify this, I wrote a simple `bash` script which provides a command `create_db`, and placed it in my `$PATH`. It prompts me for the database and the user names, and generates a random password. I should probably add it to this repo as a utility.

Now that your database is set up, it's time to set up your environment variables. This repo contains a direcctory `.envs.sample` which has sample `.env` files for you to build on and customize.

```sh
# first, rename the `.envs.sample` directory to `.envs` 
mv -v .envs.sample/ .envs/

# then, let's remove the .sample suffix from all the `*.env.sample` files in the renamed directory
for i in $(ls -a .envs/ | grep sample);do mv -i .envs.sample/$i .envs.sample/`basename $i .sample`; done
```

There are three `.env` files:

1. `.dev.env` – for the **development** environment
2. `.test.env` – for the **test** environment
3. `.prod.env` – for the **production** environment

Edit those files and update the environment variables accordingly. The table below shows the environment variables that need to be updated. For now, you can skip the environment variables for production, and only update them when you are ready to go into production.

Please note that, in production, this project uses

- [Sendgrid](https://sendgrid.com/) for sending emails via [django-anymail](https://github.com/anymail/django-anymail). You can use your preferred provider and update both the [production settings](config/settings/production.py) and environment variables accordingly.
- [Sentry](https://sentry.io) for error tracking. You'll have to setup an account (if you don't have one already) and register the project.

|   | development       | test              | production         |
|---|-------------------|-------------------|--------------------|
| 1 | DJANGO_SECRET_KEY | DJANGO_SECRET_KEY | DJANGO_SECRET_KEY  |
| 2 | DATABASE_URL      |                   | DATABASE_URL       |
| 3 |                   |                   | EMAIL_RECIPIENTS   |
| 4 |                   |                   | DEFAULT_FROM_EMAIL |
| 5 |                   |                   | ALLOWED_HOSTS      |
| 6 |                   |                   | BASE_URL           |
| 7 |                   |                   | SENDGRID_API_KEY   |
| 8 |                   |                   | SENTRY_DSN         |

Okay, now that you have installed all dependencies and have set up your database and environment variables, you can now make migrations and create the superuser in readiness to run the project.

```sh
./manage.py makemigrations && ./manage.py migrate
./manage.py createsuperuser
```

We are now ready to run!

## Run the project

### without celery

```sh
yarn dev
```

### with celery

```sh
yarn dev:celery
```

If all goes well, this will launch two tabs in your default browser – a `maildev` tab and a `django` tab with today's date and a quote for today, as shown in the screenshot below:

![screenshot](https://i.imgur.com/Oey9js2.png)

The [Browsersync](https://browsersync.io/) and [gulp](https://gulpjs.com/) setup provides for automatic restarting of the dev server and autoreload of the browser, so you can work on the project and make changes to the files without having to do this manually.

## Tests

This project uses pytest and the initial tests should give you about 93% test coverage.

```sh
yarn test
```

## Production-ready

Going into production shouldn't be too complicated, as the project includes production-ready configurations right from the start:

- I have already mentioned the [`.prod.env`](.envs.sample/.prod.env.sample) file,
- There's the [`config/settings/production.py`](config/settings/production.py) file,
- I created a separate [`wsgi_production.py`](config/wsgi_production.py) file and
- There are some celery and celery beat configuration files in the [`.envs.example/celery`](.envs.sample/celery/) directory. These will come in handy if you're using [systemd](https://systemd.io/). I wrote a [blog post](https://importthis.tech/djangocelery-from-development-to-production) that describes how to daemonize celery and celery beat using systemd.
