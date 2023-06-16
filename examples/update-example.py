import rate-limiter
import time

def main():
    with rate-limiter.RateLimiter('my_cfg.ini') as rl:
        rl.update_limits(year=2000, hour=500)

if __name__ == '__main__':
    main()
