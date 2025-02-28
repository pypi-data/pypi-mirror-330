from distutils.core import setup

setup(
    name         ='pyhyperworks',
    version      ='1.0.0',
    py_modules   =['pyhyperworks'],
    author       ='xinxing.zhang',
    author_email ='zxx4477@126.com',
    description  ='Tools for Altiar Hyperworks App',
    )

from setuptools import setup, find_packages

setup(
    name="pyhyperworks",      # 包名（需在PyPI唯一）
    version="1.0.0",          # 版本号
    packages=find_packages(), # 自动发现所有包
    install_requires=[],      # 依赖库列表
    author="xinxing.zhang",
    author_email ='zxx4477@126.com',
    description="This package is a tools-package for Altair HyperWorks",
    url="https://github.com/zxx4477/pyhyperworks",
    license="MIT",
)
