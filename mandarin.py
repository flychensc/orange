"""
Mandarin orange (柑橘)
普通命令
"""

import datetime
import click
import pandas as pd
from pandas import ExcelWriter

from stock import get_annual_report, get_quarterly_results
from stock import get_basic_info, get_level0_report

_DICT_QUARTER = {1: '-03-31', 2: '-06-30', 3: '-09-30', 4: '-12-31'}


def _to_quarter(mon):
    """
        根据月份获取季度
    Parameters
    ------
        mon:int
            月份
    return
    ------
        int
    """
    if mon in [1, 2, 3]:
        return 1
    elif mon in [4, 5, 6]:
        return 2
    elif mon in [7, 8, 9]:
        return 3
    elif mon in [10, 11, 12]:
        return 4
    else:
        raise TypeError('month error.')


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
        year = datetime.date.today().year
        try:
            year_yoy = get_annual_report(code, year)
        except KeyError:
            year -= 1
            year_yoy = get_annual_report(code, year)
        year_yoy.loc['股票代码'] = code
        year_yoy.loc['年报时间'] = "%s-12-31" % year

        year = datetime.date.today().year
        quarter = _to_quarter(datetime.date.today().month)
        try:
            quarter_yoy = get_quarterly_results(
                code, year, quarter, measure='YoY')
            quarter_qoq = get_quarterly_results(
                code, year, quarter, measure='QoQ')
        except KeyError:
            if quarter is 1:
                year -= 1
                quarter = 1
            else:
                quarter -= 1
            try:
                quarter_yoy = get_quarterly_results(
                    code, year, quarter, measure='YoY')
                quarter_qoq = get_quarterly_results(
                    code, year, quarter, measure='QoQ')
            except KeyError:
                if quarter is 1:
                    year -= 1
                    quarter = 1
                else:
                    quarter -= 1
                quarter_yoy = get_quarterly_results(
                    code, year, quarter, measure='YoY')
                quarter_qoq = get_quarterly_results(
                    code, year, quarter, measure='QoQ')
        quarter_yoy.loc['股票代码'] = code
        quarter_qoq.loc['股票代码'] = code
        quarter_yoy.loc['季报时间'] = "%s%s" % (year, _DICT_QUARTER[quarter])
        quarter_qoq.loc['季报时间'] = "%s%s" % (year, _DICT_QUARTER[quarter])

        year_yoy_list.append(
            pd.concat([
                year_yoy['增长率(%)'].rename(index=lambda x: x + '(%)'),
                get_level0_report(year_yoy)
            ]))
        quarter_yoy_list.append(
            pd.concat([
                quarter_yoy['增长率(%)'].rename(index=lambda x: x + '(%)'),
                get_level0_report(quarter_yoy)
            ]))
        quarter_qoq_list.append(
            pd.concat([
                quarter_qoq['增长率(%)'].rename(index=lambda x: x + '(%)'),
                get_level0_report(quarter_qoq)
            ]))

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
