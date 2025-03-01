from setuptools import setup, find_packages

setup(
    name = "NyxUtils",
    version = "0.1.2",
    author = "AlitaZzz",
    description = "A utility package providing various helpful functions.",
    packages = find_packages(),
    install_requires = ["aiosqlite", "requests"],
    python_requires = '>=3.6',
    url = "https://github.com/yourusername/NyxUtils",  # 项目地址
    classifiers = [
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
