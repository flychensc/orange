# Orange

小橙子基金

## Mandarin

获取股票的简单信息，生成到一个excel里

```cmd
orange>python mandarin.py --help
Usage: mandarin.py [OPTIONS] COMMAND [ARGS]...

  get report of stocks

Options:
  --help  Show this message and exit.

Commands:
  basic   basic report of stocks
  detail  detail report of stock

orange>
```

### basic

基础信息，支持输入一组股票代码

```cmd
orange>python mandarin.py basic 002271 002230
Done

orange>
```

![basic](./sample/v1_01_basic.png)

### detail

详细信息，仅能输入一支股票代码

```cmd
orange>python mandarin.py detail 002271
Done

orange>
```

![detail](./sample/v1_02_detail.png)

## Navel

股票信息查询

```cmd
orange>python manage.py runserver
Performing system checks...

System check identified no issues (0 silenced).

You have 14 unapplied migration(s). Your project may not work properly until you apply the migrations for app(s): admin, auth, contenttypes, sessions.
Run 'python manage.py migrate' to apply them.
December 16, 2017 - 20:37:06
Django version 2.0, using settings 'navel.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CTRL-BREAK.
```

![index](./sample/v2_01_index.png)

![annual_report](./sample/v2_02_annual_report.png)

![tick_data](./sample/v2_03_tick_data.png)

## Test

执行命令`python -m unittest -v`进行单元测试

```cmd
orange>python -m unittest
test_classifier_level_report (test_stock.TestStock) ... ok
test_get_annual_report (test_stock.TestStock) ... ok
test_get_balance_sheet (test_stock.TestStock) ... ok
test_get_basic_info (test_stock.TestStock) ... ok
test_get_level0_report (test_stock.TestStock) ... ok
test_get_level1_report (test_stock.TestStock) ... [Getting data:]##########################################################[Getting data:]##########################################################[Getting data:]##########################################################[Getting data:]##########################################################[Getting data:]##########################################################ok
test_get_margin_details (test_stock.TestStock) ... [Getting data:]#5929 rows data found.Please wait for a moment.###########ok
test_get_profit_statement (test_stock.TestStock) ... ok
test_get_quarterly_results (test_stock.TestStock) ... ok
test_get_tick_data (test_stock.TestStock) ... ok
test_pct_change (test_stock.TestStock) ... ok

----------------------------------------------------------------------
Ran 11 tests in 285.514s

OK

orange>
```
