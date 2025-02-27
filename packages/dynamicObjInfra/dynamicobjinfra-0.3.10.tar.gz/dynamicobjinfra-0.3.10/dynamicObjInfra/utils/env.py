from dataclasses import dataclass
from dynamicObjInfra.enums import TTL_Type

@dataclass
class EnvConfig:
    db_host: str = "localhost"
    db_port: int = 27017
    db_name: str = None
    db_useRedisCache: bool = False
    redis_host: str = "localhost"
    redis_port: int = 6379
    cache_short_ttl: int = 300
    cache_long_ttl: int = 1800
    cache_extra_long_ttl: int = 86400

_GLOBAL_CONFIG: EnvConfig | None = None

def initialize(config: EnvConfig) -> None:
    """
    Store a global config object for use elsewhere in the package.
    Must be called once by the application.
    """
    global _GLOBAL_CONFIG
    _GLOBAL_CONFIG = config

def get_config() -> EnvConfig:
    """
    Return the global config, or raise an error if not initialized yet.
    """
    if _GLOBAL_CONFIG is None:
        raise RuntimeError("InfraConfig is not initialized. Call initialize(...) first.")
    return _GLOBAL_CONFIG

def get_ttl_by_type(ttlType : TTL_Type):
    if (ttlType == TTL_Type.SHORT):
        return get_config().cache_short_ttl
    elif (ttlType == TTL_Type.LONG):
        return get_config().cache_long_ttl
    elif (ttlType == TTL_Type.EXTRA_LONG):
        return get_config().cache_extra_long_ttl        
    
    return None
