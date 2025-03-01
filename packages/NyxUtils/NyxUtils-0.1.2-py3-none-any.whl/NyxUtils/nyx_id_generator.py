import time
import uuid
import secrets
import os
import random
from typing import Dict, Union, Literal


class NyxIDGenerator:

    @staticmethod
    def snowflake_id(machine_id: int = 1) -> int:
        """
        使用雪花算法生成唯一 ID。
        :param machine_id: 机器 ID，默认为 1。
        :return: 64 位的唯一 ID。ID: 1234567890123456789
        """
        snowflake = Snowflake(machine_id)  # 创建 Snowflake 实例
        return snowflake.generate_id()

    @staticmethod
    def uuid4() -> str:
        """
        生成 UUID v4。
        :return: 36 位的 UUID 字符串。550e8400-e29b-41d4-a716-446655440000
        """
        return str(uuid.uuid4())

    @staticmethod
    def random_string(length: int = 32) -> str:
        """
        生成随机字符串。
        :param length: 字符串长度，默认为 32。
        :return: 随机字符串。abc123...
        """
        return secrets.token_urlsafe(length)

    @staticmethod
    def custom_random_string(
        length: int = 32, charset: str = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    ) -> str:
        """
        生成自定义字符集的随机字符串。
        :param length: 字符串长度，默认为 32。
        :param charset: 字符集，默认为字母和数字。
        :return: 随机字符串。
        """
        return ''.join(secrets.choice(charset) for _ in range(length))

    @staticmethod
    def timestamp_id() -> str:
        """
        生成基于时间戳的唯一 ID。
        :return: 时间戳 + 随机数的字符串。16970496000001234
        """
        timestamp = int(time.time() * 1000)  # 毫秒级时间戳
        random_num = secrets.randbelow(10000)  # 4 位随机数
        return f"{timestamp}{random_num:04d}"

    @staticmethod
    def short_id(length: int = 8) -> str:
        """
        生成短 ID（基于随机字符串）。
        :param length: 短 ID 的长度，默认为 8。
        :return: 短 ID 字符串。abc12345
        """
        return secrets.token_urlsafe(length)[:length]

    @staticmethod
    def numeric_id(length: int = 10) -> str:
        """
        生成纯数字的唯一 ID。
        :param length: 数字 ID 的长度，默认为 10。
        :return: 纯数字的唯一 ID。1234567890
        """
        return ''.join(secrets.choice("0123456789") for _ in range(length))

    @staticmethod
    def object_id() -> str:
        """
        生成 MongoDB 风格的 ObjectID。
        :return: 24 位的十六进制字符串。615f7b8b3e1a2b3c4d5e6f7g
        """
        timestamp = int(time.time())  # 4 字节时间戳
        machine_id = random.randint(0, 0xFFFFFF)  # 3 字节机器 ID
        process_id = os.getpid() & 0xFFFF  # 2 字节进程 ID
        counter = random.randint(0, 0xFFFFFF)  # 3 字节随机数

        object_id = (f"{timestamp:08x}"
                     f"{machine_id:06x}"
                     f"{process_id:04x}"
                     f"{counter:06x}")
        return object_id

    @staticmethod
    def parse_snowflake_id(snowflake_id: int) -> Dict[str, int]:
        """
        解析雪花 ID。
        :param snowflake_id: 雪花 ID。
        :return: 包含时间戳、机器 ID 和序列号的字典。
        """
        timestamp = (snowflake_id >> 22) + 1288834974657  # 转换为 Unix 时间戳
        machine_id = (snowflake_id >> 12) & 0x3FF  # 10 位机器 ID
        sequence = snowflake_id & 0xFFF  # 12 位序列号
        return {
            "timestamp": timestamp,
            "machine_id": machine_id,
            "sequence": sequence,
        }

    @staticmethod
    def format_id(id_value: Union[int, str], prefix: str = "ID", separator: str = "-") -> str:
        """
        格式化 ID。
        :param id_value: ID 值。
        :param prefix: ID 前缀，默认为 "ID"。
        :param separator: 分隔符，默认为 "-"。
        :return: 格式化后的 ID 字符串。
        """
        return f"{prefix}{separator}{id_value}"


class Snowflake:

    def __init__(self, machine_id: int = 1):
        """
        初始化雪花算法生成器。
        :param machine_id: 机器 ID，默认为 1。
        """
        self.machine_id = machine_id
        self.sequence = 0
        self.last_timestamp = -1

    def generate_id(self) -> int:
        """
        生成雪花 ID。
        :return: 64 位的唯一 ID。
        """
        timestamp = self._current_timestamp()

        if timestamp == self.last_timestamp:
            self.sequence = (self.sequence + 1) & 4095  # 12 位序列号
            if self.sequence == 0:
                timestamp = self._wait_for_next_millisecond(self.last_timestamp)
        else:
            self.sequence = 0

        self.last_timestamp = timestamp

        # 雪花算法结构：时间戳（41 位） + machine_id（10 位） + 序列号（12 位）
        return ((timestamp << 22) | (self.machine_id << 12) | self.sequence)

    def _current_timestamp(self) -> int:
        """
        获取当前时间戳（毫秒级）。
        :return: 当前时间戳。
        """
        return int(time.time() * 1000)

    def _wait_for_next_millisecond(self, last_timestamp: int) -> int:
        """
        等待到下一毫秒。
        :param last_timestamp: 上次生成 ID 的时间戳。
        :return: 下一毫秒的时间戳。
        """
        timestamp = self._current_timestamp()
        while timestamp <= last_timestamp:
            timestamp = self._current_timestamp()
        return timestamp


__all__ = ["NyxIDGenerator"]
