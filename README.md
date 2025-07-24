# PyFolio - Portfolio Analytics

<div align="center">

![Python](https://img.shields.io/badge/python-3.8%20%7C%203.9%20%7C%203.10%20%7C%203.11%20%7C%203.12%20%7C%203.13-blue)
![License](https://img.shields.io/badge/license-Apache%202.0-green)
![Tests](https://github.com/cloudQuant/pyfolio/workflows/CI/badge.svg)

**A comprehensive Python library for portfolio performance and risk analysis**

[English](#english) | [中文](#中文)

</div>

---

## English

PyFolio is a powerful Python library designed for comprehensive portfolio performance analysis and risk analytics. This enhanced fork includes additional features like a modern Flask web interface and extensive Chinese data support.

### ✨ Key Features

- **📊 Comprehensive Analytics**: Returns, risk metrics, drawdowns, and performance attribution
- **📈 Rich Visualizations**: Professional charts with matplotlib and seaborn
- **🌐 Web Interface**: Modern Flask-based dashboard for interactive analysis
- **📝 Tear Sheets**: Automated comprehensive reports
- **🔄 Multi-Format Support**: Both English and Chinese data formats
- **⚡ High Performance**: Optimized calculations using empyrical
- **🧪 Well Tested**: Extensive test suite across multiple Python versions

### 🚀 Quick Start

#### Installation

**Windows:**
```bash
install_win.bat
```

**Unix/Linux/macOS:**
```bash
./install_unix.sh
```

**Manual Installation:**
```bash
pip install -e .
```

#### Basic Usage

```python
import pandas as pd
import pyfolio as pf

# Load your returns data
returns = pd.Series([0.01, 0.02, -0.01, 0.03], 
                   index=pd.date_range('2023-01-01', periods=4))

# Create a comprehensive tear sheet
pf.create_returns_tear_sheet(returns)

# Or use the modern web interface
pf.create_full_tear_sheet_by_flask(returns, run_flask_app=True)
```

#### Web Dashboard Demo

```python
# Run the Flask demo
python examples/demo_flask.py
```

This creates a professional financial dashboard with:
- Key performance metrics cards
- Interactive charts and visualizations
- Collapsible detailed statistics sections
- Responsive design optimized for financial data

### 📋 Available Tear Sheets

| Function | Description |
|----------|-------------|
| `create_returns_tear_sheet()` | Basic returns analysis |
| `create_full_tear_sheet()` | Comprehensive analysis with positions |
| `create_position_tear_sheet()` | Position-level analysis |
| `create_txn_tear_sheet()` | Transaction analysis |
| `create_round_trip_tear_sheet()` | Round trip trade analysis |
| `create_risk_tear_sheet()` | Risk factor analysis |
| `create_perf_attrib_tear_sheet()` | Performance attribution |

### 🔧 Development

#### Testing
```bash
# Run all tests with parallel execution
pytest tests/ -n 4

# Run specific test file
pytest tests/test_timeseries.py

# Run with coverage
pytest tests/ --cov=pyfolio
```

#### Building
```bash
# Build package
python setup.py build

# Create distribution
python setup.py sdist bdist_wheel
```

### 📁 Project Structure

```
pyfolio/
├── pyfolio/           # Main package
│   ├── tears.py       # Main tear sheet interface
│   ├── timeseries.py  # Time series analysis
│   ├── plotting.py    # Visualization functions
│   ├── risk.py        # Risk metrics
│   ├── pos.py         # Position analysis
│   ├── txn.py         # Transaction analysis
│   └── flask_app.py   # Web interface
├── examples/          # Usage examples
├── tests/             # Test suite
└── templates/         # Flask templates
```

### 🌟 Core Metrics

PyFolio calculates a comprehensive set of performance and risk metrics:

**Performance Metrics:**
- Total Returns, Annual Returns, Cumulative Returns
- Sharpe Ratio, Sortino Ratio, Calmar Ratio
- Alpha, Beta, Max Drawdown, Volatility

**Risk Analytics:**
- Value at Risk (VaR), Conditional VaR
- Rolling metrics and time-series analysis
- Factor exposure and performance attribution

### 🔗 Dependencies

- **empyrical**: Performance calculations (from [GitHub](https://github.com/cloudQuant/empyrical))
- **pandas**: Data manipulation and analysis
- **numpy**: Numerical computing
- **scipy**: Scientific computing
- **matplotlib**: Plotting and visualization
- **flask**: Web interface framework

### 📄 License

This project is licensed under the Apache 2.0 License - see the LICENSE file for details.

### 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

---

## 中文

PyFolio 是一个功能强大的 Python 投资组合分析库，专为全面的投资组合绩效分析和风险分析而设计。这个增强版本包含现代化的 Flask Web 界面和广泛的中文数据支持。

### ✨ 主要特性

- **📊 全面分析**: 收益率、风险指标、回撤和绩效归因
- **📈 丰富可视化**: 使用 matplotlib 和 seaborn 的专业图表
- **🌐 Web 界面**: 基于 Flask 的现代化交互式分析仪表板
- **📝 分析报告**: 自动化综合报告生成
- **🔄 多格式支持**: 支持英文和中文数据格式
- **⚡ 高性能**: 使用 empyrical 优化计算
- **🧪 完善测试**: 跨多个 Python 版本的广泛测试套件

### 🚀 快速开始

#### 安装

**Windows:**
```bash
install_win.bat
```

**Unix/Linux/macOS:**
```bash
./install_unix.sh
```

**手动安装:**
```bash
pip install -e .
```

#### 基础用法

```python
import pandas as pd
import pyfolio as pf

# 加载收益率数据
returns = pd.Series([0.01, 0.02, -0.01, 0.03], 
                   index=pd.date_range('2023-01-01', periods=4))

# 创建综合分析报告
pf.create_returns_tear_sheet(returns)

# 或使用现代化 Web 界面
pf.create_full_tear_sheet_by_flask(returns, run_flask_app=True)
```

#### Web 仪表板演示

```python
# 运行 Flask 演示
python examples/demo_flask.py
```

这将创建一个专业的金融仪表板，包含：
- 关键绩效指标卡片
- 交互式图表和可视化
- 可折叠的详细统计部分
- 针对金融数据优化的响应式设计

### 📋 可用分析报告

| 函数 | 描述 |
|------|------|
| `create_returns_tear_sheet()` | 基础收益率分析 |
| `create_full_tear_sheet()` | 包含持仓的综合分析 |
| `create_position_tear_sheet()` | 持仓级别分析 |
| `create_txn_tear_sheet()` | 交易分析 |
| `create_round_trip_tear_sheet()` | 往返交易分析 |
| `create_risk_tear_sheet()` | 风险因子分析 |
| `create_perf_attrib_tear_sheet()` | 绩效归因分析 |

### 🔧 开发

#### 测试
```bash
# 并行运行所有测试
pytest tests/ -n 4

# 运行特定测试文件
pytest tests/test_timeseries.py

# 运行覆盖率测试
pytest tests/ --cov=pyfolio
```

#### 构建
```bash
# 构建包
python setup.py build

# 创建分发包
python setup.py sdist bdist_wheel
```

### 📁 项目结构

```
pyfolio/
├── pyfolio/           # 主包
│   ├── tears.py       # 主要分析报告接口
│   ├── timeseries.py  # 时间序列分析
│   ├── plotting.py    # 可视化函数
│   ├── risk.py        # 风险指标
│   ├── pos.py         # 持仓分析
│   ├── txn.py         # 交易分析
│   └── flask_app.py   # Web 界面
├── examples/          # 使用示例
├── tests/             # 测试套件
└── templates/         # Flask 模板
```

### 🌟 核心指标

PyFolio 计算全面的绩效和风险指标集：

**绩效指标:**
- 总收益率、年化收益率、累计收益率
- 夏普比率、索提诺比率、卡玛比率
- Alpha、Beta、最大回撤、波动率

**风险分析:**
- 风险价值 (VaR)、条件风险价值
- 滚动指标和时间序列分析
- 因子暴露和绩效归因

### 🔗 依赖库

- **empyrical**: 绩效计算 (来自 [GitHub](https://github.com/cloudQuant/empyrical))
- **pandas**: 数据处理和分析
- **numpy**: 数值计算
- **scipy**: 科学计算
- **matplotlib**: 绘图和可视化
- **flask**: Web 界面框架

### 📄 许可证

本项目采用 Apache 2.0 许可证 - 详情请参阅 LICENSE 文件。

### 🤝 贡献

欢迎贡献！请随时提交 Pull Request。

---

<div align="center">

**Made with ❤️ by CloudQuant (云金杞)**

[GitHub](https://github.com/cloudQuant/pyfolio) | [Gitee](https://gitee.com/yunjinqi/pyfolio)

</div>