import rate_limiter
import time


@rate_limiter.request
def foo():
    return 1

def main():
    rl = rate_limiter.RateLimiter(cfg='./limits.cfg')


    cd = rl.request_cooldown()
    print(cd)
    time.sleep(cd / 1000)

    foo()

    rl.write_usage()


if __name__ == '__main__':
    main()


