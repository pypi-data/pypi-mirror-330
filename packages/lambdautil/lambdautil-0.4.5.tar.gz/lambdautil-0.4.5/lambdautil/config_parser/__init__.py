from configparser import ConfigParser

class CaseSensitiveConfigParser(ConfigParser):
    def optionxform(self, optionstr):
        return optionstr
