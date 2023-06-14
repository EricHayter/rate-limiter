import rate_limiter
import time
from units import Units

def foo():
    return

def main():
    for i in Units:
        print(i)
        print(i.value + 1)

#    counter = 0
#    rl = rate_limiter.RateLimiter(cfg='./limits.cfg')
#
#    start = time.time()
#    while counter < 1000:
#        if (cd := rl.request_cooldown()) > 0:
#            print(f'sleeping for {cd} seconds')
#            time.sleep(cd)
#        rl.request(foo)
#        print(f'counter: {counter}')
#        counter += 1
#
#    rl.write_usage()



if __name__ == '__main__':
    main()


