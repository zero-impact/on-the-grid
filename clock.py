#This file controls the scheduling of tasks such as posting to hipchat
#and updating the database with new information

import subprocess
from apscheduler.schedulers.blocking import BlockingScheduler

import logging
logging.basicConfig()

sched = BlockingScheduler()

def db_tasks():
    subprocess.call(["python", "manage.py", "update_vendors"])
    subprocess.call(["python", "manage.py", "update_vendor_events"])

@sched.scheduled_job('date') #run once immediately on starting the web app
def scheduled_job():
    db_tasks()

@sched.scheduled_job('cron', day_of_week='*', hour=23, minute=59)
def scheduled_job():
    db_tasks()

@sched.scheduled_job('cron', day_of_week='*', hour=23, minute=59)
def scheduled_job():
    subprocess.call(["python", "manage.py", "update_vendors"])
    subprocess.call(["python", "manage.py", "update_vendor_events"])

@sched.scheduled_job('cron', day_of_week='wed,fri', hour=11)
def scheduled_job():
    subprocess.call(["python", "manage.py", "post_to_hipchat"])

sched.start()