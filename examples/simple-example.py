import rate_limiter
import time

def foo():
    return


def main():
    num_requests = 50
    with rate_limiter.RateLimiter(cfg='./limits.cfg') as rl:
        for _ in range(num_requests):
            time.sleep(rl.cooldown())
            rl.request(foo)

if __name__ == '__main__':
    main()
