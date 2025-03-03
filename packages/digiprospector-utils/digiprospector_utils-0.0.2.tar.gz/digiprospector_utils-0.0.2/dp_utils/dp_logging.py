from pathlib import Path
import logging
from colorlog import ColoredFormatter
from logging.handlers import RotatingFileHandler

def get_logger(name, s_lvl=logging.INFO, f_lvl=logging.DEBUG, log_dir=None):
    """
    Return a logger that outputs to both console (colored) and a rotating file.

    Args:
        name (str): The name of the logger.
        s_lvl (int): The logging level for the stream handler (console).
        f_lvl (int): The logging level for the file handler.
        log_dir (str, optional): The directory to save log file. if not set, using the path of caller file. Defaults to None.

    Returns:
        logging.Logger: The configured logger.
    """

    color_formatter = ColoredFormatter(
        "%(log_color)s[%(levelname).1s][%(asctime)s][%(filename)s:%(lineno)d]:%(message)s",
        datefmt='%H:%M:%S',
        reset=True,
        log_colors={
            'DEBUG': 'cyan',
            'INFO': 'green',
            'WARNING': 'yellow',
            'ERROR': 'red',
            'CRITICAL': 'bold_red',
        }
    )

    formatter = logging.Formatter(
        "[%(levelname).1s][%(asctime)s][%(filename)s:%(lineno)d]:%(message)s",
        datefmt='%Y%m%d %H:%M:%S'
    )

    logger = logging.getLogger(name)
    
    if not logger.handlers:
        logger.setLevel(logging.DEBUG)  # Set the lowest level to catch all messages

        # Stream Handler (Console)
        s_handler = logging.StreamHandler()
        s_handler.setFormatter(color_formatter)
        s_handler.setLevel(s_lvl)
        logger.addHandler(s_handler)

        # File Handler
        if not log_dir:
            # Get the caller's file path
            caller_frame = None
            import inspect
            for frame in inspect.stack():
                if frame.filename != __file__:
                    caller_frame = frame
                    break
            if caller_frame:
                caller_file_path = Path(caller_frame.filename)
                log_dir = caller_file_path.parent / "logs"  # Create subdir "logs"
            else:
                log_dir = Path("./logs")  # Create subdir "logs"
        else:
            log_dir = Path(log_dir)

        log_dir.mkdir(parents=True, exist_ok=True)
        
        log_filename = Path(log_dir) / Path(name).with_suffix(".log")
        f_handler = RotatingFileHandler(log_filename, maxBytes=10000000, backupCount=5)
        f_handler.setFormatter(formatter)
        f_handler.setLevel(f_lvl)
        logger.addHandler(f_handler)

    return logger
