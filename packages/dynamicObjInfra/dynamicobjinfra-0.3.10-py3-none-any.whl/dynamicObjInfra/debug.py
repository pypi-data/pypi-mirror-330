from dynamicObjInfra.redisClient import RedisClient
from baseObj import BaseObj
from utils.env import EnvConfig, initialize

def configureEnv():

    dbhost = "127.0.0.1"
    dbport = 27017
    chatDbName = "claro_kp"
    redisHost = "127.0.0.1"
    redisPort = 6379

    dynObjConf = EnvConfig(db_host=dbhost, db_port=dbport, db_name=chatDbName, redis_host=redisHost, redis_port=redisPort, db_useRedisCache=True)
    initialize(dynObjConf)

class A(BaseObj):
    dbCollectionName = "test"
    id :str
    name: str

configureEnv()

aIns = A(id="1", name="test")

redis = RedisClient()
redis.saveTempToDB("1", aIns)

bIns : A = redis.loadFromDB(A, "1")
print(bIns.toReadableText())