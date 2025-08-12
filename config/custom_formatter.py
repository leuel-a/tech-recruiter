import logging


class CustomFormatter(logging.Formatter):
    """
    A custom formatter that adds color to log levels.
    """

    # ANSI escape codes for colors
    ANSI_BLUE = "\x1b[34m"
    ANSI_RED = "\x1b[31m"
    ANSI_RESET = "\x1b[0m"

    FORMATS = {
        logging.INFO: f"%(asctime)s - {ANSI_BLUE}%(levelname)s{ANSI_RESET} - %(message)s",
        logging.ERROR: f"%(asctime)s - {ANSI_RED}%(levelname)s{ANSI_RESET} - %(message)s",
        "DEFAULT": "%(asctime)s - %(levelname)s - %(message)s"
    }

    def format(self, record):
        """
        Format the specified record with colors based on log level.

        :param record: The log record to format.
        :type record: logging.LogRecord
        :return: The formatted log message as a string.
        :rtype: str
        """
        log_fmt = self.FORMATS.get(record.levelno, self.FORMATS["DEFAULT"])
        formatter = logging.Formatter(log_fmt)
        return formatter.format(record)

