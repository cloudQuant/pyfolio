#
# Copyright 2018 Quantopian, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import division

import warnings

from itertools import cycle
from matplotlib.pyplot import cm
import numpy as np
import pandas as pd
try:
    from IPython.display import display, HTML
    HAS_IPYTHON = True
except ImportError:
    HAS_IPYTHON = False
    # Define dummy functions for non-IPython environments
    def display(obj):
        print(obj)
    def HTML(string):
        return string
from pathlib import Path
import os
import pyfolio as pf
import empyrical.utils
from pandas.testing import assert_frame_equal, assert_series_equal
from packaging import version

from . import pos
from . import txn
import matplotlib
matplotlib.use('Agg')

APPROX_BDAYS_PER_MONTH = 21
APPROX_BDAYS_PER_YEAR = 252

MONTHS_PER_YEAR = 12
WEEKS_PER_YEAR = 52

MM_DISPLAY_UNIT = 1000000.

DAILY = 'daily'
WEEKLY = 'weekly'
MONTHLY = 'monthly'
YEARLY = 'yearly'

ANNUALIZATION_FACTORS = {
    DAILY: APPROX_BDAYS_PER_YEAR,
    WEEKLY: WEEKS_PER_YEAR,
    MONTHLY: MONTHS_PER_YEAR
}

COLORMAP = 'Paired'
COLORS = ['#e6194b', '#3cb44b', '#ffe119', '#0082c8', '#f58231',
          '#911eb4', '#46f0f0', '#f032e6', '#d2f53c', '#fabebe',
          '#008080', '#e6beff', '#aa6e28', '#800000', '#aaffc3',
          '#808000', '#ffd8b1', '#000080', '#808080']


def analyze_dataframe_differences(daily_txn, expected):
    """
    Analyze the differences between two DataFrames, `daily_txn` and `expected`.

    Parameters
    ----------
    daily_txn : pd.DataFrame
        The first DataFrame to compare.
    expected : pd.DataFrame
        The second DataFrame to compare.

    Returns
    -------
    None
        Prints the differences between the two DataFrames.
    """
    print("Analyzing differences between daily_txn and expected...")

    # Check if the DataFrames are equal
    try:
        assert_frame_equal(daily_txn, expected)
        print("The DataFrames are identical.")
    except AssertionError as e:
        print("The DataFrames are not identical. Details below:")
        print(e)

    # Compare index
    print("\nComparing Index:")
    if not daily_txn.index.equals(expected.index):
        print("Indices are different:")
        print("daily_txn index:", daily_txn.index)
        print("expected index:", expected.index)
        print("daily_txn index freq:", daily_txn.index.freq)
        print("expected index freq:", expected.index.freq)
    else:
        print("Indices are identical.")

    # Compare columns
    print("\nComparing Columns:")
    if not daily_txn.columns.equals(expected.columns):
        print("Columns are different:")
        print("daily_txn columns:", daily_txn.columns)
        print("expected columns:", expected.columns)
    else:
        print("Columns are identical.")

    # Compare dtypes
    print("\nComparing Dtypes:")
    if not daily_txn.dtypes.equals(expected.dtypes):
        print("Dtypes are different:")
        print("daily_txn dtypes:", daily_txn.dtypes)
        print("expected dtypes:", expected.dtypes)
    else:
        print("Dtypes are identical.")

    # Compare values
    print("\nComparing Values:")
    if not daily_txn.equals(expected):
        print("Values are different:")
        print("Differences in daily_txn vs expected:")
        print(pd.concat([daily_txn, expected], axis=1, keys=['daily_txn', 'expected']).swaplevel(axis=1).sort_index(
            axis=1))
    else:
        print("Values are identical.")

    # Compare metadata (e.g., index frequency)
    print("\nComparing Metadata:")
    if daily_txn.index.freq != expected.index.freq:
        print("Index frequencies are different:")
        print("daily_txn index freq:", daily_txn.index.freq)
        print("expected index freq:", expected.index.freq)
    else:
        print("Index frequencies are identical.")


def analyze_series_differences(series1, series2):
    """
    Analyze the differences between two Series, `series1` and `series2`.

    Parameters
    ----------
    series1 : pd.Series
        The first Series to compare.
    series2 : pd.Series
        The second Series to compare.

    Returns
    -------
    None
        Prints the differences between the two Series.
    """
    print("Analyzing differences between series1 and series2...")

    # Check if the Series are equal
    try:
        assert_series_equal(series1, series2)
        print("The Series are identical.")
    except AssertionError as e:
        print("The Series are not identical. Details below:")
        print(e)

    # Compare index
    print("\nComparing Index:")
    if not series1.index.equals(series2.index):
        print("Indices are different:")
        print("series1 index:", series1.index)
        print("series2 index:", series2.index)
        print("series1 index freq:", series1.index.freq)
        print("series2 index freq:", series2.index.freq)
    else:
        print("Indices are identical.")

    # Compare dtypes
    print("\nComparing Dtypes:")
    if series1.dtype != series2.dtype:
        print("Dtypes are different:")
        print("series1 dtype:", series1.dtype)
        print("series2 dtype:", series2.dtype)
    else:
        print("Dtypes are identical.")

    # Compare values
    print("\nComparing Values:")
    if not series1.equals(series2):
        print("Values are different:")
        print("Differences in series1 vs series2:")
        differences = pd.concat([series1, series2], axis=1, keys=['series1', 'series2']).swaplevel(axis=1).sort_index(
            axis=1)
        print(differences[differences['series1'] != differences['series2']])
    else:
        print("Values are identical.")

    # Compare metadata (e.g., index frequency)
    print("\nComparing Metadata:")
    if series1.index.freq != series2.index.freq:
        print("Index frequencies are different:")
        print("series1 index freq:", series1.index.freq)
        print("series2 index freq:", series2.index.freq)
    else:
        print("Index frequencies are identical.")


def one_dec_places(x, pos):
    """
    Adds 1/10th decimal to plot ticks.
    """

    return '%.1f' % x


def two_dec_places(x, pos):
    """
    Adds 1/100th decimal to plot ticks.
    """

    return '%.2f' % x


def percentage(x, pos):
    """
    Adds percentage sign to plot ticks.
    """

    return '%.0f%%' % x


def format_asset(asset):
    """
    If zipline asset objects are used, we want to print them out prettily
    within the tear sheet. This function should only be applied directly
    before displaying.
    """

    try:
        import zipline.assets
    except ImportError:
        return asset

    if isinstance(asset, zipline.assets.Asset):
        return asset.symbol
    else:
        return asset


def vectorize(func):
    """
    Decorator so that functions can be written to work on Series but
    may still be called with DataFrames.
    """

    def wrapper(df, *args, **kwargs):
        if df.ndim == 1:
            return func(df, *args, **kwargs)
        elif df.ndim == 2:
            return df.apply(func, *args, **kwargs)

    return wrapper


def extract_rets_pos_txn_from_zipline(backtest):
    """
    Extract returns, positions, transactions and leverage from the
    backtest data structure returned by zipline.TradingAlgorithm.run().

    The returned data structures are in a format compatible with the
    rest of pyfolio and can be directly passed to
    e.g., tears.create_full_tear_sheet().

    Parameters
    ----------
    backtest : pd.DataFrame :
        DataFrame returned by zipline.TradingAlgorithm.run()

    Returns
    -------
    returns : pd.Series
        Daily returns of strategy.
         - See full explanation in tears.create_full_tear_sheet.
    positions : pd.DataFrame
        Daily net position values.
         - See full explanation in tears.create_full_tear_sheet.
    transactions : pd.DataFrame
        Prices and `amounts` of executed trades.One row per trade.
         - See full explanation in tears.create_full_tear_sheet.


    Example (on the Quantopian research platform)
    ---------------------------------------------
    # >>> backtest = my_algo.run()
    # >>> returns, positions, transactions =
    # >>> pyfolio.utils.extract_rets_pos_txn_from_zipline(backtest)
    # >>> pyfolio.tears.create_full_tear_sheet(returns,
    # >>> positions, transactions)
    """

    backtest.index = backtest.index.normalize()
    if backtest.index.tzinfo is None:
        backtest.index = backtest.index.tz_localize('UTC')
    returns = backtest.returns
    raw_positions = []
    for dt, pos_row in backtest.positions.items():
        df = pd.DataFrame(pos_row)
        df.index = [dt] * len(df)
        raw_positions.append(df)
    if not raw_positions:
        raise ValueError("The backtest does not have any positions.")
    positions = pd.concat(raw_positions)
    positions = pos.extract_pos(positions, backtest.ending_cash)
    transactions = txn.make_transaction_frame(backtest.transactions)
    if transactions.index.tzinfo is None:
        transactions.index = transactions.index.tz_localize('utc')

    return returns, positions, transactions


def print_table(table,
                name=None,
                float_format=None,
                formatters=None,
                header_rows=None,
                run_flask_app=False):
    """
    Pretty print a pandas DataFrame.

    Uses HTML output if running inside Jupyter Notebook, otherwise
    formatted text output.

    Parameters
    ----------
    table : pandas.Series or pandas.DataFrame
        Table to pretty-print.
    name : str, optional
        Table name to display in the upper-left corner.
    float_format : function, optional
        Formatter to use for displaying table elements, passed as the
        `float_format` arg to pd.Dataframe.to_html.
        E.g. `'{0:.2%}'.format` for displaying 100 as '100.00%'.
    formatters : list or dict, optional
        Formatters to use by column, passed as the `formatters` arg to
        pd.Dataframe.to_html.
    header_rows : dict, optional
        Extra rows to display at the top of the table.
    run_flask_app : bool, optional, default False
        Whether to run Flask app for displaying table in a web browser.
    """

    if isinstance(table, pd.Series):
        table = pd.DataFrame(table)

    if name is not None:
        table.columns.name = name

    html = table.to_html(float_format=float_format, formatters=formatters)

    if header_rows is not None:
        # Count the number of columns for the text to span
        n_cols = html.split('<thead>')[1].split('</thead>')[0].count('<th>')

        # Generate the HTML for the extra rows
        rows = ''
        for name, value in header_rows.items():
            rows += ('\n    <tr style="text-align: right;"><th>%s</th>' +
                     '<td colspan=%d>%s</td></tr>') % (name, n_cols, value)
        # Inject the new HTML
        html = html.replace('<thead>', '<thead>' + rows)
    if run_flask_app:
        # 检查pyfolio中是否存在static文件夹,如果存在,就保存数据到static中
        # 获取 pyfolio 的根目录
        data_root = Path(pf.__file__).parent
        # 目标静态文件路径
        target_static_path = data_root / "static"
        # 检查目标路径是否存在，如果不存在则创建
        target_static_path.mkdir(parents=True, exist_ok=True)
        # 生成 Excel 文件路径
        excel_file_path = target_static_path / f"strategy_performance_{name}.xlsx"
        # 将表格数据写入 Excel 文件
        try:
            # print(name, table)
            table.to_excel(excel_file_path, index=True)  # index=False 避免写入行索引
            # print(f"文件已成功保存到：{excel_file_path}")
        except Exception as e:
            print(f"保存文件时出错：{e}")
    display(HTML(html))


def standardize_data(x):
    """
    Standardize an array with mean and standard deviation.

    Parameters
    ----------
    x : np.array
        Array to standardize.

    Returns
    -------
    np.array
        Standardized array.
    """

    return (x - np.mean(x)) / np.std(x)


def detect_intraday(positions, transactions, threshold=0.25):
    """
    Attempt to detect an intraday strategy. Get the number of
    positions held at the end of the day, and divide that by the
    number of unique stocks transacted every day. If the average quotient
    is below a threshold, then an intraday strategy is detected.

    Parameters
    ----------
    positions : pd.DataFrame
        Daily net position values.
         - See full explanation in create_full_tear_sheet.
    transactions : pd.DataFrame
        Prices and `amounts` of executed trades. One row per trade.
         - See full explanation in create_full_tear_sheet.
    threshold : default 0.25
    Returns
    -------
    boolean
        True if an intraday strategy is detected.
    """

    daily_txn = transactions.copy()
    daily_txn.index = daily_txn.index.date
    txn_count = daily_txn.groupby(level=0).symbol.nunique().sum()
    daily_pos = positions.drop('cash', axis=1).replace(0, np.nan)
    return daily_pos.count(axis=1).sum() / txn_count < threshold


def check_intraday(estimate, returns, positions, transactions):
    """
    Logic for checking if a strategy is intraday and processing it.

    Parameters
    ----------
    estimate: boolean or str, optional
        Approximate returns for intraday strategies.
        See description in tears.create_full_tear_sheet.
    returns : pd.Series
        Daily returns of the strategy, noncumulative.
         - See full explanation in create_full_tear_sheet.
    positions : pd.DataFrame
        Daily net position values.
         - See full explanation in create_full_tear_sheet.
    transactions : pd.DataFrame
        Prices and `amounts` of executed trades.One row per trade.
         - See full explanation in create_full_tear_sheet.

    Returns
    -------
    pd.DataFrame
        Daily net position values, adjusted for intraday movement.
    """

    if estimate == 'infer':
        if positions is not None and transactions is not None:
            if detect_intraday(positions, transactions):
                warnings.warn('Detected intraday strategy; inferring positions from transactions. Set estimate_intraday' +
                              '=False to disable.')
                return estimate_intraday(returns, positions, transactions)
            else:
                return positions
        else:
            return positions

    elif estimate:
        if positions is not None and transactions is not None:
            return estimate_intraday(returns, positions, transactions)
        else:
            raise ValueError('Positions and txns needed to estimate intraday')
    else:
        return positions


def estimate_intraday(returns, positions, transactions, eod_hour=23):
    """
    Intraday strategies will often not hold positions at the day end.
    This attempts to find the point in the day that best represents
    the activity of the strategy on that day, and effectively resamples
    the end-of-day positions with the positions at this point of day.
    The point of day is found by detecting when our exposure in the
    market is at its maximum point. Note that this is an estimate.

    Parameters
    ----------
    returns : pd.Series
        Daily returns of the strategy, noncumulative.
         - See full explanation in create_full_tear_sheet.
    positions : pd.DataFrame
        Daily net position values.
         - See full explanation in create_full_tear_sheet.
    transactions : pd.DataFrame
        Prices and `amounts` of executed trades. One row per trade.
         - See full explanation in create_full_tear_sheet.
    eod_hour: default 23

    Returns
    -------
    pd.DataFrame
        Daily net position values, resampled for intraday behavior.
    """

    # Construct DataFrame of transaction amounts
    txn_val = transactions.copy()
    txn_val.index.names = ['date']
    txn_val['value'] = txn_val.amount * txn_val.price
    txn_val = txn_val.reset_index().pivot_table(
        index='date', values='value',
        columns='symbol').replace(np.nan, 0)

    # Cumulate transaction amounts each day
    # 此处应该有bug，进行修改
    # txn_val['date'] = txn_val.index.date
    # txn_val = txn_val.groupby('date').cumsum()
    txn_val['day'] = txn_val.index.date
    txn_val = txn_val.groupby('day').cumsum()

    # Calculate exposure, then take peak of exposure every day
    txn_val['exposure'] = txn_val.abs().sum(axis=1)
    # 出现bug，疑似使用旧版本的API
    # condition = (txn_val['exposure'] == txn_val.groupby(
    #     pd.TimeGrouper('24H'))['exposure'].transform(max))
    # condition = (txn_val['exposure'] == txn_val.groupby(
    #     pd.Grouper(freq='24h'))['exposure'].transform(max))
    condition = (txn_val['exposure'] == txn_val.groupby(
        pd.Grouper(freq='24h'))['exposure'].transform('max'))
    txn_val = txn_val[condition].drop('exposure', axis=1)

    # Compute cash delta
    txn_val['cash'] = -txn_val.sum(axis=1)

    # Shift EOD positions to positions at start of next trading day
    positions_shifted = positions.copy().shift(1).fillna(0)
    # starting_capital = positions.iloc[0].sum() / (1 + returns[0])
    starting_capital = positions.iloc[0].sum() / (1 + returns.iloc[0])
    # positions_shifted.cash[0] = starting_capital
    positions_shifted.iloc[0, positions_shifted.columns.get_loc('cash')] = starting_capital

    # Format and add start positions to intraday position changes
    txn_val.index = txn_val.index.normalize()
    corrected_positions = positions_shifted.add(txn_val, fill_value=0)
    corrected_positions.index.name = 'period_close'
    corrected_positions.columns.name = 'sid'

    return corrected_positions


def clip_returns_to_benchmark(rets, benchmark_rets):
    """
    Drop entries from rets so that the start and end dates of rets match those
    of benchmark_rets.

    Parameters
    ----------
    rets : pd.Series
        Daily returns of the strategy, noncumulative.
         - See pf.tears.create_full_tear_sheet for more details

    benchmark_rets : pd.Series
        Daily returns of the benchmark, noncumulative.

    Returns
    -------
    clipped_rets : pd.Series
        Daily noncumulative returns with index clipped to match that of
        benchmark returns.
    """

    if (rets.index[0] < benchmark_rets.index[0]) \
            or (rets.index[-1] > benchmark_rets.index[-1]):
        clipped_rets = rets[benchmark_rets.index]
    else:
        clipped_rets = rets

    return clipped_rets


def to_utc(df):
    """
    For use in tests, applied UTC timestamp to DataFrame.
    """

    try:
        df.index = df.index.tz_localize('UTC')
    except TypeError:
        df.index = df.index.tz_convert('UTC')

    return df


def to_series(df):
    """
    For use in tests; converts DataFrame's first column to Series.
    """

    return df[df.columns[0]]


def get_month_end_freq():
    """
    Get the appropriate month-end frequency string based on pandas version.
    
    Returns
    -------
    str
        'M' for pandas < 2.2.0, 'ME' for pandas >= 2.2.0
    """
    if version.parse(pd.__version__) < version.parse("2.2.0"):
        return 'M'
    else:
        return 'ME'


def make_timezone_aware(timestamp, target_tz):
    """
    Ensure a timestamp has the same timezone as target_tz.
    
    Parameters
    ----------
    timestamp : pd.Timestamp
        The timestamp to adjust
    target_tz : timezone or None
        The target timezone
        
    Returns
    -------
    pd.Timestamp
        Timestamp with matching timezone
    """
    if target_tz is not None:
        if timestamp.tz is None:
            return timestamp.tz_localize(target_tz)
        else:
            return timestamp.tz_convert(target_tz)
    elif timestamp.tz is not None:
        # Target is tz-naive but timestamp is tz-aware, remove tz
        return timestamp.tz_localize(None)
    return timestamp


# These functions are simply a passthrough to empyrical, but is
# required by the register_returns_func and get_symbol_rets.
default_returns_func = empyrical.utils.default_returns_func

# Settings dict to store functions/values that may
# need to be overridden depending on the user's environment
SETTINGS = {
    'returns_func': default_returns_func
}


def register_return_func(func):
    """
    Registers the 'returns_func' that will be called for
    retrieving returns data.

    Parameters
    ----------
    func : function
        A function that returns a pandas Series of asset returns.
        The signature of the function must be as follows

        >>> func(symbol)

        Where symbol is an asset identifier

    Returns
    -------
    None
    """

    SETTINGS['returns_func'] = func


def get_symbol_rets(symbol, start=None, end=None):
    """
    Calls the currently registered 'returns_func'

    Parameters
    ----------
    symbol : object
        An identifier for the asset whose return
        series is desired.
        e.g., ticker symbol or database ID
    start : date, optional
        Earliest date to fetch data for.
        Defaults to the earliest date available.
    end : date, optional
        Latest date to fetch data for.
        Defaults to the latest date available.

    Returns
    -------
    pandas.Series
        Returned by the current 'returns_func'
    """

    return SETTINGS['returns_func'](symbol,
                                    start=start,
                                    end=end)


def configure_legend(ax, autofmt_xdate=True, change_colors=False,
                     rotation=30, ha='right'):
    """
    Format legend for perf attribution plots:
    - put legend to the right of plot instead of overlapping with it
    - make legend order match up with graph lines
    - set colors, according to colormap
    """
    chart_box = ax.get_position()
    ax.set_position([chart_box.x0, chart_box.y0,
                     chart_box.width * 0.75, chart_box.height])

    # make legend order match graph lines
    handles, labels = ax.get_legend_handles_labels()
    handles_and_labels_sorted = sorted(zip(handles, labels),
                                       key=lambda x: x[0].get_ydata()[-1],
                                       reverse=True)

    handles_sorted = [h[0] for h in handles_and_labels_sorted]
    labels_sorted = [h[1] for h in handles_and_labels_sorted]

    if change_colors:
        for handle, color in zip(handles_sorted,
                                 cycle(COLORS)):
            handle.set_color(color)

    ax.legend(handles=handles_sorted,
              labels=labels_sorted,
              frameon=True,
              framealpha=0.5,
              loc='upper left',
              bbox_to_anchor=(1.05, 1),
              fontsize='large')

    # manually rotate xticklabels instead of using matplotlib's autofmt_xdate
    # because it disables xticklabels for all but the last plot
    if autofmt_xdate:
        for label in ax.get_xticklabels():
            label.set_ha(ha)
            label.set_rotation(rotation)


def sample_colormap(cmap_name, n_samples):
    """
    Sample a colormap from matplotlib
    """
    colors = []
    # Handle different matplotlib versions for colormap access
    try:
        # Try modern API first (matplotlib >= 3.8.0)
        import matplotlib.pyplot as plt
        colormap = plt.colormaps[cmap_name]
    except (AttributeError, KeyError):
        try:
            # Try intermediate API (matplotlib 3.5.0 - 3.7.x)
            colormap = cm.get_cmap(cmap_name)
        except (AttributeError, ValueError):
            try:
                # Try older API (matplotlib < 3.5.0)
                colormap = cm.cmap_d[cmap_name]
            except AttributeError:
                # Fallback to registry access
                colormap = cm._colormaps[cmap_name]
    
    for i in np.linspace(0, 1, n_samples):
        colors.append(colormap(i))

    return colors
