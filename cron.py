from crontab import CronTab

with CronTab(user=True) as cron:
    job = cron.new(command='/bin/python3 /home/corven/work/git/task-reminder/remind.py --title test --message testmessage')
    job.minute.every(1)

