import time
import threading
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class ConfigWatcher(FileSystemEventHandler):
    def __init__(self, config_loader, callback):
        self.config_loader = config_loader
        self.callback = callback

    def on_modified(self, event):
        """Reload the configuration when a file is modified."""
        if event.src_path in self.config_loader.config_paths:
            self.callback()

class ConfigAutoReloader:
    def __init__(self, config_loader, callback):
        self.config_loader = config_loader
        self.callback = callback
        self.observer = Observer()

    def start(self):
        """Start watching for config changes."""
        for path in self.config_loader.config_paths:
            self.observer.schedule(ConfigWatcher(self.config_loader, self.callback), path)
        self.observer.start()

    def stop(self):
        """Stop watching for config changes."""
        self.observer.stop()
        self.observer.join()