#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import sys
import time

from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer


class MyEventHandler(FileSystemEventHandler):
    def catch_all_handler(self, event):
        logging.debug(event)

    def on_moved(self, event):
        self.catch_all_handler(event)

    def on_created(self, event):
        self.catch_all_handler(event)

    def on_deleted(self, event):
        self.catch_all_handler(event)

    def on_modified(self, event):
        self.catch_all_handler(event)


import imp
print(imp.b)

with open("imp.py", "w") as file:

    file.write("a = 10")

import importlib

importlib.reload(imp)

print(imp.a)



# event_handler = MyEventHandler()
# observer = Observer()
# observer.schedule(event_handler, path, recursive=True)
# observer.start()
# try:
#     while True:
#         time.sleep(1)
# except KeyboardInterrupt:
#     observer.stop()
# observer.join()
#
# with open
