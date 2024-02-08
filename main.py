import os
import pathlib

import AI
import DownloadEmail
import OcrUtil
import ParseInvoice
import config

if __name__ == '__main__':
    # OcrUtil.ocr_invoice('./dzfp_24442000000000377692_20240101190922.pdf')
    # ParseInvoice.parse_invoice()
    # AI.ai_summary('汽车92号汽油费')
    DownloadEmail.download_email()
    # setting.parse_setting()
    # print(pathlib.Path('./dzfp_24442000000000377692_20240101190922.pdf').suffix)
    # os.rename('./dzfp_24442000000000377692_20240101190922.pdf','./newfile.pdf')