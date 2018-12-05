"""
消息面
"""

'''
    获取个股信息
Parameters
--------
    code:股票代码
    date:信息公布日期
Return
--------
    DataFrame，属性列表：
    title:信息标题
    type:信息类型
    date:公告日期
    url:信息内容URL
'''
# ts.get_notices(code, date)

'''
    获取信息地雷内容
Parameter
--------
    url:内容链接
Return
--------
    string:信息内容
'''
# ts.notice_content(url)
