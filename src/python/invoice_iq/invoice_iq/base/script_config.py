from pathlib import Path

from configparser import ConfigParser

class ConfigReader:
    '''
    Config parser class to read configuration file
    '''
    def __init__(self, script_name) -> None:
        assert script_name is not None
        self.script_name = script_name
        self._config_path = None
        self._config = None
        
    @property
    def get_config(self):
        '''
        get the file path for the config file
        '''
        cur_dir = Path(__file__).absolute()
        project_base = cur_dir.parent
        config_folder = Path(project_base).joinpath('config')
        config_file = Path(config_folder).joinpath('project_master.config')
        return config_file
    
    def parser(self):
        '''
        Create a config parser instance and read config file
        '''
        if self._config is None:
            self._config = ConfigParser(self.script_name)
            self._config.read(self.get_config)
        return self._config
    
    def get_common_section(self, key):
        return self._config.get('common',key)
    
    def get_section(self, section, key):
        return self._config.get(section, key)
    
    def get_boolean(self, section, key)->bool:
        return self._config.getboolean(section, key)
        
    
        