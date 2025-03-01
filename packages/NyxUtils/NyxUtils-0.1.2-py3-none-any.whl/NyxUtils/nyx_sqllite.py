import aiosqlite
import asyncio
from typing import Optional, Dict, List, Tuple, Any
import logging

logging.basicConfig(level = logging.INFO)
logger = logging.getLogger(__name__)


class NyxAsyncSQLiteDB:
    """
    使用手动连接池的异步 SQLite 封装类。
    """

    def __init__(self, db_path: str, pool_size: int = 5):
        """
        初始化数据库连接池。

        :param db_path: SQLite3 数据库文件路径。
        :param pool_size: 连接池的大小。
        """
        self.db_path = db_path
        self.pool_size = pool_size
        self.pool: Optional[asyncio.Queue] = None

    async def connect(self):
        """
        创建连接池。
        """
        if self.pool is None:
            self.pool = asyncio.Queue(maxsize = self.pool_size)
            for _ in range(self.pool_size):
                conn = await aiosqlite.connect(self.db_path)
                self.pool.put_nowait(conn)
            logger.info("Connection pool created.")

    async def close(self):
        """
        关闭连接池中的所有连接。
        """
        if self.pool is not None:
            while not self.pool.empty():
                conn = await self.pool.get()
                await conn.close()
            self.pool = None
            logger.info("Connection pool closed.")

    async def __aenter__(self):
        """
        异步上下文管理器入口。
        """
        await self.connect()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """
        异步上下文管理器出口。
        """
        await self.close()

    async def acquire_conn(self):
        """
        从连接池中获取一个连接。
        """
        if self.pool is None:
            raise RuntimeError("Connection pool is not initialized.")
        return await self.pool.get()

    async def release_conn(self, conn):
        """
        将连接放回连接池。
        """
        if self.pool is None:
            raise RuntimeError("Connection pool is not initialized.")
        await self.pool.put(conn)

    async def execute(self, query: str, params: Tuple[Any, ...] = ()) -> Dict[str, Any]:
        """
        执行 SQL 语句。

        :param query: SQL 查询语句。
        :param params: 查询参数，用于防注入。
        :return: 包含执行结果的字典，例如 {"success": True, "rowcount": 1}。
        """
        conn = await self.acquire_conn()
        try:
            cursor = await conn.execute(query, params)
            await conn.commit()
            return {"success": True, "rowcount": cursor.rowcount}
        except aiosqlite.Error as e:
            logger.error(f"An error occurred: {e}")
            return {"success": False, "error": str(e)}
        finally:
            await self.release_conn(conn)

    async def insert(self, table: str, data: Dict[str, Any]) -> Optional[int]:
        """
        插入数据。

        :param table: 表名。
        :param data: 要插入的数据字典，例如 {"name": "Alice", "age": 25}。
        :return: 插入的主键 ID，如果失败则返回 None。
        """
        columns = ", ".join(data.keys())
        placeholders = ", ".join(["?"] * len(data))
        query = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"
        params = tuple(data.values())
        result = await self.execute(query, params)
        if result["success"]:
            return result["rowcount"]
        return None

    async def query(self, table: str, where: str = "", where_params: Tuple[Any, ...] = ()) -> List[Tuple[Any, ...]]:
        """
        查询数据。

        :param table: 表名。
        :param where: WHERE 条件语句，例如 "age > ?"。
        :param where_params: WHERE 条件的参数。
        :return: 查询结果的所有行，如果出错则返回空列表。
        """
        query = f"SELECT * FROM {table}"
        if where:
            query += f" WHERE {where}"
        conn = await self.acquire_conn()
        try:
            cursor = await conn.execute(query, where_params)
            rows = await cursor.fetchall()
            return rows
        except aiosqlite.Error as e:
            logger.error(f"An error occurred: {e}")
            return []
        finally:
            await self.release_conn(conn)
