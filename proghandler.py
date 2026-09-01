import logging
import sys


class ProgressHandler(logging.StreamHandler):
    def emit(self, record):
        try:
            msg = self.format(record)

            if getattr(record, "progress", False):
                sys.stdout.write("\r\033[K" + msg)
                sys.stdout.flush()
            else:
                # Finish the current progress line first
                sys.stdout.write("\r\033[K")
                sys.stdout.flush()

                sys.stdout.write(msg + "\n")
                sys.stdout.flush()

        except Exception:
            self.handleError(record)