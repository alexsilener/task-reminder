#!/usr/bin/env python

import argparse
import subprocess

def get_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    
    parser.add_argument("--title", type=str, nargs="+", default="Reminder")
    parser.add_argument("--message", type=str, nargs="+", default="you forgot this part")
    
    return parser

def notify(title: str, message: list):
    # not really sure what the xdg runtime does. but it works. but there is some issue with getting notify-send to work with cron.
    subprocess.run([f'XDG_RUNTIME_DIR=/run/user/$(id -u) notify-send "{" ".join(title).capitalize()}"  "{" ".join(message).capitalize()}"'], shell=True)
    return

if __name__ == "__main__":
    
    args = get_parser().parse_args()
    
    notify(args.title, args.message)