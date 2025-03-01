from penvy.logger import colorlog


def get_logger(name: str, level: int):
    logger = colorlog.getLogger(name)
    logger.setLevel(level)

    cformat = "%(log_color)s" + "%(asctime)s - %(message)s"
    formatter = colorlog.ColoredFormatter(cformat, "%H:%M:%S")

    chandler = colorlog.StreamHandler()
    chandler.setFormatter(formatter)
    chandler.setLevel(level)

    logger.handlers = [chandler]

    return logger
