import rate_limiter
import time

def foo():
    return

def main():
    counter = 0
    rl = rate_limiter.RateLimiter(cfg='./limits.cfg')

    start = time.time()
    while counter < 1000:
        time.sleep(rl.request_cooldown())
        rl.request(foo)
        print(f'counter: {counter}')
        counter += 1

    print(cd)

    print(start - time.time())
    rl.write_usage()



if __name__ == '__main__':
    main()


