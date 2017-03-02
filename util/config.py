"""
config file loading
===================
Load configuration
"""

import traceback
from ConfigParser import ConfigParser
from datetime import datetime

from singleton import singleton

__all__ = ['ConfigLoader']


class ConfigMap:
    """
    store each config member as an attribute
    """

    def __init__(self):
        pass

    def __setattr__(self, name, value):
        self.__dict__[name] = value

    def __getattribute__(self, name):
        return self.__dict__[name]

    def __getattr__(self, name):
        return None

    def __iter__(self):
        for k in self.__dict__:
            yield k

    def __str__(self):
        return str(self.__dict__)


@singleton
class ConfigLoader:
    def __init__(self, path=None):
        if path:
            self._config_parser = ConfigParser()
            self._config_parser.read(path)
            self._system_config = ConfigMap()
            self._experiment_config = ConfigMap()
            self._model_config = ConfigMap()
            self._gridsearch_config = ConfigMap()
            self._init_system_config()
            self._init_exp_config()
            self._init_model_config()
            self._init_gridsearch_config()
            self._mode = None

    def _init_system_config(self):
        """
        init system config
        :return:
        """
        cf = self._system_config
        get_param = lambda x: self._config_parser.get('system', x)
        try:
            cf.log_level = get_param('log_level')
            cf.index_path = get_param('index_path')
            cf.fund_path = get_param('fund_path')
            cf.macro_path = get_param('macro_path')
            cf.output_path = get_param('output_path')
        except:
            traceback.print_exc()

    def _init_exp_config(self):
        """
        init running config
        :return:
        """
        cf = self._experiment_config
        get_param = lambda x: self._config_parser.get('experiment', x)
        try:
            get_start_end = lambda x : \
                [datetime(*[int(x) for x in date.split('/')])
                 for date in eval(get_param(x))]

            cf.invest_cycle = eval(get_param('invest_cycle'))
            cf.general_start_end = get_start_end('general_start_end')
            cf.backtest_start_end = get_start_end('backtest_start_end')
        except:
            traceback.print_exc()

    def _init_model_config(self):
        """
        init model config
        :return:
        """
        cf = self._model_config
        get_param = lambda x: self._config_parser.get('model', x)
        try:
            cf.talib_period = eval(get_param('talib_period'))
        except:
            traceback.print_exc()

    def _init_gridsearch_config(self):
        """
        init grid search config
        :return:
        """
        cf = self._gridsearch_config
        get_param = lambda x: self._config_parser.get('gridsearch', x)
        try:
            cf.lookback_window_list = eval(get_param('lookback_window'))
            cf.risk_thres_list = eval(get_param('risk_thres'))
            cf.adjust_thres_list = eval(get_param('adjust_thres'))
        except:
            traceback.print_exc()

    def __getattribute__(self, item):
        pass

    def __getattr__(self, item):
        if item == 'system':
            return self._system_config
        elif item == 'experiment':
            return self._experiment_config
        elif item == 'model':
            return self._model_config
        elif item == 'gridsearch':
            return self._gridsearch_config

    def __str__(self):
        form = "{system_config: %s, exp_config: %s, model_config: %s, gridsearch_config: %s}"
        return form % (str(self._system_config),
                       str(self._experiment_config),
                       str(self._model_config),
                       str(self._gridsearch_config)
                       )

if __name__ == '__main__':
    print ConfigLoader('../backtest.ini')
