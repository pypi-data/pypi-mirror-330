# pyhyperworks

#### 介绍

pyhyperworks功能包是基于Altair HyperWorks软件进行二次开发的功能集合，旨在帮助CAE工程师提升工作效率和工作规范性
This package is a tools-package for HyperWorks(a CAE preprocess software)
These enhancements make access much easier, and also debugging!

#### 功能包架构

本功能包需要在HyperWorks 2024.1及以后版本环境下使用，作为Altair Hyperworsk软件的一个外部模块。
功能包的整体结构如下：

./pyhyperworks

    ./_clientConfig      客户端配置文件夹

    ./_pkgconfig         功能包配置文件夹

    ./_cccPartLib        标准件模型库

    ./_images            图片文件夹

    ./_materialLib       材料参数文件夹

    ./_meshStandrad      网格标准文件夹

    ./_utils             功能库文件夹

    ./modeling           建模功能

    ./loadcase           工况功能

    ./Body           车身

    ./..

#### 安装教程

1. pip install pyhyperworks
2. pip list

#### 使用说明

1. import pyhyperworks as pyhw
2. dir(pyhw)

#### 应用示例

    matlib=pthw.MaterialLibrary();
    matlib.helpinfo()

#### 联系方式

Authors: Xinxing.Zhang
[Contact Author](WeChat:zxx4477 Email:zxx4477@126.com)
