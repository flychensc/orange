from django.db import models

# Create your models here.


class StockBasics(models.Model):
    """
        沪深上市公司基本情况
        code,代码
        name,名称
        industry,细分行业
        area,地区
        pe,市盈率
        outstanding,流通股本
        totals,总股本(万)
        totalAssets,总资产(万)
        liquidAssets,流动资产
        fixedAssets,固定资产
        reserved,公积金
        reservedPerShare,每股公积金
        eps,每股收益
        bvps,每股净资
        pb,市净率
        timeToMarket,上市日期
    """
    code = models.CharField(max_length=6, primary_key=True, db_index=True)
    name = models.CharField(max_length=8)
    industry = models.CharField(max_length=8)
    area = models.CharField(max_length=8)
    pe = models.FloatField()
    outstanding = models.FloatField()
    totals = models.FloatField()
    totalAssets = models.FloatField()
    liquidAssets = models.FloatField()
    fixedAssets = models.FloatField()
    reserved = models.FloatField()
    reservedPerShare = models.FloatField()
    eps = models.FloatField()
    bvps = models.FloatField()
    pb = models.FloatField()
    timeToMarket = models.DateField()


class History(models.Model):
    """
    BAR数据
        code:代码
        open:开盘
        close:收盘
        high:最高价
        low:最低价
        vol:成交量
        amount:成交额
    """
    code = models.CharField(max_length=6)
    day = models.DateField()
    open = models.FloatField()
    close = models.FloatField()
    high = models.FloatField()
    low = models.FloatField()
    vol = models.FloatField()
    amount = models.FloatField()

    class Meta:
        unique_together = ("code", "day") 


class ReportData(models.Model):
    """
        业绩报表数据
        code,代码
        name,名称
        eps,每股收益
        eps_yoy,每股收益同比(%)
        bvps,每股净资产
        roe,净资产收益率(%)
        epcf,每股现金流量(元)
        net_profits,净利润(万元)
        profits_yoy,净利润同比(%)
        distrib,分配方案
        report_date,发布日期
    """
    code = models.CharField(max_length=6, primary_key=True, db_index=True)
    name = models.CharField(max_length=8) 
    eps = models.FloatField(null=True)
    eps_yoy = models.FloatField(null=True)   
    bvps = models.FloatField(null=True)
    roe = models.FloatField(null=True)
    epcf = models.FloatField(null=True)
    net_profits = models.FloatField(null=True)
    profits_yoy = models.FloatField(null=True)
    distrib = models.CharField(max_length=16, null=True)
    report_date = models.CharField(max_length=6)
