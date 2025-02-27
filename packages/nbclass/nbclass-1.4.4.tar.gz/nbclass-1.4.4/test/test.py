# -*- coding: utf-8 -*-
"""
@ Created on 2024-09-04 15:48
---------
@summary: 
---------
@author: XiaoBai
"""

from nbclass import tools

import pyotp

# 生成pypi登录的第二重身份验证应用程序代码
key = '6ZKWQI4LZFBN27S7MHLYY5M3O3HZU4Z3'
totp = pyotp.TOTP(key)
print(totp.now())
"""
打包 python setup.py sdist bdist_wheel
发布 twine upload dist/* --repository nbclass
发布 twine upload dist/* --repository pygeocoding
pypi-AgEIcHlwaS5vcmcCJDAyMjI2MDVlLTgxMzEtNDlkMS1hYTFjLWFjY2M0NjM1ZDI4OQACD1sxLFsibmJjbGFzcyJdXQACLFsyLFsiOGYzYWQxNTUtMTY5ZS00ZDhiLWEwMWUtMjVkNzM1YTNlMjcxIl1dAAAGID_EjCEnf5IY5SZ97y1rKzAcSXWJXxWpipIj-Ee7LlyK  nbclass
pypi-AgEIcHlwaS5vcmcCJDQ2YTI4Y2MwLWY4NTQtNGViMy04M2FmLWE5ZDc1NTBjMDkwOAACKlszLCI5YWZhZjA2NS1kYmIxLTQ3YzAtYmRlOC05ZmVhZjY3NWFiY2UiXQAABiB-P4o-OTZY4NJAwa8kVLiDii7ZIbY9OJB_WHS9tNoSFA  geocoding
"""

