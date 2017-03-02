from singleton import singleton
from timeutil import datetime
import json

@singleton
class Logger:
    def __init__(self, logfile=None, level=None):
        """
        :param logfile: log file path
        :param level: "INFO", "DEBUG", "WARNING", "ERROR"
        :return:
        """
        if logfile:
            self._logFile = logfile
        else:
            self._logFile = './log'
        if level:
            assert (level == 'INFO' or level == 'DEBUG' or
                    level == 'WARNING' or level == 'ERROR')
            self._level = level
        else:
            self._level = "INFO"
        self._log_init()

    def _log_init(self):
        import logging
        self._logger = logging.getLogger("myLogger")
        self._logger.setLevel(logging.DEBUG)
        filehandlerinfo = logging.FileHandler(self._logFile)
        if self._level == "DEBUG":
            filehandlerinfo.setLevel(logging.DEBUG)
        elif self._level == "INFO":
            filehandlerinfo.setLevel(logging.INFO)
        elif self._level == "WARNING":
            filehandlerinfo.setLevel(logging.WARNING)
        elif self._level == "ERROR":
            filehandlerinfo.setLevel(logging.ERROR)
        # streamHandler = logging.StreamHandler()
        # streamHandler.setLevel(logging.DEBUG)
        self._logger.addHandler(filehandlerinfo)
        # self._logger.addHandler(streamHandler)

    def info(self, **args):
        self._logger.info(json.dumps({'level': 'INFO',
                                      'system_time': str(datetime.now()),
                                      'content': args}))

    def debug(self, **args):
        self._logger.debug(json.dumps({'level': 'DEBUG',
                                       'system_time': str(datetime.now()),
                                       'content': args}))

    def warning(self, **args):
        self._logger.warning(json.dumps({'level': 'WARNING',
                                         'system_time': str(datetime.now()),
                                         'content': args}))

    def error(self, **args):
        self._logger.error(json.dumps({'level': 'ERROR',
                                       'system_time': str(datetime.now()),
                                       'content': args}))

if __name__ == '__main__':
    logger = Logger()
    logger.init('./log')
    logger.error(information="wrong!")
