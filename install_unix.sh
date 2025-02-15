#!/bin/bash

# 定义变量
BUILD_DIR="build"
EGG_INFO_DIR="pyfolio.egg-info"
BENCHMARKS_DIR=".benchmarks"
EMPYRICAL_VERSION="0.5.6"

# 获取默认工作目录（用户主目录）
DEFAULT_WORK_DIR="$HOME"
echo "Default working directory: $DEFAULT_WORK_DIR"

# 切换到默认工作目录
echo "Switching to the default working directory..."
cd "$DEFAULT_WORK_DIR" || { echo "Failed to switch to default working directory. Exiting..."; exit 1; }


# Function to check if a Python package is installed
check_package_installed() {
    python3 -c "import pkgutil; exit(0 if pkgutil.find_loader('$1') is not None else 1)"
}

# 检查 empyrical 0.5.6 版本是否已经安装
echo "Checking if empyrical $EMPYRICAL_VERSION is installed..."
if ! check_package_installed "empyrical"; then
    echo "empyrical $EMPYRICAL_VERSION not found. Cloning empyrical from Gitee..."
    # 检查当前目录下是否存在 pyfolio 文件夹
    if [ ! -d "empyrical" ]; then
        echo "empyrical directory does not exist. Cloning empyrical from Gitee..."
        git clone https://gitee.com/yunjinqi/empyrical
        if [ $? -ne 0 ]; then
            echo "Failed to clone empyrical repository. Exiting..."
            exit 1
        fi
    else
        echo "empyrical directory already exists. Skipping git clone."
    fi
    # 运行 install_unix.sh 安装 empyrical
    echo "Running install_unix.sh for empyrical..."
    cd ./empyrical
    sh install_unix.sh
    if [ $? -ne 0 ]; then
        echo "Failed to run install_unix.sh for empyrical. Exiting..."
        exit 1
    fi
    cd ..
else
    echo "empyrical $EMPYRICAL_VERSION is already installed."
fi

# 安装 requirements.txt 中的依赖
echo "Installing dependencies from requirements.txt..."
pip install -U -r ./pyfolio/requirements.txt
if [ $? -ne 0 ]; then
    echo "Failed to install dependencies from requirements.txt. Exiting..."
    exit 1
fi

# 安装 pyfolio 包
echo "Installing pyfolio..."
pip install -U --no-build-isolation ./pyfolio
if [ $? -ne 0 ]; then
    echo "Failed to install pyfolio. Exiting..."
    exit 1
fi

# 运行 backtrader 的测试用例，使用 4 个进程并行测试
echo "Running tests for pyfolio..."
pytest ./pyfolio/tests -n 4
if [ $? -ne 0 ]; then
    echo "Test cases for pyfolio failed. Exiting..."
    exit 1
fi

# 切换到 pyfolio 目录
cd ./pyfolio
# 删除中间构建和 egg-info 目录
echo "Deleting intermediate files..."
if [ -d "$BUILD_DIR" ]; then
    rm -rf "$BUILD_DIR"
    echo "Deleted $BUILD_DIR directory."
fi

if [ -d "$EGG_INFO_DIR" ]; then
    rm -rf "$EGG_INFO_DIR"
    echo "Deleted $EGG_INFO_DIR directory."
fi

# 删除 .benchmarks 目录
if [ -d "$BENCHMARKS_DIR" ]; then
    rm -rf "$BENCHMARKS_DIR"
    echo "Deleted $BENCHMARKS_DIR directory."
fi

# 删除所有 .log 文件
echo "Deleting all .log files..."
find . -type f -name "*.log" -exec rm -f {} \;
echo "All .log files deleted."

# 脚本执行完成
echo "Script execution completed!"




