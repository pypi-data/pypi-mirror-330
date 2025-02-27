from redis.cluster import RedisCluster, ClusterNode
from redis import Redis
from typing import List, Tuple, Union

from redis.cluster import RedisCluster
from ..redis.keys import TaskStatus

class RedisClientUtil:
    """The RedisClientUtil class is used to initialize a redis connection and operate on the redis server.
    """
    def __init__(self, cluster_mode: bool = False, redis_url: str = "localhost:6379", redis_cluster_nodes: List[str] = "", ttl: int = 7 * 24 * 60 * 60):
        """Init redis connection and set ttl

        Args:
            cluster_mode (bool, optional): true if the server uses Redis Cluster. Defaults to False.
            redis_url (_type_, optional): Defaults to "localhost:6379".
            redis_cluster_nodes (List[str], optional): Defaults to "".
            ttl (int, optional): Time To Live. Defaults to 7*24*60*60.
        """
        self.ttl = ttl  # Default ttl 7 days
        self._cluster_mode = cluster_mode
        self._redis_url = redis_url
        self._redis_cluster_nodes = redis_cluster_nodes
        
        self.conn = self.__connect__()
        print(f"Redis connection {self.conn}")
        if self.conn is None:
            print("Redis connection failure. cannot cache result result")

    def get_redis_data(self, key: str) -> dict:
        """ Get result from redis

        Args:
            key (str): _description_

        Returns:
            dict: _description_
        """
        data = self.hgetall(key)
        if data:
            data = {key.decode("utf-8"): value for key, value in data.items()}
            try:
                return data
            except:
                return {}
        return {}
    
    def hmset(self, key: str, value: dict, expiry: int = 300):
        """ Set result to redis by hmset

        Args:
            key (str): redis key
            value (dict): redis data. Must be in Dict format
            expiry (_type_, optional): _description_. Defaults to None.
        """
        if expiry is None:
            expiry = self.ttl
        if self.conn:
            self.conn.hmset(key, value)
            self.conn.expire(key, expiry)
    
    def hset(self, key: str, value: dict, expiry: int = 300):
        """ Set result to redis by hset

        Args:
            key (str): redis key
            value (dict): redis data. Must be in Dict format
            expiry (_type_, optional): _description_. Defaults to None.
        """
        if expiry is None:
            expiry = self.ttl
        if self.conn:
            for hset_key, hset_value in value.items():
                self.conn.hset(name=key, key=hset_key, value=hset_value)
            self.conn.expire(key, expiry)

    def hgetall(self, key: str) -> dict:
        """ Get result from redis

        Args:
            key (str): redis key

        Returns:
            dict: result from redis
        """
        if self.conn:
            return self.conn.hgetall(key)
        return {}

    def __connect__(self) -> Union[Redis, RedisCluster]:
        """Connect to redis server based on cluster mode

        Returns:
            RedisCluster: _description_
        """
        if self._cluster_mode == True:
            nodes = []
            for url in self._redis_cluster_nodes:
                host, port = self.__parse_location(url)
                nodes.append(ClusterNode(host=host, port=port))
            return RedisCluster(startup_nodes=nodes, decode_responses=True)
        return Redis.from_url(self._redis_url)
    
    @staticmethod
    def __parse_location(path: str) -> Tuple[str, str]:
        """ Parse redis path to get host and port

        Args:
            path (str): url

        Raises:
            Exception: Invalid redis path

        Returns:
            Tuple[str, str]: Host and port
        """
        parts = path.split(":")
        if len(parts) < 2:
            raise Exception("Invalid redis path")
        return parts[0], parts[1]
    
    
class RedisTaskUtil(RedisClientUtil):
    def update_task(self, key: str, device_tokens: List[str], user_id: str, status: str, result: str, expiry: int = 300):
        """ Upsert task's data to redis

        Args:
            key (str): task id
            device_tokens (List[str]): 
            user_id (str): 
            status (str): status of task. Might be pending, in_process, done, failed, cancelled
            result (str): the result of task
            expiry (int, optional): _description_. Defaults to 300.
        """
        redis_data = {}
        redis_data["status"] = status
        redis_data["device_tokens"] = device_tokens if device_tokens else []
        redis_data["user_id"] = user_id if user_id else ""
        redis_data["result"] = result if result else ""
        self.hset(key, redis_data, expiry)

    def get_result(self, key: str) -> dict:
        """ Get result from redis

        Args:
            key (str): redis key

        Returns:
            dict: Task result from redis in dict format
        """
        data = self.hgetall(key)
        if data:
            data = {key.decode("utf-8"): value for key, value in data.items()}
            try:
                task_status = int(data["status"].decode("utf-8"))
                return dict(status=TaskStatus(task_status), result=data["result"])
            except:
                return {}
        return {}
    
    def init_task(self, task_id: str, task_data: dict):
        """ Init task in redis & set status to pending

        Args:
            task_id (str): _description_
            device_tokens (List[str]): _description_
            task_info (dict): _description_
        """
        self.hset(task_id, task_data)

    def start_process_task(self, task_id: str):
        """ Set task status to in_process

        Args:
            task_id (str): redis key
            device_tokens (str):
        """
        self.update_task(task_id, status=TaskStatus.in_process.value)
        
    def fail_task(self, task_id: str):
        """ Set task status to fail

        Args:
            task_id (str): redis key
            device_tokens (List[str]): device tokens
        """
        self.update_task(task_id, status=TaskStatus.failed.value)

    def cancel_process_task(self, task_id: str):
        """ Set task status to cancelled

        Args:
            task_id (str): redis key
            device_tokens (str): 
        """
        self.update_task(task_id, status=TaskStatus.cancelled.value)

    def done_task(self, task_id: str, device_tokens: List[str], result_url: str = ""):
        """ Set task status to done and add result_url
        
        Args:
            task_id (str): redis key
            device_tokens (List[str]): 
            result_url (str, optional): The Public URL of the result. Defaults to "".
        """
        print(f"Redis finished task {task_id} {TaskStatus.done.value}")
        self.update_task(task_id, device_tokens=device_tokens, status=TaskStatus.done.value, result=result_url)

    def is_cancelled_task(self, task_id: str) -> bool:
        """ Check if task is cancelled

        Args:
            task_id (str): redis key

        Returns:
            bool: if task is cancelled -> True, else -> False
        """
        task_data = self.get_result(task_id)
        if hasattr(task_data, "status"):
            return task_data["status"].value == TaskStatus.cancelled.value
        return False

    def is_done_task(self, task_id: str) -> bool:
        """ Check if task is done

        Args:
            task_id (str): redis key

        Returns:
            bool: if task is done -> True, else -> False
        """
        task_data = self.get_result(task_id)
        if hasattr(task_data, "status"):
            return task_data["status"].value == TaskStatus.done.value
        return False
