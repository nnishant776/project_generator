'''
Implementation for logger
'''
import logging
import os


def get_logger(module_name: str, stream: logging.Handler = None) -> logging.Logger:
    '''
    Return a configured logger
    '''
    logger = logging.getLogger(module_name)
    if stream is None:
        stream = logging.StreamHandler()
    log_formatter = logging.Formatter(
        "%(asctime)s; %(levelname)s; %(name)s; %(message)s")
    stream.setFormatter(log_formatter)
    logger.addHandler(stream)

    logger.setLevel(_get_log_level_from_env())

    return logger


def _get_log_level_from_env():
    '''
    Return logging level based on environment variable 'LOG_LVL'
    '''
    env_lvl_str = os.getenv('LOG_LVL')
    if env_lvl_str is not None:
        env_lvl_str = env_lvl_str.upper()

    if env_lvl_str == 'DEBUG':
        return logging.DEBUG
    if env_lvl_str == 'WARN':
        return logging.WARN
    if env_lvl_str == 'ERROR':
        return logging.ERROR
    if env_lvl_str == 'FATAL':
        return logging.FATAL
    if env_lvl_str == 'CRITICAL':
        return logging.CRITICAL
    return logging.INFO
