from configparser import ConfigParser
from datetime import datetime

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
        if 'cfg' not in kwargs:
            self.config = ConfigParser()
            self.latest_time = datetime.now()
            return

        self.cfg_file = kwargs['cfg']  
        self.config = ConfigParser()
        self.config.read(self.cfg_file)
        if 'LIMITS' not in self.config.sections(): # might not be needed
            raise Exception('error: limits configuration file is not formatted correctly')

        if 'USAGE' not in self.config.sections():
            self.latest_time = datetime.now()
            for param in self.config['LIMITS']:
                self.config['USAGE'] = dict()
                if param in RateLimiter.PARAMS and param in self.config['LIMITS']:
                    self.config['USAGE'][param] = '0'
        else:
            if 'last_time' not in self.config['USAGE']: # should I even worry about this edge case?
                self.latest_time = datetime.now()
            else:
                self.latest_time = datetime.fromisoformat(self.config['USAGE']['last_time'])
            for key, value in self.config['USAGE'].items():
                if param in RateLimiter.PARAMS and value.isdigit():
                    self.config['USAGE'][key] = int(value)


    def update_limits(self, **kwargs):
        cfg_file = kwargs['cfg_file'] if 'cfg_file' in kwargs else 'limits.cfg'
        for key, value in kwargs.items():
            if key in RateLimiter.PARAMS and value.isdigit():
                self.config['LIMITS'][key] = value
        with open(cfg_file, 'w') as configfile:
            self.config.write(configfile)

        
    def write_usage(self, **kwargs):
        with open(cfg_file, 'w') as configfile:
            self.config.write(configfile)

                
    def request_cooldown(self):
        '''
        returns the amount of miliseconds until you can make another request
        '''

        # where does the resetting of usage come from?


        for unit in self.config['LIMITS']:
        # need to check time before even checking limits and usages
            if self.compare_time(unit) > 0:
                print('resetting')
                # reset the usage up to that unit
                return 0
            

            if self.config['USAGE'][unit] >= self.config['LIMIT'][unit]:
                return calculate_time(unit)
        

        return 0

        # they are in the same time period and have credits to use
        # right time period but over limit
        # need to reset time

    def compare_time(self, unit) -> int:
        '''
        if latest < current: reset
        if equal: compare usage and limit
        if latest > current: we have a serious issue XD (time travel technology)
        '''
        latest_time = self.latest_time.timetuple()
        current_time = datetime.now().timetuple()
        
        if unit == 'day':
            return latest_time.tm_mday - current_time.tm_mday
        elif unit == 'hour':
            return latest_time.tm_hour - current_time.tm_hour
        elif unit == 'minute':
            return latest_time.tm_min - current_time.tm_min
        elif unit == 'second':
            return latest_time.tm_sec - current_time.tm_sec
        else:
            raise Exception('invalid time unit given')


    def calculate_time(self, unit):
        delta_time = self.latest_time - datetime.now() # difference from latest time and current time
        
        pass

    # this is going to be the decorator
    # wrap function in try catch
    # if the request goes through add + 1 to each of the usage params in config
def request(func):
    def call(self, *args, **kwargs):
        try:
            func()
            for key, value in self.config['USAGE'].items():
                if isinstance(value, int):
                    self.config['USAGE'] = key + 1
            self.latest_time = datetime.now()
        except e:
            self.write_usage()
            yield e
    return call
