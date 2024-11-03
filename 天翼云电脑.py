import requests
import json
import hashlib
import time

def send_post_request(url, headers, data):
    response = requests.post(url, headers=headers, data=data)
    return response.json()

# 用户配置的参数
user_account = "13xxxxxxx"  # 手机号示例值，请按实际情况替换
password = "2d1fa0df154021xxxxxxxxxxxxxxxxxxx7b1fb417bf92521548"    # 密码示例值，请按实际情况替换
device_code = "web_gOlq7yuKuHMXRNwOxMK0Lt6Dq80iPFSi"  # 设备码示例值，请按实际情况替换
objId = "14889277"	# 云电脑页面ID值后八位


deviceName = "火狐浏览器",
sysVersion = "Windows+NT+10.0;+Win64;+x64;+rv:127.0",
deviceTypeValue = "60"

requestIdValue = str(int(time.time() * 1000))
tenantIdValue = "250432"
versionValue = "201360101"

# 登录请求
login_url = "https://desk.ctyun.cn:8810/api/auth/client/login"
login_headers = {
    "Host": "desk.ctyun.cn:8810",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:127.0) Gecko/20100101 Firefox/127.0",
    "Accept": "application/json, text/plain, */*",
    "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Content-Type": "application/x-www-form-urlencoded",
    "Referer": "https://pc.ctyun.cn/",
    "Origin": "https://pc.ctyun.cn",
    "CTG-APPMODEL": "2",
    "CTG-DEVICECODE": device_code,
    "CTG-DEVICETYPE": "60",
    "CTG-REQUESTID":  requestIdValue,  # 这个可能需要动态生成或调整
    "CTG-TIMESTAMP":  str(int(time.time() * 1000)),  # 同上
    "CTG-VERSION": "201360101",
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-site",
    "Connection": "keep-alive",
    "Priority": "u=1",
    "TE": "trailers",
}
login_data = {
    "userAccount": user_account,
    "password": password,
    "sha256Password": password,  # 计算密码的SHA256
    "deviceCode": device_code,
    "deviceName": deviceName,
    "hostName": deviceName,
    "deviceType": "60",
    "deviceModel": sysVersion,
    "appVersion": "1.36.1",
    "sysVersion": sysVersion,
    "clientVersion": "201360101",
    # 其他设备信息保持不变，可根据实际情况调整
}

login_response = send_post_request(login_url, login_headers, login_data)
print("登录用户ID:", login_response["data"]["userId"])
# 检查登录是否成功
if login_response.get("code") == 0:
    # 提取登录后的必要信息以构造第二个请求的头部和数据
    tenant_id = str(login_response["data"]["tenantId"])
    user_id = str(login_response["data"]["userId"])
    secretKey =str(login_response["data"]["secretKey"])
    timestampValue = str(int(time.time() * 1000))
    signatureStr = deviceTypeValue + requestIdValue + tenant_id + timestampValue + user_id + versionValue + secretKey

    hash_object = hashlib.md5(signatureStr.encode())
    md5_hash = hash_object.hexdigest().upper()

    # 连接桌面请求
    connect_url = "https://desk.ctyun.cn:8810/api/desktop/client/connect"
    connect_headers = {
        "Accept": "application/json, text/plain, */*",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
        "Connection": "keep-alive",
        "Content-Type": "application/x-www-form-urlencoded",
        "CTG-APPMODEL": "2",
        "CTG-DEVICECODE": device_code,
        "CTG-DEVICETYPE": "60",
        "CTG-REQUESTID":  requestIdValue,  # 这个可能需要动态生成或调整
        "CTG-SIGNATURESTR": md5_hash,  # 注意这个签名可能需要根据实际逻辑生成
        "CTG-TENANTID": tenant_id,
        'ctg-timestamp': timestampValue,
        "CTG-USERID": user_id,
        "CTG-VERSION": "201360101",
        "Host": "desk.ctyun.cn:8810",
        "Origin": "https://pc.ctyun.cn",
        "Referer": "https://pc.ctyun.cn/",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-site",
        "TE": "trailers",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:127.0) Gecko/20100101 Firefox/127.0",
    }
    connect_data = {
        "objId": objId,
        "objType": "0",
        "osType": "15",
        "deviceId": "60",
        "deviceCode": device_code,
        "deviceName": deviceName,
        "sysVersion": sysVersion,
        "appVersion": "1.36.1",
        "hostName": deviceName,
        "vdCommand":"",
        "ipAddress":"",
        "macAddress":"",
        "hardwareFeatureCode":device_code,
    }
    
    connect_response = send_post_request(connect_url, connect_headers, connect_data)
    if connect_response.get("code") == 0:
        print("连接桌面响应:", connect_response["data"]["desktopId"])
         # 提取登录后的必要信息以构造第二个请求的头部和数据
        token = str(connect_response["data"]["desktopInfo"]["token"])
        timestampValue2 = str(int(time.time() * 1000))

        signatureStr = deviceTypeValue + requestIdValue + tenant_id + timestampValue2 + user_id + versionValue + secretKey

        hash_object = hashlib.md5(signatureStr.encode())
        md5_hash = hash_object.hexdigest().upper()

        # 连接桌面请求
        connect2_url = "https://desk.ctyun.cn:8810/api/desktop/client/state"
        connect2_headers = {
            "Accept": "application/json, text/plain, */*",
            "Accept-Encoding": "gzip, deflate, br, zstd",
            "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
            "Connection": "keep-alive",
            "Content-Type": "application/json",
            "CTG-APPMODEL": "2",
            "CTG-DEVICECODE": device_code,
            "CTG-DEVICETYPE": "60",
            "CTG-REQUESTID":  requestIdValue,  # 这个可能需要动态生成或调整
            "CTG-SIGNATURESTR": md5_hash,  # 注意这个签名可能需要根据实际逻辑生成
            "CTG-TENANTID": tenant_id,
            'ctg-timestamp': timestampValue2,
            "CTG-USERID": user_id,
            "CTG-VERSION": "201360101",
            "Host": "desk.ctyun.cn:8810",
            "Origin": "https://pc.ctyun.cn",
            "Referer": "https://pc.ctyun.cn/",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-site",
            "TE": "trailers",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:127.0) Gecko/20100101 Firefox/127.0",
            
            "X-AUTH-TOKEN":token,
            # 其他头部保持与登录请求一致或做适当调整
        }
        connect2_data = [{"objId":objId,"objType":0}]
        

        connect2_response = send_post_request(connect2_url, connect2_headers, data=json.dumps(connect2_data))
        if connect2_response.get("code") == 0:
            print("桌面状态:", connect2_response["data"][0]["desktopState"])
        else:
            print("检测状态:",connect2_response)
    
else:
    print("登录失败，请检查账号密码。")