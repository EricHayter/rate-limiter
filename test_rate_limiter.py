import rate_limiter

rl = rate_limiter.RateLimiter(cfg='./limits.cfg')

rl.update_limits(day = '1400')
