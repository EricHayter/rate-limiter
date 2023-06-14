from configparser import ConfigParser
from datetime import datetime, timedelta
from units import Units


'''
- ALMOST the right behaviour. for some reason we are allowd to make 1 additional
  request after the first set of cooldowns

- efficiency in reset usage
- init
- update_limits
- write usage

- calculate time isn't right atm
- what are we doing with optional arguments?
- package all the files together into one module?
- or just move enum class to this module?
- usage isn't storing at all now
- rename parse_unit to something better
- writing to files isn't quite working yet
'''

class RateLimiter:
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
            self.parse_limits()
        else:
            self.latest_time = datetime.fromisoformat(self.config['USAGE']['latest_time'])
            for key, value in self.config['USAGE'].items():
                unit = RateLimiter.parse_unit(key)
                if unit != None and value.isdigit():
                    self.usage[unit] = int(value)

    # not sure about this being in the class
    def parse_limits(self):
        for param in self.config['LIMITS']:
            if (unit := parse_unit) != None:
                self.usage[unit] = 0
            else:
                raise Exception(f'unknown time unit in LIMITS: {param}')



    def parse_unit(string: str) -> Units:
        if string == 'year':
            return Units.YEAR
        elif string == 'month':
            return Units.MONTH
        elif string == 'day':
            return Units.DAY
        elif string == 'hour':
            return Units.HOUR
        elif string == 'minute':
            return Units.MINUTE
        elif string == 'second':
            return Units.SECOND
        else:
            return None


    def update_limits(self, **kwargs):
        for key, value in kwargs.items():
            if RateLimiter.parse_unit(key) != None and value.isdigit():
                self.config['LIMITS'][key] = value
        with open(self.cfg_file, 'w') as configfile:
            self.config.write(configfile)

        
    def write_usage(self, **kwargs):
        self.config['USAGE']['latest_time'] = str(self.latest_time)
        for key, value in self.usage.items():
            self.config['USAGE'][key] = str(value)
        with open(self.cfg_file, 'w') as configfile:
            self.config.write(configfile)

                
    def request_cooldown(self):
        '''
        returns the amount of seconds until you can make another request
        '''
        for unit in self.config['LIMITS']:
            # something seems to be wrong with the if statement here
            u = RateLimiter.parse_unit(unit)
            if u != None and self.usage[u] >= int(self.config['LIMITS'][unit]):
                return self.calculate_time(unit)
        
        return 0


    def is_after(self, unit: Units) -> bool:
        '''
        if latest < current: reset
        if equal: compare usage and limit
        if latest > current: we have a serious issue XD (time travel technology)
        '''
        latest_time = self.latest_time.timetuple()
        current_time = datetime.now().timetuple()

        for i in range(unit.value):
            if current_time[i] < latest_time[i]:
                return False
        else:
            if current_time[i+1] == latest_time[i+1]:
                return False
        return True


    def reset_usage(self, unit: Units):
        # not 100% efficient as usage would be storing all params
        for u in reversed(Units):
            if u not in self.usage:
                continue
            self.usage[u] = 0
            if u == unit:
                break
        

    def calculate_time(self, unit: Units):
        next_increment = [*datetime.min.timetuple()][:6]
        for u in Units:
            next_increment[u.value] = self.latest_time.timetuple()[u.value]
        next_increment = datetime(*next_increment)

        if unit == Units.YEAR:
            next_increment += timedelta(years=1)
        elif unit == Units.MONTH:
            next_increment += timedelta(months=1)
        elif unit == Units.DAY:
            next_increment += timedelta(days=1)
        elif unit == Units.HOUR:
            next_increment += timedelta(hours=1)
        elif unit == Units.MINUTE:
            next_increment += timedelta(minutes=1)
        elif unit == Units.SECOND:
            next_increment += timedelta(seconds=1)

        return (next_increment - self.latest_time).total_seconds()


    def request(self, func):
        ''' returning the value'''
        try:
            output = func()
            for unit in self.usage:
                self.usage[unit] += 1
                if self.is_after(unit):
                    self.reset_usage(unit)

            self.latest_time = datetime.now()
        except Exception as e:
            self.write_usage()
            raise e

        return output

