from cryptography.hazmat.backends.openssl import backend

print('\n')

print("OpenSSL版本:", backend.openssl_version_text())
# 检查是否存在CRYPTOGRAPHY_OPENSSL_300_OR_GREATER属性
print("是否使用OpenSSL 3.0+:", hasattr(backend._lib, 'CRYPTOGRAPHY_OPENSSL_300_OR_GREATER'))

print('\n')

import certifi
print(certifi.where())

print('\n')

from datetime import datetime as dt

a=dt.now().strftime("%Y%m%d%H%M%S")
print(a)
print('\n')