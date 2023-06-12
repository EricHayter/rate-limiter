import rate_limiter
import time


def foo():
    print('foo')
    return 1

def main():
    rl = rate_limiter.RateLimiter(cfg='./limits.cfg')


    cd = rl.request_cooldown()
    
    # time.sleep(cd / 1000)

    print('calling foo')
    rl.request(foo)
    print('done calling foo')

    rl.write_usage()


if __name__ == '__main__':
    main()


