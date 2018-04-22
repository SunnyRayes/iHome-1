# coding=gbk

# coding=utf-8

# -*- coding: UTF-8 -*-

from ihome.libs.ronglianyun.CCPRestSDK import REST
import ConfigParser

# 主帐号
accountSid = '8a216da862dcd1050162dd22ef400061'

# 主帐号Token
accountToken = 'cbf5863dbe3d4902b5ae89df49be2a62'

# 应用Id
appId = '8a216da862dcd1050162dd22ef9f0068'

# 请求地址，格式如下，不需要写http://
serverIP = 'app.cloopen.com'

# 请求端口
serverPort = '8883'

# REST版本号
softVersion = '2013-12-26'


# 发送模板短信
# @param to 手机号码
# @param datas 内容数据 格式为数组 例如：{'12','34'}，如不需替换请填 ''
# @param $tempId 模板Id

# 封装单例类
class CCP(object):
    def __new__(cls, *args, **kwargs):
        if not hasattr(CCP, '_instance'):
            cls._instance = super(CCP, cls).__new__(cls, *args, **kwargs)
            cls._instance.rest = REST(serverIP, serverPort, softVersion)
            cls._instance.rest.setAccount(accountSid, accountToken)
            cls._instance.rest.setAppId(appId)
        return cls._instance

    def sendTemplateSMS(self, to, datas, tempId):
        # 初始化REST SDK
        result = self.rest.sendTemplateSMS(to, datas, tempId)
        return int(result.get('statusCode'))
        # for k, v in result.iteritems():
        #
        #     if k == 'templateSMS':
        #         for k, s in v.iteritems():
        #             print '%s:%s' % (k, s)
        #     else:
        #         print '%s:%s' % (k, v)

