from cistell import ConfigField

from pynenc.conf.config_base import ConfigPynencBase


class ConfigRedis(ConfigPynencBase):
    """
    Specific Configuration for any Redis client.

    This class provides configuration settings specific to Redis clients, allowing
    for customization of the Redis connection used in the system.

    :cvar ConfigField[str] redis_host:
        The hostname of the Redis server. Defaults to 'localhost', specifying that
        the Redis server is expected to be running on the same machine as the client.

    :cvar ConfigField[int] redis_port:
        The port number on which the Redis server is listening. Defaults to 6379,
        which is the default port for Redis.

    :cvar ConfigField[int] redis_db:
        The database number to connect to on the Redis server. Redis servers typically
        support multiple databases (numbered from 0), allowing different applications
        or parts of an application to operate in separate data spaces. Defaults to 0.

    Example usage of the `ConfigRedis` class involves initializing it with specific
    values for host, port, and database, or relying on the defaults for a standard
    Redis setup.
    """

    redis_host = ConfigField("localhost")
    redis_port = ConfigField(6379)
    redis_db = ConfigField(0)
