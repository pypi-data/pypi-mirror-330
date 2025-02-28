import logging
from TrueGIXERJ_Utils.colours import red, cyan, yellow, green

# Define "SUCCESS" logging level as 25 (between INFO and WARNING)
SUCCESS = 25
logging.addLevelName(SUCCESS, "SUCCESS")

class ColoredFormatter(logging.Formatter):
    """
    A custom logging formatter that applies colours to different log levels.

    The formatter modifies the log level name (INFO, DEBUG, SUCCESS, WARNING, ERROR) by colouring it
    in console output. The colors are mapped based on log level.
    """
    COLORS = {
        logging.DEBUG: cyan,
        logging.INFO: cyan,
        SUCCESS: green,
        logging.WARNING: yellow,
        logging.ERROR: red,
        logging.CRITICAL: red,
    }

    def format(self, record):
        """
        Format the log record with colour based on its level.

        :param record: the log record to format.
        :return: the formatted log message with color applied to just the level name.
        """
        colourise = self.COLORS.get(record.levelno, str)
        #record.msg = colourise(record.msg)
        record.levelname = colourise(record.levelname)
        return super().format(record)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG) # Default logging level

# log format [HH:MM:SS] [LEVEL] MESSAGE
formatter = ColoredFormatter('%(asctime)s [%(levelname)s] %(message)s', datefmt='[%H:%M:%S]')
stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)
logger.addHandler(stream_handler)


def success(self, message, *args, **kwargs):
    """
    Custom logging method for logging success messages.
    Behaves similarly to 

    :param message: the log message to be logged.
    :param args: any additional arguments to pass to the log message.
    :param kwargs: any keyword arguments for the log message.
    """
    if self.isEnabledFor(SUCCESS):
        self._log(SUCCESS, message, args, **kwargs)
logging.Logger.success = success
