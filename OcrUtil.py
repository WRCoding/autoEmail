import base64
import json
from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.ocr.v20181119 import ocr_client, models


def transfer_base64(file_path):
    with open(file_path, 'rb') as file:
        content = file.read()
        return base64.b64encode(content).decode('utf-8')


def ocr_invoice(file_path):
    try:
        cred = credential.Credential("", "")
        # 实例化一个http选项，可选的，没有特殊需求可以跳过
        httpProfile = HttpProfile()
        httpProfile.endpoint = "ocr.tencentcloudapi.com"

        # 实例化一个client选项，可选的，没有特殊需求可以跳过
        clientProfile = ClientProfile()
        clientProfile.httpProfile = httpProfile
        # 实例化要请求产品的client对象,clientProfile是可选的
        client = ocr_client.OcrClient(cred, "ap-guangzhou", clientProfile)

        # 实例化一个请求对象,每个接口都会对应一个request对象
        req = models.RecognizeGeneralInvoiceRequest()
        params = {
            "ImageBase64": transfer_base64(file_path)
        }
        req.from_json_string(json.dumps(params))

        # 返回的resp是一个RecognizeGeneralInvoiceResponse的实例，与请求对象对应
        resp = client.RecognizeGeneralInvoice(req)
        # print(resp.to_json_string())
        # print(resp.MixedInvoiceItems[0])
        dict = json.loads(resp.to_json_string())
        subType = dict['MixedInvoiceItems'][0]['SubType']
        # print(subType)
        # print(dict['MixedInvoiceItems'][0]['SingleInvoiceInfos'])
        singleInvoiceInfos = json.dumps(dict['MixedInvoiceItems'][0]['SingleInvoiceInfos'])
        # print(singleInvoiceInfos)
        # print(json.loads(singleInvoiceInfos)[subType])
        return json.loads(singleInvoiceInfos)[subType]

    except TencentCloudSDKException as err:
        print(err)
        return None
