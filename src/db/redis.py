
import aioredis
from ..config import settings

JTI_EXPIRY = 3600

token_blocklist = aioredis.StrictRedis(
    host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=0
)


async def add_jti_to_blocklist(jti: str) -> None:
    await token_blocklist.set(name=jti, value="", ex=JTI_EXPIRY)


async def token_in_blocklist(jti:str) -> bool:
   jti =  await token_blocklist.get(jti)

   return jti is not None