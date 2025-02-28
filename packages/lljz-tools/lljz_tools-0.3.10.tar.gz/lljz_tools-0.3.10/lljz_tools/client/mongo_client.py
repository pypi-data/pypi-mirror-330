import re
from typing import Optional

from lljz_tools.color import Color
from ..models import Model


class MongoDBConfig(Model):
    host: str
    port: int
    database: str
    username: Optional[str] = None
    password: Optional[str] = None
    


class MongoClient:
    def __init__(self, uri: str, ssh_uri: Optional[str] = None):
        self.uri = uri
        self._ssh = None
        
        self.config = self.parse_uri(uri)  # 解析 URI 得到配置
        
        # Validate URI
        self.validate_uri()

        if ssh_uri:
            from lljz_tools.client.utils import setup_ssh_tunnel
            
            self._ssh = setup_ssh_tunnel(self.config.host, self.config.port, ssh_uri)
            self.config.host = '127.0.0.1'
            self.config.port = self._ssh.local_bind_port

        self.client, self.db = self.connect_to_mongo()

    @staticmethod
    def parse_uri(uri: str):
        # 解析 URI 并返回配置字典
        pattern = r'mongodb://(?P<username>.+):(?P<password>.+)@(?P<host>.+):(?P<port>\d+)/(?P<database>[^?]+)?'
        match = re.match(pattern, uri)
        if not match:
            raise ValueError(f'Invalid MongoDB URI format: {uri}')
        
        config = match.groupdict()
        config['port'] = int(config['port'])
        return MongoDBConfig(**config)  # type: ignore
    
    def validate_uri(self):
        if not self.uri:
            raise ValueError("MongoDB URI must be specified.")

    def connect_to_mongo(self):
            
        try:
            from pymongo import MongoClient as BaseMongoClient
            
            client = BaseMongoClient(host=self.config.host, port=self.config.port, username=self.config.username, password=self.config.password)
            database = client[self.config.database]  # 获取默认数据库
            return client, database
        except ImportError:
            raise ImportError(f'package not installed! use "{Color.color('pip install pymongo', style='i u yellow')}"')
        except Exception as e:
            raise ConnectionError(f"Failed to connect to MongoDB: {e}")

    def close(self):
        if self.client:
            self.client.close()
        if self._ssh:
            self._ssh.stop()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def find_one(self, collection: str, query: dict):
        return self.db[collection].find_one(query)

    def find(self, collection: str, query: dict):
        return list(self.db[collection].find(query))

    def insert_one(self, collection: str, data: dict):
        return self.db[collection].insert_one(data)

    def insert_many(self, collection: str, data: list[dict]):
        return self.db[collection].insert_many(data)

    def update_one(self, collection: str, query: dict, data: dict):
        return self.db[collection].update_one(query, data)

    def update_many(self, collection: str, query: dict, data: dict):
        return self.db[collection].update_many(query, data)

    def delete_one(self, collection: str, query: dict):
        return self.db[collection].delete_one(query)

    def delete_many(self, collection: str, query: dict):
        return self.db[collection].delete_many(query)

