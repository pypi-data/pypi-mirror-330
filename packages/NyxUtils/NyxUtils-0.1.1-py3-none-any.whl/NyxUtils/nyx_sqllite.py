import sqlite3
import aiosqlite
from typing import List, Tuple, Any, Dict, Optional, Union
import asyncio


class NyxSQLiteDB:

    def __init__(self, db_path: str):
        """
        初始化数据库连接
        :param db_path: 数据库文件路径
        """
        self.db_path = db_path

    def _sync_execute(self, query: str, params: Tuple[Any, ...] = None) -> Optional[sqlite3.Cursor]:
        """
        同步执行 SQL 语句
        :param query: SQL 查询语句
        :param params: 查询参数
        :return: 游标对象
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                if params:
                    cursor.execute(query, params)
                else:
                    cursor.execute(query)
                conn.commit()
                return cursor
        except sqlite3.Error as e:
            print(f"Error executing sync query: {e}")
            return None

    async def _async_execute(self, query: str, params: Tuple[Any, ...] = None) -> Optional[aiosqlite.Cursor]:
        """
        异步执行 SQL 语句
        :param query: SQL 查询语句
        :param params: 查询参数
        :return: 游标对象
        """
        try:
            async with aiosqlite.connect(self.db_path) as conn:
                cursor = await conn.execute(query, params)
                await conn.commit()
                return cursor
        except aiosqlite.Error as e:
            print(f"Error executing async query: {e}")
            return None

    def execute(self, query: str, params: Tuple[Any, ...] = None) -> Optional[Union[sqlite3.Cursor, aiosqlite.Cursor]]:
        """
        动态选择同步或异步执行 SQL 语句
        :param query: SQL 查询语句
        :param params: 查询参数
        :return: 游标对象
        """
        if asyncio.iscoroutinefunction(self.execute):
            return self._async_execute(query, params)
        else:
            return self._sync_execute(query, params)

    def fetch_one(self, query: str, params: Tuple[Any, ...] = None) -> Optional[Tuple[Any, ...]]:
        """
        动态选择同步或异步查询单条记录
        :param query: SQL 查询语句
        :param params: 查询参数
        :return: 单条记录
        """
        if asyncio.iscoroutinefunction(self.fetch_one):
            return self._async_fetch_one(query, params)
        else:
            return self._sync_fetch_one(query, params)

    def fetch_all(self, query: str, params: Tuple[Any, ...] = None) -> List[Tuple[Any, ...]]:
        """
        动态选择同步或异步查询所有记录
        :param query: SQL 查询语句
        :param params: 查询参数
        :return: 所有记录
        """
        if asyncio.iscoroutinefunction(self.fetch_all):
            return self._async_fetch_all(query, params)
        else:
            return self._sync_fetch_all(query, params)

    def _sync_fetch_one(self, query: str, params: Tuple[Any, ...] = None) -> Optional[Tuple[Any, ...]]:
        """
        同步查询单条记录
        :param query: SQL 查询语句
        :param params: 查询参数
        :return: 单条记录
        """
        cursor = self._sync_execute(query, params)
        if cursor:
            return cursor.fetchone()
        return None

    async def _async_fetch_one(self, query: str, params: Tuple[Any, ...] = None) -> Optional[Tuple[Any, ...]]:
        """
        异步查询单条记录
        :param query: SQL 查询语句
        :param params: 查询参数
        :return: 单条记录
        """
        cursor = await self._async_execute(query, params)
        if cursor:
            return await cursor.fetchone()
        return None

    def _sync_fetch_all(self, query: str, params: Tuple[Any, ...] = None) -> List[Tuple[Any, ...]]:
        """
        同步查询所有记录
        :param query: SQL 查询语句
        :param params: 查询参数
        :return: 所有记录
        """
        cursor = self._sync_execute(query, params)
        if cursor:
            return cursor.fetchall()
        return []

    async def _async_fetch_all(self, query: str, params: Tuple[Any, ...] = None) -> List[Tuple[Any, ...]]:
        """
        异步查询所有记录
        :param query: SQL 查询语句
        :param params: 查询参数
        :return: 所有记录
        """
        cursor = await self._async_execute(query, params)
        if cursor:
            return await cursor.fetchall()
        return []

    def insert(self, table: str, data: Dict[str, Any]) -> Optional[int]:
        """
        动态选择同步或异步插入一条记录
        :param table: 表名
        :param data: 插入的数据（字典形式）
        :return: 插入的行 ID
        """
        if asyncio.iscoroutinefunction(self.insert):
            return self._async_insert(table, data)
        else:
            return self._sync_insert(table, data)

    def _sync_insert(self, table: str, data: Dict[str, Any]) -> Optional[int]:
        """
        同步插入一条记录
        :param table: 表名
        :param data: 插入的数据（字典形式）
        :return: 插入的行 ID
        """
        columns = ', '.join(data.keys())
        placeholders = ', '.join(['?'] * len(data))
        query = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"
        params = tuple(data.values())
        cursor = self._sync_execute(query, params)
        if cursor:
            return cursor.lastrowid
        return None

    async def _async_insert(self, table: str, data: Dict[str, Any]) -> Optional[int]:
        """
        异步插入一条记录
        :param table: 表名
        :param data: 插入的数据（字典形式）
        :return: 插入的行 ID
        """
        columns = ', '.join(data.keys())
        placeholders = ', '.join(['?'] * len(data))
        query = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"
        params = tuple(data.values())
        cursor = await self._async_execute(query, params)
        if cursor:
            return cursor.lastrowid
        return None

    def batch_insert(self, table: str, data: List[Dict[str, Any]]) -> bool:
        """
        动态选择同步或异步批量插入记录
        :param table: 表名
        :param data: 插入的数据列表（字典形式）
        :return: 是否插入成功
        """
        if asyncio.iscoroutinefunction(self.batch_insert):
            return self._async_batch_insert(table, data)
        else:
            return self._sync_batch_insert(table, data)

    def _sync_batch_insert(self, table: str, data: List[Dict[str, Any]]) -> bool:
        """
        同步批量插入记录
        :param table: 表名
        :param data: 插入的数据列表（字典形式）
        :return: 是否插入成功
        """
        if not data:
            return False
        columns = ', '.join(data[0].keys())
        placeholders = ', '.join(['?'] * len(data[0]))
        query = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"
        params = [tuple(item.values()) for item in data]
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.executemany(query, params)
                conn.commit()
                return True
        except sqlite3.Error as e:
            print(f"Error during sync batch insert: {e}")
            return False

    async def _async_batch_insert(self, table: str, data: List[Dict[str, Any]]) -> bool:
        """
        异步批量插入记录
        :param table: 表名
        :param data: 插入的数据列表（字典形式）
        :return: 是否插入成功
        """
        if not data:
            return False
        columns = ', '.join(data[0].keys())
        placeholders = ', '.join(['?'] * len(data[0]))
        query = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"
        params = [tuple(item.values()) for item in data]
        try:
            async with aiosqlite.connect(self.db_path) as conn:
                await conn.executemany(query, params)
                await conn.commit()
                return True
        except aiosqlite.Error as e:
            print(f"Error during async batch insert: {e}")
            return False
