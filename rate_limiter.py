from configparser import ConfigParser
import datetime

'''
- creating configuration files
- rate limit dunder class
- saving used 
- logfile for errors (prob not)
'''

class RateLimiter:
    PARAMS = ['day', 'hour', 'minute', 'second']
    def __init__(self, **kwargs):
        '''
        optional argument for the config 
        '''
        self.cfg_file = kwargs['cfg']
        self.usage = dict()

        self.latest_time = datetime.datetime.now()

        if 'cfg' in kwargs:
            self.config = ConfigParser()
            self.config.read(self.cfg_file)
            if 'LIMITS' not in self.config.sections(): # might not be needed
                raise Exception('error: limits configuration file is not formatted correctly')
            # further checking needed for the input file
        else:
            self.config = ConfigParser()

    def update_limits(self, **kwargs):
        for key, value in kwargs.items():
            # type is not guarenteed need to fix that
            if key in RateLimiter.PARAMS and value.isdigit():
                self.config['LIMITS'][key] = value
            with open('example.ini', 'w') as configfile:
                self.config.write(configfile)

        
    def write_usage(self, **kwargs):
        # json object with days, minutes, etc...
        # current time
        pass
                
    def request_cooldown(self):
         
        # cases 3
        # they are in the same time period and have credits to use
        # right time period but over limit
        # need to reset time
        pass

    # this is going to be the decorator
    # wrap function in try catch
    # if the request goes through add + 1 to each of the usage params in config
    def request(self, func):
        pass
     
