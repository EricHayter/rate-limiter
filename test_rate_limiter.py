import rate_limiter
import time


def foo():
    return 1

def main():
    rl = rate_limiter.RateLimiter(cfg='./limits.cfg')

    start = time.time()
    while rl.request_cooldown() == 0:
        rl.request(foo)

    print(start - time.time())
    rl.write_usage()



if __name__ == '__main__':
    main()


