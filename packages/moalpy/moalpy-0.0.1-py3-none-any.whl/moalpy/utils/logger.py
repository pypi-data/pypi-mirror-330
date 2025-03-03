
import logging


class Logger:

    @staticmethod
    def create(name, format_str=None):
        logger = logging.getLogger(name)
        logger.setLevel(logging.INFO)
        if format_str is None:
            formatter = logging.Formatter('%(asctime)s, %(levelname)s, %(name)s: %(message)s',
                                          datefmt="%Y/%m/%d %I:%M:%S %p")
        else:
            formatter = logging.Formatter(format_str, datefmt="%Y/%m/%d %I:%M:%S %p")
        handler = logging.StreamHandler()
        handler.setFormatter(formatter)

        if not logger.hasHandlers():
            logger.addHandler(handler)

        return logger
