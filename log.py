from botpy import logging
import os
from botpy.logging import DEFAULT_FILE_HANDLER

DEFAULT_FILE_HANDLER["filename"] = os.path.join(os.getcwd(), "log", "%(name)s.log")

_log = logging.get_logger()

if not os.path.exists("markdown"):
    os.mkdir("markdown")


class MarkdownLogger:
    def __init__(self):
        self.dir = "markdown/"
        self.markdown_filename = ""
        self.logMode = False

    def set_file_name(self, filename):
        self.markdown_filename = filename + ".md"
        self.logMode = True

    def log(self, message):
        if self.logMode:
            if not message.startswith("(") and not message.startswith("（"):
                with open(os.path.join(self.dir, self.markdown_filename), "a", encoding="utf-8") as file:
                    file.write(f"{message}\n")

    def log_mode_on(self):
        self.logMode = True

    def log_mode_off(self):
        self.logMode = False

    def return_md_file(self):
        if self.logMode:
            self.logMode = False
            return self.markdown_filename
        else:
            return None


class MarkdownFileLogger(MarkdownLogger):
    def __init__(self):
        super().__init__()

    def log(self, message):
        super().log(message)


_mdlogger = MarkdownFileLogger()
