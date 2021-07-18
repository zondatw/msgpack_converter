import logging

def setup_log(project_name: str, Debug: bool):
    logger = logging.getLogger(project_name)
    logger.propagate = True
    logger.setLevel(logging.DEBUG if Debug else logging.INFO)

    # create console handler and set level to debug
    console = logging.StreamHandler()

    # create formatter
    formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(name)s: %(message)s')

    # add formatter to console
    console.setFormatter(formatter)

    # add console to logger
    logger.addHandler(console)