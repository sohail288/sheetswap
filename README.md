# Sheetswap

A flask app that allows users to trade sheet music

The models are located outside of app because they do not depend on flask.  You can create a new application using Pyramid and plug the models by just creating a declarative Base.

This project lives at [Sheetswap.com](http://sheetswap.com)

To get this program started and deployed you need to set some key settings located in config.py.  Create a file called .env_local or .env_something and set these variables

```
export APP_SETTINGS='production'| 'dev' | 'testing'
export DEV_DATABASE_URL='yourdatabaseurl'  # this is used only if you are developing locally
export TEST_DATABASE_URL='yourtestdatabaseurl'  # used in testing situations
export PRODUCTION_DATABASE_URL='yourproductiondatabaseurl' # database used in production

# for email purposes
export MAIL_SERVER="the smtp url for your email service"
export MAIL_PORT=portnumber(int)
export MAIL_USE_TLS=true|false
export MAIL_USERNAME='string'
export MAIL_PASSWORD='string'

```

You need to start up a celery instance by doing 
```
  celery -A app.celery_creator worker -l info
```
in the root folder of the app.

The fabric file provided deploys the app into an ubuntu server and takes care of provisioning the database for you.  The only thing you need to provide are the above settings.
