from redis import Redis

from app.config.settings import REDIS_HOST, REDIS_PORT

redis = Redis(host=REDIS_HOST, port=REDIS_PORT, db=0)