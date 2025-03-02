from inspy_logger import InspyLogger, Loggable


ROOT_LOGGER = InspyLogger('EasyExitCalls', console_level='info', no_file_logging=True)

LOG_LEVELS = ROOT_LOGGER.LEVELS

__all__ = [
    'Loggable',
    'LOG_LEVELS',
    'ROOT_LOGGER'
]
