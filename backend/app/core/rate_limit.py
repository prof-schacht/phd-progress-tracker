from datetime import datetime, timedelta
from typing import Callable
from fastapi import HTTPException, Request, status
from fastapi.responses import Response
import redis.asyncio as redis
from app.core.config import settings


class RateLimiter:
    def __init__(
        self,
        times: int = 5,
        minutes: int = 15,
        key_prefix: str = "rate_limit"
    ):
        self.times = times
        self.minutes = minutes
        self.key_prefix = key_prefix
        self.redis_client = None
    
    async def get_redis(self):
        if not self.redis_client:
            self.redis_client = await redis.from_url(
                settings.REDIS_URL,
                encoding="utf-8",
                decode_responses=True
            )
        return self.redis_client
    
    async def __call__(self, request: Request, response: Response):
        redis_client = await self.get_redis()
        
        # Get client IP
        client_ip = request.client.host
        key = f"{self.key_prefix}:{request.url.path}:{client_ip}"
        
        try:
            # Get current count
            current = await redis_client.get(key)
            
            if current is None:
                # First request
                pipe = redis_client.pipeline()
                pipe.incr(key, 1)
                pipe.expire(key, self.minutes * 60)
                await pipe.execute()
                
                response.headers["X-RateLimit-Limit"] = str(self.times)
                response.headers["X-RateLimit-Remaining"] = str(self.times - 1)
                response.headers["X-RateLimit-Reset"] = str(
                    int((datetime.now() + timedelta(minutes=self.minutes)).timestamp())
                )
                return True
            
            current_count = int(current)
            
            if current_count >= self.times:
                # Rate limit exceeded
                ttl = await redis_client.ttl(key)
                raise HTTPException(
                    status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                    detail=f"Rate limit exceeded. Try again in {ttl} seconds."
                )
            
            # Increment counter
            new_count = await redis_client.incr(key)
            ttl = await redis_client.ttl(key)
            
            response.headers["X-RateLimit-Limit"] = str(self.times)
            response.headers["X-RateLimit-Remaining"] = str(self.times - new_count)
            response.headers["X-RateLimit-Reset"] = str(
                int((datetime.now() + timedelta(seconds=ttl)).timestamp())
            )
            
            return True
            
        except redis.RedisError:
            # If Redis is down, allow the request but log warning
            print("Warning: Redis unavailable for rate limiting")
            return True


# Create rate limiters for different endpoints
auth_rate_limiter = RateLimiter(times=5, minutes=15, key_prefix="auth")
api_rate_limiter = RateLimiter(times=100, minutes=1, key_prefix="api")