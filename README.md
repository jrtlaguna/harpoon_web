# Harpoon Web Platform

## Minimum Requirements

```console
$ python3 --version
Python 3.9.7
$ psql --version
psql (PostgreSQL) 14.0
```

## Setup

```console
$ cp .env.dev.example .env # <- update the env file as needed
$ python3 -m venv venv
$ . ./venv/bin/activate
(venv) $ pip install -r requirements.txt
(venv) $ pre-commit install # <- code style checker/linter -- important!
(venv) $ chmod +x ./manage.py
(venv) $ ./manage.py migrate
(venv) $ ./manage.py runserver
Django version 3.2.9, using settings 'config.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CONTROL-C.
```

## Deployment

Manual steps:

1. Create a Heroku app (`heroku create`)
2. Setup the environment variables (`heroku config:set`)
3. Make sure to set `IS_HEROKU` to `1`
4. `git push heroku master`

Automation via Bitbucket pipelines:

1. Add the following repository variables:

- `HEROKU_API_KEY` -> Your Heroku oAuth2 token
- `HEROKU_PROD_APP_NAME` -> The Heroku app name for the production environment
- `HEROKU_STAGING_APP_NAME` -> The Heroku app name for the staging environment

2. You'd also need to add the environment variables used by the application to the repository. See the
   `.env.dev.example` file for more details.

## Conventions

- When creating a new app, see if it makes sense to name it according to a "main" model. For example, if an app is built
  around an `Event` model, it can be named as `events`
- If it comprises multiple "main" models, name it appropriately according to its use-case. For example, an app that
  comprises a `User`, `Account`, and `AccessToken` model, it can be named as `authentication`
- Always add an `app_name` to a new app's `urls.py`, which should be the same as the app name itself
