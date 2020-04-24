import logging

# LEVELS = {0: 'ERROR', 1: 'WARNING', 2: 'INFO', 3: 'DEBUG'}


def configure_stream(level="WARNING"):
    """Configure root logger using a standard stream handler.
    Args:
        level (string, optional): lowest level to log to the console
    Returns:
        logging.RootLogger: root logger instance with attached handler
    """
    # get the root logger
    root_logger = logging.getLogger()
    # set the logger level to the same as will be used by the handler
    root_logger.setLevel(level)

    # customize formatter, align each column
    template = "[%(asctime)s] %(levelname)-8s %(message)s"
    formatter = logging.Formatter(template)

    # add a basic STDERR handler to the logger
    console = logging.StreamHandler()
    console.setLevel(level)
    console.setFormatter(formatter)

    root_logger.addHandler(console)
    return root_logger
