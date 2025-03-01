import fnmatch
import os
import time

from .kaa_definition import KaaDefinition


class KeyWatcher:
    def watch(self, callback):
        while True:
            a = input("")
            if "r" == a:
                callback("restart")
            if "q" == a:
                callback("quit")
            time.sleep(1)


class FileWatcher:
    def __init__(self) -> None:
        definition = KaaDefinition()
        self.path = definition.get_root_path()
        self.interval = definition.get_polling_interval()
        self.validator = ElementValidator(*definition.get_polling_paths())

    def watch(self, callback):
        last_mtime = None
        while True:
            current_mtime = max(
                os.path.getmtime(os.path.join(root, f))
                for root, _, files in os.walk(self.path)
                if self.validator.is_valid(root)
                for f in files
                if self.validator.is_valid(f)
            )
            if last_mtime and current_mtime > last_mtime:
                print("Changes detected.")
                callback("restart")
            last_mtime = current_mtime
            time.sleep(self.interval)


class ElementValidator:
    def __init__(self, inclusions: list, exclusions: list) -> None:
        self.inclusions = inclusions
        self.exclusions = exclusions

    def is_valid(self, element: str) -> bool:
        if not element.strip():
            return False
        normalized = os.path.normpath(element)
        if self.exclusions:
            for exclude in self.exclusions:
                if fnmatch.fnmatch(normalized, exclude):
                    return False
        if self.inclusions:
            for include in self.inclusions:
                if fnmatch.fnmatch(normalized, include):
                    return True
            return False
        return True
