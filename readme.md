# Red Cross Volunteer Registry

A django webapp to handle volunteers at Indian Red Cross.

## Required environment variables for deploying on Heroku

* `SECRET_KEY`: This will be used as `django.conf.settings.SECRET_KEY`.
* `HEROKU`: Set this variable to any value.
  The presence of this environment variable makes django use settings appropriate for Heroku.
