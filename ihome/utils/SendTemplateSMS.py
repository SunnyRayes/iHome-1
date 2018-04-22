# coding=gbk

# coding=utf-8

# -*- coding: UTF-8 -*-

from ihome.libs.ronglianyun.CCPRestSDK import REST
import ConfigParser

# ���ʺ�
accountSid = '8a216da862dcd1050162dd22ef400061'

# ���ʺ�Token
accountToken = 'cbf5863dbe3d4902b5ae89df49be2a62'

# Ӧ��Id
appId = '8a216da862dcd1050162dd22ef9f0068'

# �����ַ����ʽ���£�����Ҫдhttp://
serverIP = 'app.cloopen.com'

# ����˿�
serverPort = '8883'

# REST�汾��
softVersion = '2013-12-26'


# ����ģ�����
# @param to �ֻ�����
# @param datas �������� ��ʽΪ���� ���磺{'12','34'}���粻���滻���� ''
# @param $tempId ģ��Id

# ��װ������
class CCP(object):
    def __new__(cls, *args, **kwargs):
        if not hasattr(CCP, '_instance'):
            cls._instance = super(CCP, cls).__new__(cls, *args, **kwargs)
            cls._instance.rest = REST(serverIP, serverPort, softVersion)
            cls._instance.rest.setAccount(accountSid, accountToken)
            cls._instance.rest.setAppId(appId)
        return cls._instance

    def sendTemplateSMS(self, to, datas, tempId):
        # ��ʼ��REST SDK
        result = self.rest.sendTemplateSMS(to, datas, tempId)
        return int(result.get('statusCode'))
        # for k, v in result.iteritems():
        #
        #     if k == 'templateSMS':
        #         for k, s in v.iteritems():
        #             print '%s:%s' % (k, s)
        #     else:
        #         print '%s:%s' % (k, v)

