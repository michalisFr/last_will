#!/usr/bin/env python3
from crontab import CronTab
import sys
from pathlib import Path

my_cron = CronTab(user=True)
my_cron.remove_all(comment='check in')

valid_vars = ['SHELL', 'PATH', 'MAILTO']

time = '12:00'

for index, arg in enumerate(sys.argv):
    if index > 0:
        (env_var, value) = sys.argv[index].split('=')
        if env_var.upper() in valid_vars:
            my_cron.env[env_var.strip().upper()] = value.strip()
        elif env_var.upper() == 'REMOVE':
            if value.strip().upper() in my_cron.env.keys():
                my_cron.env.pop(value.strip().upper())
        elif env_var.upper() == 'TIME':
            time = value

job = my_cron.new(command=f'cd {Path.cwd()} && pipenv python3 check_in.py', comment='check in')
job.day.every(1)
job.hour.on(time.split(':')[0].strip())
job.minute.on(time.split(':')[1].strip())

my_cron.write()


