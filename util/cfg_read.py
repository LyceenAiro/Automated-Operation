from os import path
import sys
from configparser import ConfigParser

from util.log import _log

from importlib import import_module


# Read config.cfg
class Config:

    def __init__(self):
        self.cfg = ConfigParser()
        if not path.exists('config.cfg'):
            self._create()
            _log._ERROR('config.cfg not found, the program will try to generate a new one.\n')
            input('Press enter to continue.')
            sys.exit(1)

        self.app_language = self._read()
        
        language = getattr(import_module("lang.language", package="lang"), self.app_language)
        _log._INFO(language.cfg_read_success)


    def _create(self):
        _cfg = open('config.cfg', 'w', encoding='utf-8')
        _cfg.write(
            '[app]\n'
            'language = zh_cn\n'
        )
        _cfg.close()

    def _read(self):
        self.cfg.read('config.cfg', encoding='utf-8')
        app_language = self.cfg.get('app', 'language')

        if not len(app_language) == 5 and not '_' in app_language:
            _log._ERROR('Language setting error.\n')
            input('Press enter to continue.')

        return app_language

cfg = Config()
