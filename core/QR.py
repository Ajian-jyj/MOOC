# -*- encoding: utf-8 -*-
"""
@File    :   login.py    
@Contact :   jyj345559953@qq.com
@Author  :   Esword
"""
from pyzbar.pyzbar import decode
from PIL import Image
import qrcode

# 公众号二维码图片显示
print('\n')
barcode_url = ''
barcodes = decode(Image.open('core\QR.png'))
for barcode in barcodes:
    barcode_url = barcode.data.decode("utf-8")
# print(barcode_url)

qr = qrcode.QRCode()
qr.add_data(barcode_url)
# invert=True白底黑块,有些app不识别黑底白块.
qr.print_ascii(invert=True)
print('\n')