# rate-limiter
rate-limiter is a simple python module for all of your python rate-limting needs. 

### using rate-limiter
To get started with the rate-limiter module you can create a simple configuration file by either writting it yourself or allowing the module to create a file for you. After a configuration file has been created you are ready to go! Here is a quick demo of rate-limiter in action:
``` python
import rate-limiter
import time

with rate-limiter.RateLimiter('my-cfg.cfg') as rl:
   time.sleep(rl.cooldown())
   rl.request(my_func, 'foo', my_num=3)
```

### configuration files
configuration files will include two sections: limits and usage. the limits section of the configuration file will contain units of time: years, months, days, hours, minutes, and seconds with the maximum amount of requests that can be made during each period of time.

configuration files will also include the usage section which will keep track of the amount of requests that have been made and the time of the latest request.

here is an example configuration file:
``` ini
[LIMITS]
day = 1000
minute = 10

[USAGE]
day = 400
minute = 5
latest_time = 2023-06-15 16:30:00.002020
```

In this example, the user has set a limit of 1000 daily requests and 10 requests per minute. The configuration file also shows that the user has used 400 of their 1000 daily requests but the user has used 5 of their requests for the minute.

To create a configuration file using the module try:
``` python
import rate-limiter

with rate-limiter.RateLimiter() as rl:
    rl.update_limits(day=300, minute=8)
```

### examples
further code and configuration examples can be found in the ``examples/`` directory.
