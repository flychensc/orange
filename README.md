# Orange

小橙子基金主要用于股票投资，从基本面，技术面，消息面对A股市场进行筛选。

## Mandarin

获取股票的简单信息，生成到一个excel里

`python mandarin.py --help`

### basic

基础信息，支持输入一组股票代码

`python mandarin.py basic 002271 002230`

### detail

详细信息，仅能输入一支股票代码

`python mandarin.py detail 002271`

## Navel

股票信息查询

`python manage.py runserver`

### celery

启动celery后台任务

`celery -A navel worker -l info --concurrency=15`

清除celery后台任务

`celery -A navel purge`

## Test

执行命令`python -m unittest -v`进行单元测试

## wiki

更多详情可移步[wiki](https://github.com/flychensc/orange/wiki)页面
