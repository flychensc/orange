"""
Mandarin orange (柑橘)
普通命令
"""

import click
import pandas as pd
from pandas import ExcelWriter

from stock import get_annual_report, get_quarterly_results
from stock import get_basic_info, get_level0_report


@click.command()
@click.argument('stocks', nargs=-1)
def simple(stocks):
    """
    simple report of stocks
    """
    # Get basic info from stocks
    basics = pd.DataFrame([get_basic_info(code) for code in stocks])
    basics.set_index(['股票代码'], inplace=True)

    year_yoy_list = []
    quarter_yoy_list = []
    quarter_qoq_list = []
    for code in stocks:
        # get annual report of stock
        annual_report = get_annual_report(code)
        # YoY
        year_yoy = annual_report.pct_change(axis=1).iloc[:, -1]
        # format
        year_yoy.rename(index=lambda x: x + '(%)', inplace=True)
        year_yoy = (year_yoy * 100).round(2)
        year_yoy.loc['股票代码'] = code
        year_yoy.loc['年报时间'] = str(year_yoy.name)[:10]
        # append
        year_yoy_list.append(
            pd.concat([year_yoy,
                       get_level0_report(annual_report.iloc[:, -1])]))

        # get quarterly results
        quarterly_results = get_quarterly_results(code)

        if str(quarterly_results.columns[-1])[4:10] != '-12-31':
            # measure='YoY'
            quarter_yoy = quarterly_results.pct_change(
                periods=4, axis=1).iloc[:, -1]

            # YoY
            quarter_yoy.rename(index=lambda x: x + '(%)', inplace=True)
            quarter_yoy = (quarter_yoy * 100).round(2)
            quarter_yoy.loc['股票代码'] = code
            quarter_yoy.loc['季报时间'] = str(quarter_yoy.name)[:10]

            quarter_yoy_list.append(
                pd.concat([
                    quarter_yoy,
                    get_level0_report(quarterly_results.iloc[:, -1])
                ]))

        if str(quarterly_results.columns[-1])[4:10] != '-03-31':
            # measure='QoQ'
            quarter_qoq = quarterly_results.pct_change(
                periods=1, axis=1).iloc[:, -1]

            # QoQ
            quarter_qoq.rename(index=lambda x: x + '(%)', inplace=True)
            quarter_qoq = (quarter_qoq * 100).round(2)
            quarter_qoq.loc['股票代码'] = code
            quarter_qoq.loc['季报时间'] = str(quarter_qoq.name)[:10]

            quarter_qoq_list.append(
                pd.concat([
                    quarter_qoq,
                    get_level0_report(quarterly_results.iloc[:, -1])
                ]))

    writer = ExcelWriter("orange.xls")

    basics.to_excel(writer, "基本信息")

    year_yoys = pd.DataFrame(year_yoy_list)
    year_yoys.set_index(['股票代码', '年报时间'], inplace=True)
    year_yoys.to_excel(writer, "年报对比")

    if quarter_yoy_list:
        quarter_yoys = pd.DataFrame(quarter_yoy_list)
        quarter_yoys.set_index(['股票代码', '季报时间'], inplace=True)
        quarter_yoys.to_excel(writer, "季报同比")

    if quarter_qoq_list:
        quarter_qoqs = pd.DataFrame(quarter_qoq_list)
        quarter_qoqs.set_index(['股票代码', '季报时间'], inplace=True)
        quarter_qoqs.to_excel(writer, "季报环比")

    writer.save()

@click.group()
@click.pass_context
def cli(cxn):
    """
    get report of stocks
    """
    click.echo("Done")


cli.add_command(simple)

if __name__ == "__main__":
    cli(obj={})
