import re
from typing import Optional

from lljz_tools.color import Color
from lljz_tools.models import Model


class RedisConfig(Model):
    host: [str]
    port: int
    database: int
    username: Optional[str] = None
    password: Optional[str] = None


class RedisClient(Redis):
    def __init__(self, uri: str, ssh_uri: Optional[str] = None):
        self.uri = uri
        self._ssh = None

        self.config = self.parse_uri(uri)  # 解析 URI 得到配置

        # Validate URI
        self.validate_uri()

        if ssh_uri:
            try:
                from lljz_tools.client.utils import setup_ssh_tunnel
            except ImportError:
                raise ImportError(
                    f'package not installed! use "{Color.color('pip install sshtunnel', style='i u yellow')}"')

            self._ssh = setup_ssh_tunnel(self.config.host, self.config.port, ssh_uri)
            self.config.host = '127.0.0.1'
            self.config.port = self._ssh.local_bind_port

        self._redis = self.connect_to_redis()

    @staticmethod
    def parse_uri(uri: str):
        # 解析 URI 并返回配置字典
        pattern = r'redis://(((?P<username>.+):)?(?P<password>.+)@)?(?P<host>.+):(?P<port>\d+)/(?P<database>\d+)?'
        match = re.match(pattern, uri)
        if not match:
            raise ValueError(f'Invalid Redis URI format: {uri}')

        config = match.groupdict()
        config['port'] = int(config['port'])
        config['database'] = int(config['database'])
        return RedisConfig(**config)  # type: ignore

    def validate_uri(self):
        if not self.uri:
            raise ValueError("Redis URI must be specified.")

    def connect_to_redis(self):

        try:
            from redis import Redis

            client = Redis(
                host=self.config.host,
                port=self.config.port,
                username=self.config.username,
                password=self.config.password,
                decode_responses=True,
            )
            return client
        except ImportError:
            raise ImportError(
                f'package not installed! use "{Color.color('pip install redis', style='i u yellow')}"')
        except Exception as e:
            raise ConnectionError(f"Failed to connect to MongoDB: {e}")

    def close(self):
        if self._redis:
            self._redis.close()
        if self._ssh:
            self._ssh.stop()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def get(self, key):
        return self._redis.get(key)

    def set(self, key, value):
        return self._redis.set(key, value)


if __name__ == '__main__':
    c = RedisClient.parse_uri('redis://123456@192.168.1.220:6379/0')
    print(c)