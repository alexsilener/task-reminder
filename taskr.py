import json
from json.decoder import JSONDecodeError
import tabulate
import click
import os
from loguru import logger
import datetime

# calling main() after while within main() doesnt work
# remove the need for main after every function
# some very convoluted lines need to be simplified
# rewrite json file pattern to be dict of dicts with id as first index

json_path = os.path.join(os.getcwd(),"data.json")

def get_new_id():
    last_id = 0
    data = read_data()
    if data is not None and len(data) > 0:
        # sort. check if in. make this better.
        last_id = data[-1]["id"]
    return last_id + 1

def read_data(display=True):
    try:
        with open(json_path, "r") as f:
            data = json.load(f)
            if display:
                data = [row for row in data if row["display"]]
    except FileNotFoundError:
        with open(json_path, "w") as f:
            logger.info("First run. Making local json file")
            data = []
            json.dump(data, f)
    except JSONDecodeError:
        logger.warning("Corrupt local JSON data. initializing runtime data to null. Unhandled behaviour. \
                        Abort immediately to save local state.")
        data = []

    return data            

def write_data(data):
    try:
        with open(json_path, "w") as f:
            json.dump(data, f)
    except:
        logger.error("unhandled in write_data")
        raise

@click.command()
def list():
    data = read_data()
    print(tabulate.tabulate(data, headers="keys"))
    main()

@click.command()
@click.option('--name', prompt='task name >',
              help='Enter a task to add.')
def t_add(name: str):
    data = read_data()
    id = get_new_id()
    task = dict(id=id, name=name.strip(), display=True)
    data.append(task)
    write_data(data)
    main()

@click.command()
@click.option('--id', prompt='task id to remove >')
def t_remove(id):
    """just no longer displays. task always stored in json."""
    if input("enter y to confirm: ").lower() not in ("y", "yes"):
        main()

    id = int(id)
    data = read_data()
    # inefficient. especially for long lists
    if id not in [row["id"] for row in data]:
        logger.error("id not in task list.")
    else:
        for idx, row in enumerate(data):
            if id == row["id"]:
                data[idx]["display"] = False 
    write_data(data)
    main()

@click.command()
@click.option('--id', prompt='task id to set reminder for >')
@click.option('--date_time', prompt="reminder date and time iso format YYYY-MM-DDTHH:MM >")
@click.option('--repeat', prompt="s - single, d - daily, w - weekly >")
def remind(id, date_time, repeat):
    data = read_data()
    if int(id) not in [row["id"] for row in data]:
        logger.error("id not in task list.")
    else:
        date_time = datetime.datetime.fromisoformat(date_time)
        # date time formats not serialisable. for now will have to rely on redoing it to string.
        # point of this is to auto parse partial time information
        date_time = date_time.isoformat()

        for idx, row in enumerate(data):
            if int(id) == row["id"]:
                data[idx]["reminder"] = date_time
                data[idx]["repeat"] = repeat
    write_data(data)
    main()

@click.command()
@click.option('--command', prompt='>',
              help='enter a command. list todo')
def main(command):
    """Simple program that does todo reminders."""
    
    while True:
        if command == "add":
            t_add()
        elif command == "list":
            list()
        elif command == "remove":
            t_remove()
        elif command == "remind":
            remind()

        main()

if __name__ == '__main__':
    read_data()
    main()