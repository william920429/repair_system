from os import path, mkdir
import logging
from logging.handlers import TimedRotatingFileHandler
from datetime import datetime
from flask import Flask, has_request_context, request
from flask_login import LoginManager
from flask_mail import Mail
from flask_apscheduler import APScheduler
from .config import config
from .database import db


login_manager = LoginManager()
mail = Mail()
scheduler = APScheduler()

class RequestFormatter(logging.Formatter):
    def format(self, record):
        if has_request_context():
            record.url = request.url
            record.remote_addr = request.remote_addr
        else:
            record.url = None
            record.remote_addr = None

        return super().format(record)


def create_app(env):
    app = Flask(__name__, template_folder="../templates", static_folder="../static")
    app.config.from_object(config[env])

    login_manager.init_app(app)
    db.init_app(app)
    mail.init_app(app)
    scheduler.init_app(app)
    scheduler.start()
    from .mail_helper import send_daily_mail
    scheduler.add_job(
        "send_daily_mail",
        send_daily_mail,
        trigger="cron",
        day="*",
        hour="7",
    )

    # log
    if not path.exists("log"):
        mkdir("log")
    formatter = RequestFormatter(
        "[%(asctime)s] %(remote_addr)s requested %(url)s %(levelname)s: %(message)s"
    )
    access_log_handler = TimedRotatingFileHandler(
        "log/access_" + datetime.now().strftime("%Y-%m-%d") + ".log",
        when="D",
        interval=1,
        backupCount=15,
        encoding="UTF-8",
        delay=False,
        utc=False,
    )
    access_log_handler.setLevel("INFO")
    access_log_handler.setFormatter(formatter)
    access_log_handler.suffix = "access_%Y-%m-%d.log"
    app.logger.addHandler(access_log_handler)

    # Blueprint
    from .main import main_bp

    app.register_blueprint(main_bp)

    from .user import user_bp

    app.register_blueprint(user_bp)

    from .admin import admin_bp

    app.register_blueprint(admin_bp)

    return app
