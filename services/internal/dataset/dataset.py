import sys, time

from imports.config import Config
from imports.manager import Manager

def set_interval(func, sec, args=[]):
    while 1:
        if (not args):
            func()
        else:
            func(args)
        time.sleep(sec)

print("Dataset server started.")

commands = ["-config", "-c"]
current_command = ""

for arg in sys.argv[1:]:
    if arg in commands:
        current_command = arg
    else:
        if current_command == "-config" or current_command == "-c":
            Config.set_config(arg)

manager = Manager(Config.val['sources_file'])

#set_interval(manager.update_datasets, Config.val['get_interval'])
manager.update_datasets()
