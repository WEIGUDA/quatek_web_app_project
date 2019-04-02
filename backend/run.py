import logging
import os
import sys
from logging import handlers

from app import create_app, socketio


def get_logger(file):
    logger = logging.getLogger(
        os.path.splitext(os.path.split((os.path.abspath(file)))[1])[0]
    )
    logger.setLevel(logging.INFO)
    logFormatter = logging.Formatter(
        "%(asctime)s - %(levelname)s - %(message)s"
    )
    fileHandler = handlers.RotatingFileHandler(
        "{}{}".format(os.path.splitext(os.path.abspath(file))[0], ".log"),
        maxBytes=1024 * 1024 * 1,  # 1MB
        backupCount=10,
    )
    fileHandler.setFormatter(logFormatter)

    consoleHandler = logging.StreamHandler(sys.stdout)
    consoleHandler.setFormatter(logFormatter)

    # logger.addHandler(fileHandler)
    logger.addHandler(consoleHandler)

    return logger


logger = get_logger(__file__)


if __name__ == "__main__":
    os.environ["ENV"] = "development"
    os.environ["DEBUG"] = "True"
    app = create_app()
    socketio.run(app, host="0.0.0.0", port=5001, debug=True, use_reloader=True)
