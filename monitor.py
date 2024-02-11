from watchdog.events import FileSystemEvent, PatternMatchingEventHandler


class MyHandler(PatternMatchingEventHandler):
    patterns = ["*.pdf"]
    created = 0

    def on_created(self, event: FileSystemEvent) -> None:
        print(event.src_path)
        self.created = 1

    def get_created(self):
        return self.created

    def reset_create(self):
        self.created = 0
