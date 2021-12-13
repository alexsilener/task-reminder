from crontab import CronTab
import taskr
from datetime import datetime, timedelta
from loguru import logger

def set_cron_notify(cron, id, time: datetime, repeat, title, message):
    remove_cron_job(cron, id)
    if repeat == "d":
        job = cron.new(command=f'/bin/python3 /home/corven/work/git/task-reminder/remind.py --title {"in 5 mins: "+ title} --message {message}')
        job.setall(time.time())
    elif repeat == "s":
        job = cron.new(command=f'/bin/python3 /home/corven/work/git/task-reminder/remind.py --title {"in 15 mins: "+ title} --message {message}')
        job.setall(time)

    job.set_comment(f"taskr_id_{id}")

def read_cron_ids(cron):
    ids = []
    for job in cron:
        id = job.comment.split("_")
        if len(id) == 3:
            id = int(id[-1])
            ids.append(id)
    
    return ids

def remove_cron_job(cron, id):
    if not isinstance(id, int):
        return

    for job in cron.find_comment(f'taskr_id_{id}'):
        cron.remove(job)

def main():
    data = taskr.read_data()
    with CronTab(user=True) as cron:
        cron_ids = read_cron_ids(cron)
        for idx, row in enumerate(data):
            if "reminder" in row.keys() and (row["repeat"] == "d" or row["repeat"] == "s"):
                if row["id"] in cron_ids:
                    cron_ids.remove(row["id"])
                set_cron_notify(cron, row["id"], datetime.fromisoformat(row["reminder"]), row['repeat'], 
                                row['name'], row['name']+" - a taskr reminder.")
                logger.info(f"Set cron job for task id {row['id']} - {row['name']}")
        
        # cleaning up
        if len(cron_ids):
            for id in cron_ids:
                remove_cron_job(cron, id)
            logger.info("old task reminders removed.")
if __name__ == "__main__":
    main()