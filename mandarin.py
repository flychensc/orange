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
def main(stocks):
    """
    main函数
    """
    basics = pd.DataFrame([get_basic_info(code) for code in stocks])
    basics.set_index(['股票代码'], inplace=True)

    year_yoy_list = []
    quarter_yoy_list = []
    quarter_qoq_list = []
    for code in stocks:
        annual_report = get_annual_report(code)
        year_yoy = annual_report.pct_change(axis=1).iloc[:, -1]

        year_yoy.rename(index=lambda x: x + '(%)', inplace=True)
        year_yoy = (year_yoy * 100).round(2)
        year_yoy.loc['股票代码'] = code
        year_yoy.loc['年报时间'] = str(year_yoy.name)[:10]

        quarterly_results = get_quarterly_results(code)
        # measure='YoY'
        quarter_yoy = quarterly_results.pct_change(axis=1).iloc[:, -1]
        # measure='QoQ'
        quarter_qoq = quarterly_results.pct_change(
            periods=4, axis=1).iloc[:, -1]

        # YoY
        quarter_yoy.rename(index=lambda x: x + '(%)', inplace=True)
        quarter_yoy = (quarter_yoy * 100).round(2)
        quarter_yoy.loc['股票代码'] = code
        quarter_yoy.loc['季报时间'] = str(quarter_yoy.name)[:10]

        # QoQ
        quarter_qoq.rename(index=lambda x: x + '(%)', inplace=True)
        quarter_qoq = (quarter_qoq * 100).round(2)
        quarter_qoq.loc['股票代码'] = code
        quarter_qoq.loc['季报时间'] = str(quarter_qoq.name)[:10]

        year_yoy_list.append(
            pd.concat([year_yoy,
                       get_level0_report(annual_report.iloc[:, -1])]))
        quarter_yoy_list.append(
            pd.concat([
                quarter_yoy,
                get_level0_report(quarterly_results.iloc[:, -1])
            ]))
        quarter_qoq_list.append(quarter_qoq)

    year_yoys = pd.DataFrame(year_yoy_list)
    year_yoys.set_index(['股票代码', '年报时间'], inplace=True)

    quarter_yoys = pd.DataFrame(quarter_yoy_list)
    quarter_yoys.set_index(['股票代码', '季报时间'], inplace=True)

    quarter_qoqs = pd.DataFrame(quarter_qoq_list)
    quarter_qoqs.set_index(['股票代码', '季报时间'], inplace=True)

    writer = ExcelWriter("orange.xls")

    basics.to_excel(writer, "基本信息")
    year_yoys.to_excel(writer, "年报对比")
    quarter_yoys.to_excel(writer, "季报同比")
    quarter_qoqs.to_excel(writer, "季报环比")

    writer.save()


if __name__ == "__main__":
    # pylint: disable=E1120
    main()
    # pylint: enable=E1120
