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
    """
    code = models.CharField(max_length=6)
    day = models.DateField()
    open = models.FloatField()
    close = models.FloatField()
    high = models.FloatField()
    low = models.FloatField()
    vol = models.FloatField()

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


class ProfitData(models.Model):
    """
        盈利能力数据
        code,代码
        name,名称
        roe,净资产收益率(%)
        net_profit_ratio,净利率(%)
        gross_profit_rate,毛利率(%)
        net_profits,净利润(万元)
        eps,每股收益
        business_income,营业收入(百万元)
        bips,每股主营业务收入(元)
    """
    code = models.CharField(max_length=6, primary_key=True, db_index=True)
    name = models.CharField(max_length=8)
    roe = models.FloatField(null=True)
    net_profit_ratio = models.FloatField(null=True)
    gross_profit_rate = models.FloatField(null=True)
    net_profits = models.FloatField(null=True)
    eps = models.FloatField(null=True)
    business_income = models.FloatField(null=True)
    bips = models.FloatField(null=True)


class OperationData(models.Model):
    """
        营运能力数据
        code,代码
        name,名称
        arturnover,应收账款周转率(次)
        arturndays,应收账款周转天数(天)
        inventory_turnover,存货周转率(次)
        inventory_days,存货周转天数(天)
        currentasset_turnover,流动资产周转率(次)
        currentasset_days,流动资产周转天数(天)
    """
    code = models.CharField(max_length=6, primary_key=True, db_index=True)
    name = models.CharField(max_length=8)
    arturnover = models.FloatField(null=True)
    arturndays = models.FloatField(null=True)
    inventory_turnover = models.FloatField(null=True)
    inventory_days = models.FloatField(null=True)
    currentasset_turnover = models.FloatField(null=True)
    currentasset_days = models.FloatField(null=True)


class GrowthData(models.Model):
    """
        成长能力数据
        code,代码
        name,名称
        mbrg,主营业务收入增长率(%)
        nprg,净利润增长率(%)
        nav,净资产增长率
        targ,总资产增长率
        epsg,每股收益增长率
        seg,股东权益增长率
    """
    code = models.CharField(max_length=6, primary_key=True, db_index=True)
    name = models.CharField(max_length=8)
    mbrg = models.FloatField(null=True)
    nprg = models.FloatField(null=True)
    nav = models.FloatField(null=True)
    targ = models.FloatField(null=True)
    epsg = models.FloatField(null=True)
    seg = models.FloatField(null=True)


class DebtpayingData(models.Model):
    """
        成长能力数据
        code,代码
        name,名称
        currentratio,流动比率
        quickratio,速动比率
        cashratio,现金比率
        icratio,利息支付倍数
        sheqratio,股东权益比率
        adratio,股东权益增长率
    """
    code = models.CharField(max_length=6, primary_key=True, db_index=True)
    name = models.CharField(max_length=8)
    currentratio = models.FloatField(null=True)
    quickratio = models.FloatField(null=True)
    cashratio = models.FloatField(null=True)
    icratio = models.FloatField(null=True)
    sheqratio = models.FloatField(null=True)
    adratio = models.FloatField(null=True)


class CashflowData(models.Model):
    """
        成长能力数据
        code,代码
        name,名称
        cf_sales,经营现金净流量对销售收入比率
        rateofreturn,资产的经营现金流量回报率
        cf_nm,经营现金净流量与净利润的比率
        cf_liabilities,经营现金净流量对负债比率
        cashflowratio,现金流量比率
    """
    code = models.CharField(max_length=6, primary_key=True, db_index=True)
    name = models.CharField(max_length=8)
    cf_sales = models.FloatField(null=True)
    rateofreturn = models.FloatField(null=True)
    cf_nm = models.FloatField(null=True)
    cf_liabilities = models.FloatField(null=True)
    cashflowratio = models.FloatField(null=True)


class Tick(models.Model):
    """
    分笔数据
        code:代码
        day:日期
        sec1_buy:区间1资金流入
        sec1_sell:区间1资金流出
        sec2_buy:区间2资金流入
        sec2_sell:区间2资金流出
        sec3_buy:区间3资金流入
        sec3_sell:区间3资金流出
        sec4_buy:区间4资金流入
        sec4_sell:区间4资金流出
    """
    code = models.CharField(max_length=6)
    day = models.DateField()
    # section: 9:30-10:30
    sec1_buy = models.FloatField()
    sec1_sell = models.FloatField()
    # section: 10:30-11:30
    sec2_buy = models.FloatField()
    sec2_sell = models.FloatField()
    # section: 13:00-14:00
    sec3_buy = models.FloatField()
    sec3_sell = models.FloatField()
    # section: 14:00-15:00
    sec4_buy = models.FloatField()
    sec4_sell = models.FloatField()

    class Meta:
        unique_together = ("code", "day") 


class Interest(models.Model):
    """
    自选股
        code:代码
        name:名称
        industry:行业
        policy:策略,[卖出，中性，关注，买入，持有]
        priceToBuy:买入价
        priceToSell:预期价格
        预期涨幅
        reasonToInterest:关注理由
        reasonToBuy:买入理由
        reasonToHold:持有理由
        reasonToSell:卖出理由
        createDay:创建日期
        updateDay:更新日期
    """
    code = models.CharField(max_length=6, primary_key=True, db_index=True)
    name = models.CharField(max_length=8)
    industry = models.CharField(max_length=8)

    policy = models.CharField(max_length=4)
    priceToBuy = models.FloatField()
    priceToSell = models.FloatField()

    reasonToInterest = models.TextField()
    reasonToBuy = models.TextField()
    reasonToHold = models.TextField()
    reasonToSell = models.TextField()

    createDay = models.DateField()
    updateDay = models.DateField()
