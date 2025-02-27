from setuptools import setup, find_packages

setup(
    name = "NyxUtils",  # 包的名称
    version = "0.1.1",  # 版本号
    author = "AlitaZzz",
    packages = find_packages(),  # 自动发现包含 `__init__.py` 的子模块
    install_requires = ["aiosqlite", "requests"],
    python_requires = '>=3.6'
)
