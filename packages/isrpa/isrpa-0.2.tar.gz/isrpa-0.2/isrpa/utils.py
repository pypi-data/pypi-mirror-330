import json
import os

import requests


def getUrl(port="9002"):
    """
        环境变量设置
        windows
        setx ipAddress "192.168.12.249"

        linux
        export ipAddress = "192.168.12.249"
        source /etc/profile
    :param port:
    :return:
    """

    ip_address = os.environ.get("ipAddress", "192.168.12.249")

    return "ws://" + ip_address + ":" + port


def upload_file(file_path, dic_path, port: str):
    """
    通知客户端上传文件
    :param file_path:
    :param dic_path:
    :param port:
    :return:
    """

    path = os.environ.get("ipAddress", "192.168.12.249")
    url = "http://" + path + "/isrpa/executeCmd"
    print(url)
    headers = {
        'Content-Type': 'application/json',  # 说明请求体是 JSON 格式
    }
    cmd_str = "proxy_manager_cli upload --port " + port + " --localfile " + file_path + " --destfile" + dic_path
    # 请求体的数据
    data = {
        'cmd_str': cmd_str
    }
    print(data)
    requests.post(url, headers=headers, json=data)


def vCode(image: str, code_type, apiKey, secretKey):
    """
    ocr 识别图片验证码
    :param image: 图片base64
    :param code_type: 8000
    :param apiKey:
    :param secretKey:
    :return:
    """
    url = "https://ai.i-search.com.cn/ocr/v2/vCode"
    print(url)
    headers = {
        'Content-Type': 'application/json',  # 说明请求体是 JSON 格式
    }

    # 请求体的数据
    data = {
        'image': image,
        'code_type': code_type,
        'apiKey': apiKey,
        'secretKey': secretKey
    }
    print(data)
    response = requests.post(url, headers=headers, json=data)
    status_code = response.status_code
    if status_code != 200:
        print("请求失败，状态码：", status_code)
        return {"error_msg": "failure", "error_code": status_code}

    return response.json()
