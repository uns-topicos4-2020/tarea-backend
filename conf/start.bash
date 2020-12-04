#!/bin/bash

USER=rc                                           # the user to run as
NAME="topicos4"                                   # Name of the application
PROJECT_DIR=/home/$USER/webapps/$NAME             # Project directory
SOURCE_DIR=$PROJECT_DIR/src                       # Source directory
SOCKFILE=$PROJECT_DIR/gunicorn.sock  # we will communicte using this unix socket
NUM_WORKERS=1                                     # how many worker processes should Gunicorn spawn

# GROUP=webapps                                     # the group to run as
# DJANGO_SETTINGS_MODULE=hello.settings             # which settings file should Django use
# DJANGO_WSGI_MODULE=hello.wsgi                     # WSGI module name

echo "Starting $NAME as `whoami`"

# Activate the virtual environment
cd $SOURCE_DIR
source /home/$USER/.virtualenvs/$NAME/bin/activate
# export DJANGO_SETTINGS_MODULE=$DJANGO_SETTINGS_MODULE
# export PYTHONPATH=$SOURCE_DIR:$PYTHONPATH

# Create the run directory if it doesn't exist
RUNDIR=$(dirname $SOCKFILE)
test -d $RUNDIR || mkdir -p $RUNDIR

# Start your Django Unicorn
# Programs meant to be run under supervisor should not daemonize themselves (do not use --daemon)
exec /home/$USER/.virtualenvs/$NAME/bin/uwsgi --ini $PROJECT_DIR/conf/uwsgi_config.ini
