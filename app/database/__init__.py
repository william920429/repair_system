import logging
from logging.handlers import TimedRotatingFileHandler
import re  # regex

from .model import db, timeformat, timeformat_re_str
from . import backup, db_helper

__all__ = [db, backup, db_helper]


# def my_namer(default_name):
#     # This will be called when doing the log rotation
#     # default_name is the default filename that would be assigned, e.g. Rotate_Test.txt.YYYY-MM-DD
#     # Do any manipulations to that name here, for example this changes the name to Rotate_Test.YYYY-MM-DD.txt
#     base_filename, ext, date = default_name.split(".")
#     return f"{base_filename}_{date}.{ext}"

# todo rewrite log hendeler
sql_log_handler = TimedRotatingFileHandler(
    r"log/SQL.log",
    when="D",
    interval=10,
    backupCount=2,
    encoding="UTF-8",
    delay=False,
    utc=False,
)

# sql_log_handler.suffix = timeformat
# sql_log_handler.extMatch = re.compile(timeformat_re_str+".log")
# sql_log_handler.namer = my_namer

format = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
sql_log_handler.setFormatter(format)
sql_log_handler.setLevel(logging.INFO)

sql_logger = logging.getLogger('sqlalchemy.engine')
sql_logger.addHandler(sql_log_handler)
sql_logger.setLevel(logging.DEBUG)
