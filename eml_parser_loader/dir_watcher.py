import os
import time
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler
from eml_ioc_extractor import parse_eml
from config import WATCHER_PATTERNS, WATCH_PATH, ARCHIVE_PATH
from elk_shipper import send_to_elk


def on_created(event):
    try:
        print(f"Processing file: {event.src_path}")
        eml_data = parse_eml(event.src_path)
        send_to_elk(eml_data)
        filename = os.path.basename(event.src_path)
        os.rename(event.src_path, f"{ARCHIVE_PATH}/{filename}")
    except Exception as e:
        print(e)


if __name__ == "__main__":
    event_handler = PatternMatchingEventHandler(
        WATCHER_PATTERNS,
        ignore_directories=True,
        case_sensitive=True
    )
    event_handler.on_created = on_created
    my_observer = Observer()
    my_observer.schedule(event_handler, WATCH_PATH, recursive=True)
    my_observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        my_observer.stop()
        my_observer.join()
