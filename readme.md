# Red Cross Volunteer Registry

A django webapp to handle volunteers at Indian Red Cross.

This webapp has only been tested on Ubuntu 16.04.
It is compatible with python 2.7 and python 3.4+.

## Deploying on Heroku

### Required environment variables

* `SECRET_KEY`: This will be used as `django.conf.settings.SECRET_KEY`.
* `HEROKU`: Set this variable to any value.
  The presence of this environment variable makes django use settings appropriate for Heroku.

### Setup instructions

1.  Create a heroku app.
2.  Setup environment variables as specified above.
3.  Push code to heroku app.
4.  Run a one-off dyno (using `heroku run bash`) and run these commands on it:
    * `python manage.py migrate`.
    * `python createsuperuser`. Now fill out details of the superuser.
    * Optionally run `scripts/load_all_locs.py` or `scripts/load_locations.py` to load location
      data. See `sample_data/` for an example of location files.

## Deploying locally for testing

For setting up a development environment, you must install the required dependencies.
It is recommended to use a virtualenv.

### Quick start

    pip install -r requirements/dev.txt.
    python manage.py migrate
    python createsuperuser
    python scripts/load_all_locs.py sample_data
    python manage.py runserver

Now go to http://localhost:8000/admin/ to check out your webapp.

## Settings

Settings can be found in `project_conf/settings/`:

* `heroku.py` contains settings to run the webapp on Heroku.
* `default.py` contains settings to run the development environment.
* `__init__.py` contains the common settings.

If you want to override settings, it is recommended to copy `default.py`
to a new file `local.py` and make changes there, to avoid messing things up.

We use SQLite by default for development and testing.
You can change settings to use something else.

We use whitenoise to serve static assets.

## Directory structure

* `devel` - Tools to help with development and testing.
* `lib` - Useful reusable code.
* `main` - The main django app.
* `mysite` - locale data.
* `project_conf` - Project settings. Also contains root urlconf and wsgi.py.
* `requirements` - Project requirements for dev and heroku.
* `sample_data` - Sample csv files containing location data.
  These can be used with `scripts/load_all_locs.py` and `scripts/load_locations.py`.
* `scripts` - Scripts useful in both development and production.
* `stubs` - mypy stubs for django. Useful for type checking.

## Automated testing

* [mypy](http://mypy-lang.org) - static type checker for python.
  First do `pip install -r requirements/mypy.txt`.
  Then use it from `devel/run_mypy.py`. It only works on python 3.
* pyflakes - linter and static checker.
  Use it from `devel/lint_all.py`.
  `devel/lint-all.py` also uses a custom linter.
* `python manage.py test` - django backend tests.

We also have a .travis.yml to run tests automatically on Travis CI.
The travis helper scripts are located in `devel/travis/`.
