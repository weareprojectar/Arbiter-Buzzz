#! /bin/bash

## change owndership of celerybeat-schedule file
chown arbiter celerybeat-schedule

## copy celery conf files to supervisor conf directory
cp ./config/celery* /etc/supervisor/conf.d

## read in supervisor conf files and start processes
supervisorctl reread
supervisorctl update
supervisorctl start arbiter_celery
supervisorctl start arbiter_celerybeat
