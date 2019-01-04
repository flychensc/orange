# Orange

小橙子基金主要用于股票投资，从基本面，技术面，消息面对A股市场进行筛选。

## Mandarin

获取股票的简单信息，生成到一个excel里

### basic

列出一组股票的基础信息

例如： `python mandarin.py basic 002271 002230`

### detail

列出某支股票的详细信息

例如： `python mandarin.py detail 002271`

## Navel

一个WEB服务器，用于股票信息查询

启动命令： `python manage.py runserver 0.0.0.0:8000`

### celery

采用celery管理后台任务

启动命令： `celery -A navel worker -l info -c 15 -B`

#### web管理界面

命令: `celery -A navel flower`

## Test

执行命令`python -m unittest -v`进行单元测试

## Home Page

![主页](https://github.com/flychensc/orange/blob/master/sample/home.PNG)

## wiki

更多详情可移步[wiki](https://github.com/flychensc/orange/wiki)页面
