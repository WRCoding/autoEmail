import json
import os.path

import OcrUtil
import config
import util


def parse_invoice():
    invoice_list = get_invoice_list()
    location = config.get_location()
    for invoice in invoice_list:
        file_path = os.path.join(location, invoice)
        invoice_info = OcrUtil.ocr_invoice(file_path)
        new_file_name = get_new_file_name(invoice_info)
        util.rename(invoice, new_file_name)
        print(f'{invoice} : {new_file_name}')


def get_new_file_name(invoice_info):
    date = util.parse_date(invoice_info['Date'], '%Y年%m月%d日', '%Y%m%d')
    summary = get_summary(invoice_info)
    return summary + '_' + invoice_info['Number'] + '_' + invoice_info['Total'].split('.')[0] + '_' + date


def get_summary(item):
    if 'VatElectronicItems' in item:
        info = json.loads(json.dumps(item['VatElectronicItems']))
    else:
        info = json.loads(json.dumps(item['VatInvoiceItemInfos']))
    return AI.ai_summary(info[0]['Name'])


def get_invoice_list():
    path = config.get_location()
    if not os.path.exists(path):
        print(f'文件路径{path}不存在')
        return
    file_list = [f for f in os.listdir(path) if
                 os.path.isfile(os.path.join(path, f))]
    return file_list
