@echo off
:: 切换到脚本所在目录的上一级目录，确保相对路径正确
cd /d "%~dp0.."
:: 检查 empyrical 0.5.6 版本是否已经安装
pip show empyrical | findstr "Version: 0.5.6"
IF %ERRORLEVEL% NEQ 0 (
    echo empyrical 0.5.6 not found. Cloning empyrical from Gitee...

    :: 检查 empyrical 目录是否已存在
    IF NOT EXIST empyrical (
        :: 克隆 empyrical 仓库
        git clone https://gitee.com/yunjinqi/empyrical
        IF %ERRORLEVEL% NEQ 0 (
            echo Failed to clone empyrical repository. Exiting...
            exit /b 1
        )
    )
    :: 运行 install_win.bat 安装 empyrical
    echo Running install_win.bat for empyrical...
    call .\empyrical\install_win.bat
    IF %ERRORLEVEL% NEQ 0 (
        echo Failed to run install_win.bat for empyrical. Exiting...
    )
) ELSE (
    echo empyrical 0.5.6 is already installed.
)

:: 安装 requirements.txt 中的依赖
pip install -U -r ./pyfolio/requirements.txt

SET BUILD_DIR=build
SET EGG_INFO_DIR=pyfolio.egg-info
SET BENCHMARKS_DIR=.benchmarks

:: 安装 pyfolio 包
echo Installing pyfolio...
pip install -U ./pyfolio
IF %ERRORLEVEL% NEQ 0 (
    echo Failed to install pyfolio. Exiting...
    exit /b 1
)

:: 运行测试用例，使用 4 个进程并行测试
echo Running tests for pyfolio...
pytest ./pyfolio/tests -n 4
IF %ERRORLEVEL% NEQ 0 (
    echo Test cases for pyfolio failed. Exiting...
    exit /b 1
)

cd ./pyfolio

:: 删除中间构建和 egg-info 目录
echo Deleting intermediate files...
IF EXIST %BUILD_DIR% (
    rmdir /s /q %BUILD_DIR%
    echo Deleted %BUILD_DIR% directory.
)
IF EXIST %EGG_INFO_DIR% (
    rmdir /s /q %EGG_INFO_DIR%
    echo Deleted %EGG_INFO_DIR% directory.
)

:: 删除 pytest 生成的 .benchmarks 目录
IF EXIST %BENCHMARKS_DIR% (
    rmdir /s /q %BENCHMARKS_DIR%
    echo Deleted %BENCHMARKS_DIR% directory.
)

:: 删除所有 .log 文件
echo Deleting all .log files...
del /s /q *.log
echo All .log files deleted.


