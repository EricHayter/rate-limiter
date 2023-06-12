from configparser import ConfigParser
from datetime import datetime

'''
- creating configuration files
- rate limit dunder class
- saving used 
- logfile for errors (prob not)
- latest time isn't being saved correctly
'''

class RateLimiter:
    PARAMS = ['day', 'hour', 'minute', 'second']
    def __init__(self, **kwargs):
        '''
        optional argument for the config 
        '''
        self.usage = dict()
        # this is waiting to explode XD
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
            self.config['USAGE'] = dict()
            for param in self.config['LIMITS']:
                if param in RateLimiter.PARAMS:
                    self.usage[param] = 0
        else:
            if 'latest_time' not in self.config['USAGE']: # last_time not in cfg file???
                self.latest_time = datetime.now()
            else:
                self.latest_time = datetime.fromisoformat(self.config['USAGE']['latest_time'])
            for key, value in self.config['USAGE'].items():
                if key in RateLimiter.PARAMS and value.isdigit():
                    self.usage[key] = int(value)


    def update_limits(self, **kwargs):
        cfg_file = kwargs['cfg_file'] if 'cfg_file' in kwargs else 'limits.cfg'
        for key, value in kwargs.items():
            if key in RateLimiter.PARAMS and value.isdigit():
                self.config['LIMITS'][key] = value
        with open(cfg_file, 'w') as configfile:
            self.config.write(configfile)

        
    def write_usage(self, **kwargs):
        self.config['USAGE']['latest_time'] = str(self.latest_time)
        for key, value in self.usage.items():
            self.config['USAGE'][key] = str(value)
        with open(self.cfg_file, 'w') as configfile:
            self.config.write(configfile)

                
    def request_cooldown(self):
        '''
        returns the amount of miliseconds until you can make another request
        '''
        for unit in self.config['LIMITS']:
            if self.is_after(unit):
                self.reset_usage(unit)
                return 0
            
            # this isn't a safe operation for casting
            if self.usage[unit] >= int(self.config['LIMITS'][unit]):
                return self.calculate_time(unit)
        

        return 0

        # they are in the same time period and have credits to use
        # right time period but over limit
        # need to reset time

    def is_after(self, unit) -> bool:
        '''
        if latest < current: reset
        if equal: compare usage and limit
        if latest > current: we have a serious issue XD (time travel technology)
        '''

        # need to work down to unit
        # this could be a class variable?;
        uti = {
            'year': 0,
            'month': 1,
            'day': 2,
            'hour': 3,
            'minute': 4,
            'second': 5,
        }

        latest_time = self.latest_time.timetuple()
        current_time = datetime.now().timetuple()

        for i in range(uti['year'], uti[unit] + 1): # this isn't the cleanest
            if current_time[i] < latest_time[i]:
                return False
        else: # might be off by 1
            if current_time[i] == latest_time[i]:
                return False

        # edge case if they are equal

        return True

    def reset_usage(self, unit):
        uti = {
            'year': 0,
            'month': 1,
            'day': 2,
            'hour': 3,
            'minute': 4,
            'second': 5,
        }
        
        # chane this code to use params
        itu = {
            0: 'year',
            1: 'month',
            2: 'day',
            3: 'hour',
            4: 'minute',
            5: 'second',

        }

        for i in range(uti[unit], uti['second'] + 1):
            if itu[i] in self.usage:
                self.usage[itu[i]] = 0

        

    def calculate_time(self, unit):
        delta_time = self.latest_time - datetime.now() # difference from latest time and current time
        
        return 1000


    def request(self, func):
        ''' returning the value'''
        try:
            func()
            for unit in self.usage:
                self.usage[unit] += 1
            self.latest_time = datetime.now()
        except Exception as e:
            self.write_usage()
            raise e

