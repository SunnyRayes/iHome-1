# -*- coding: utf-8 -*-
# flake8: noqa
from qiniu import Auth, put_data

# 需要填写你的 Access Key 和 Secret Key
access_key = 'yV4GmNBLOgQK-1Sn3o4jktGLFdFSrlywR2C-hvsW'
secret_key = 'bixMURPL6tHjrb8QKVg2tm7n9k8C7vaOeQ4MEoeW'

# 上传空间
bucket_name = 'ihome'


def upload_image(img_data):
    # 构建鉴权对象
    q = Auth(access_key, secret_key)

    # 生成上传 Token，可以指定过期时间等
    token = q.upload_token(bucket_name)

    ret, info = put_data(token, None, img_data)

    if info.status_code == 200:
        return ret.get('key')

    raise Exception('上传图片失败')

if __name__ == '__main__':
    with open('/home/shayv/Pictures/111.png', 'rb') as f:
        img_data = f.read()
    upload_image(img_data)
