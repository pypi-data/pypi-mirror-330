from typing import List
from .redisClient import RedisClient
from .logProvider import logger
from .baseObj import BaseObj
from singleton import Singleton
from pymongo import MongoClient
from .validators import validate_base_obj_cls, validate_base_obj_instance
from .utils.env import get_config 

#TBD: add support for redis configutation

class DBClient(metaclass=Singleton):
    dbInstance = None
    useRedisCache : bool = False
    redisCache : RedisClient

    def __init__(self):
        #empty __init__ to allow external configuration
        pass

    def getDatabase(self):                
        if self.dbInstance is None:
            host = get_config().db_host
            port = get_config().db_port
            dbName = get_config().db_name   
            self.useRedisCache = get_config().db_useRedisCache
            
            logger().debug(f"DBClient: host: {host}, port: {port}, dbName: {dbName}, useRedisCache: {self.useRedisCache}")

            if (dbName is None or dbName == ""):
                logger().critical(f'DBClient was created without dbName')
                return None
            
            if (self.useRedisCache):
                self.redisCache = RedisClient()
            
            connectionString = f"mongodb://{host}:{port}/"
            client = MongoClient(connectionString, tz_aware=True)

            self.dbInstance = client[dbName]

        return self.dbInstance
    
    @validate_base_obj_instance
    def saveToDB (self, dataObj : BaseObj, filter = {}):
        db = self.getDatabase()
        collection = db[dataObj.dbCollectionName]

        if (filter == {}):
            filter = {'id': dataObj.id}
            
        collection.replace_one(filter, dataObj.serialize(), upsert=True)

        if (self.useRedisCache and dataObj.isCached):
            #update cache
            self.redisCache.saveTempToDB(dataObj=dataObj, objId=dataObj.id)

    @validate_base_obj_cls
    def deleteFromDB(self, cls, field_value, field_name: str = 'id'):
        db = self.getDatabase()
        collection = db[cls.dbCollectionName]

        query = {field_name: field_value}
        collection.delete_one(query)

        if (self.useRedisCache and cls.isCached):
            #update cache
            self.redisCache.removeFromDB(cls=cls, objId=field_value)

    @validate_base_obj_cls
    def loadFromDB(self, cls, field_value, field_name: str = 'id'):
        if (self.useRedisCache and cls.isCached):
            # see if the data is in the cache
            obj = self.redisCache.loadFromDB(cls=cls, objId=field_value)
            if (obj is not None):
                return obj

        db = self.getDatabase()
        collection = db[cls.dbCollectionName]

        query = {field_name: field_value}
        result = collection.find_one(query)

        if result:
            # Remove '_id' 
            result.pop('_id', None)
            obj : BaseObj = cls.deserialize(result)
           
            if (obj is None):
                logger().error(f'loadFromDB failed to desiralize objId {field_value}, result is {result}')
                return None

            if (self.useRedisCache and cls.isCached):
                # update cache
                self.redisCache.saveTempToDB(objId=obj.id, dataObj=obj)

            return obj
        else:
            return None
        
    # @validate_base_obj_cls
    # def loadManyFromDB(self, cls, field_name: str, field_value):
    #     db = self.getDatabase()
    #     collection = db[cls.dbCollectionName]

    #     query = {field_name: field_value}
    #     results = collection.find(query)

    #     objects = []
    #     for result in results:
    #         result.pop('_id', None)  # Remove '_id'
    #         obj = cls.deserialize(result)
    #         objects.append(obj)

    #         if (self.useRedisCache and cls.isCached):
    #             # update cache
    #             self.redisCache.saveTempToDB(objId=obj.id, dataObj=obj)

    #     return objects

    @validate_base_obj_cls
    def loadManyFromDB(self, cls, field_name: str, field_value):
        
        logger().debug(f"loadManyFromDB: {cls.dbCollectionName} where {field_name} = {field_value}, userRedisCache: {self.useRedisCache}, cls.isCached: {cls.isCached}")
        # 1) Try to retrieve cached docs from Redis.
        cached_ids = set()
        cached_docs = {}
        if self.useRedisCache and cls.isCached:
            redis_results : List[BaseObj]= self.redisCache.searchByField(cls, field_name, field_value)
            for doc in redis_results:
                cached_ids.add(doc.id)
                cached_docs[doc.id] = doc

        # 2) Fetch missing documents from the DB using $nin.
        db = self.getDatabase()
        collection = db[cls.dbCollectionName]
        query = { field_name: field_value }
        if cached_ids:
            query["id"] = {"$nin": list(cached_ids)}

        missing_docs = []
        for result in collection.find(query):
            result.pop('_id', None)
            obj = cls.deserialize(result)
            missing_docs.append(obj)
            # Update cache.
            if self.useRedisCache and cls.isCached:
                self.redisCache.saveTempToDB(objId=obj.id, dataObj=obj)

        # 3) Return merged results: cached docs + missing docs.
        all_docs = list(cached_docs.values()) + missing_docs
        return all_docs


    @validate_base_obj_cls
    def loadManyFromDBByFilter(self, cls, filter = {}):
        db = self.getDatabase()
        collection = db[cls.dbCollectionName]

        results = collection.find(filter)

        objects = []
        for result in results:
            result.pop('_id', None)  # Remove '_id'
            obj = cls.deserialize(result)
            objects.append(obj)

            if (self.useRedisCache and cls.isCached):
                # update cache
                self.redisCache.saveTempToDB(objId=obj.id, dataObj=obj)            

        return objects