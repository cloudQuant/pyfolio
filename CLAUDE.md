# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Pyfolio is a Python library for portfolio performance analysis and risk analytics. This is a modified fork of Quantopian's original pyfolio, enhanced by CloudQuant (云金杞) with additional features including a Flask web interface and Chinese documentation support.

## Key Commands

### Installation
```bash
# Windows
install_win.bat

# Unix/Linux/macOS
./install_unix.sh
```

### Testing
```bash
# Run all tests with 4 parallel processes
pytest tests/ -n 4

# Run specific test file
pytest tests/test_timeseries.py

# Run with coverage
pytest tests/ --cov=pyfolio
```

### Building
```bash
# Build the package
python setup.py build

# Create distribution
python setup.py sdist bdist_wheel
```

### Development Installation
```bash
# Install in development mode
pip install -e .
```

## Architecture Overview

The codebase follows a modular structure with specialized components:

1. **Core Analysis Modules**:
   - `timeseries.py`: Statistical time series analysis (VaR, Sharpe ratio, etc.)
   - `plotting.py`: All visualization functions using matplotlib/seaborn
   - `tears.py`: Main interface that orchestrates creating comprehensive reports ("tear sheets")
   - `pos.py`: Position-level analysis and metrics
   - `txn.py`: Transaction-level analysis
   - `risk.py`: Risk metrics and factor analysis
   - `round_trips.py`: Round trip trade analysis
   - `perf_attrib.py`: Performance attribution analysis

2. **Web Interface**:
   - `flask_app.py`: Flask application for web-based result display
   - Templates in `templates/`: HTML templates for web UI
   - Designed to work in IDEs (Spyder, PyCharm, VSCode) and browsers

3. **Data Flow**:
   - Input: Returns series (pandas Series), positions (DataFrame), transactions (DataFrame)
   - Processing: Uses empyrical for performance calculations
   - Output: Matplotlib figures or Flask web pages

## Important Technical Notes

1. **Dependencies**: Requires empyrical 0.5.6 from https://gitee.com/yunjinqi/empyrical (not PyPI version)

2. **Matplotlib Backend**: The code sets matplotlib backend to 'Agg' in tears.py - be aware when modifying plotting code

3. **Chinese Data Support**: Sample data files use Chinese column names. The library handles both English and Chinese data formats.

4. **Testing Data**: Test data is provided in `tests/test_data/` directory with pickle files for various test scenarios

5. **Flask Integration**: The `tears.create_returns_tear_sheet()` and similar functions can output to Flask when `output_format='flask'`

## Code Conventions

- Use numpy-style docstrings for all public functions
- Follow existing import patterns (imports at top, grouped by standard/third-party/local)
- Maintain compatibility with pandas DataFrames and Series
- Use empyrical for standard performance calculations rather than reimplementing
- Preserve bilingual support (Chinese documentation, English code/comments)

## Common Development Tasks

When modifying analysis functions:
1. Check if empyrical already provides the calculation
2. Add corresponding plotting function if creating new metrics
3. Update relevant tear sheet functions to include new analysis
4. Add tests with sample data

When working with the Flask interface:
1. Templates are in `templates/` directory
2. Static files go in `static/` directory
3. Use the existing `show_in_flask()` pattern for new visualizations