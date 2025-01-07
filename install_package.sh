#!/bin/bash

# 切换到上级目录
cd ..

# 安装或升级 pyfolio 包
pip install -U ./pyfolio

# 切换回 pyfolio 目录
cd pyfolio

# 如果存在pyfolio.egg-info文件夹，删除之
if [ -d "pyfolio.egg-info" ]; then
    rm -rf pyfolio.egg-info
fi
# 如果存在build文件夹，删除之
if [ -d "build" ]; then
    rm -rf build
fi

