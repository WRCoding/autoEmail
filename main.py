import time

from ai.AIRegister import AIRegister
from ai.GPT import GPT
# import DownloadEmail

if __name__ == '__main__':
    # OcrUtil.ocr_invoice('./dzfp_24442000000000377692_20240101190922.pdf')
    # ParseInvoice.parse_invoice()
    # AI.ai_summary('汽车92号汽油费')
    # start = time.time()
    # DownloadEmail.download_email()
    # end = time.time()
    # print(f'执行时长: {end - start}')
    # AI.find_url(user_input.input)
    # setting.parse_setting()
    # print(pathlib.Path('./dzfp_24442000000000377692_20240101190922.pdf').suffix)
    # os.rename('./dzfp_24442000000000377692_20240101190922.pdf','./newfile.pdf')
    AIRegister.get_ai('GPT')
    print(type(GPT()))

