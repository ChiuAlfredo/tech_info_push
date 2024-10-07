import requests


burp0_url = "https://play.google.com:443/_/PlayStoreUi/data/batchexecute?rpcids=oCPfdb&source-path=%2Fstore%2Fapps%2Fdetails&f.sid=-6719535845938859562&bl=boq_playuiserver_20240821.08_p0&hl=zh_TW&authuser&soc-app=121&soc-platform=1&soc-device=1&_reqid=184696&rt=c"
burp0_cookies = {
    "AEC": "AQTF6HxZp5GFZSTkim6gdIcjMP5sRlMazbkEa1eghJnV569HPwlcHyG0cg",
    "NID": "516=s7ozvm79BDPLMkS_WsK1K_LqDXxoGNHchv2aP-oc1t004BC10I3ObFNJzqiS0-bwC1Bcxxp8G8PRqV_mY8VxdQ1MAk7hMm-TLRiU0h6VMb6te_DhM9X9VeOCHYINkozBxqI7LzOeDl7lTrhXxhQ6re1kTvj7zFryMzhJbHuJeiEmmo8YRgFl01WyYbq6Gp64qza0pi_665uSiRTFr79KU6RW8RD6pwnz-D1f3KKledY4X2Q3nKwzHZbDcw",
    "_gid": "GA1.3.1949168918.1724427093",
    "_gat_UA199959031": "1",
    "_gcl_au": "1.1.753665063.1724427093",
    "_ga": "GA1.1.1302599864.1724427093",
    "OTZ": "7702052_24_24__24_",
    "_ga_6VGGZHMLM2": "GS1.1.1724427093.1.0.1724427099.0.0.0",
}
burp0_headers = {
    "Sec-Ch-Ua": '"Chromium";v="127", "Not)A;Brand";v="99"',
    "X-Same-Domain": "1",
    "Accept-Language": "zh-TW",
    "Sec-Ch-Ua-Mobile": "?0",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.6533.100 Safari/537.36",
    "Sec-Ch-Ua-Arch": '""',
    "Sec-Ch-Ua-Form-Factors": "",
    "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8",
    "Sec-Ch-Ua-Full-Version": '""',
    "Sec-Ch-Ua-Platform-Version": '""',
    "Sec-Ch-Ua-Full-Version-List": "",
    "Sec-Ch-Ua-Bitness": '""',
    "Sec-Ch-Ua-Model": '""',
    "Sec-Ch-Ua-Wow64": "?0",
    "Sec-Ch-Ua-Platform": '"Windows"',
    "Accept": "*/*",
    "Origin": "https://play.google.com",
    "X-Client-Data": "CM76ygE=",
    "Sec-Fetch-Site": "same-origin",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Dest": "empty",
    "Referer": "https://play.google.com/",
    "Accept-Encoding": "gzip, deflate, br",
    "Priority": "u=1, i",
}
burp0_data = {
    "f.req": '[[["oCPfdb","[null,[2,1,[20,null,\\"CmgKZjAsMTAwMDAwMC41MTk1NTkzODM0LDg4MDQyNjA0Mjg2NSwiaHR0cDovL21hcmtldC5hbmRyb2lkLmNvbS9kZXRhaWxzP2lkPXYyOmNvbS5pZ3MubWpzdGFyMzE6MSIsMSxmYWxzZQ\\"],null,[null,null,null,null,null,null,null,null,2]],[\\"com.igs.mjstar31\\",7]]",null,"generic"]]]&'
}
response = requests.post(
    burp0_url, headers=burp0_headers, cookies=burp0_cookies, data=burp0_data
)

data = response.content.decode("utf-8", errors="replace").replace(")]}'\n\n15976\n", "")


import requests

burp0_url = "https://play.google.com:443/_/PlayStoreUi/data/batchexecute?rpcids=oCPfdb&source-path=%2Fstore%2Fapps%2Fdetails&f.sid=-6719535845938859562&bl=boq_playuiserver_20240821.08_p0&hl=zh_TW&authuser&soc-app=121&soc-platform=1&soc-device=1&_reqid=384696&rt=c"
burp0_cookies = {
    "AEC": "AQTF6HxZp5GFZSTkim6gdIcjMP5sRlMazbkEa1eghJnV569HPwlcHyG0cg",
    "_gid": "GA1.3.1949168918.1724427093",
    "_gcl_au": "1.1.753665063.1724427093",
    "_ga": "GA1.1.1302599864.1724427093",
    "OTZ": "7702052_24_24__24_",
    "_ga_6VGGZHMLM2": "GS1.1.1724427093.1.0.1724427099.0.0.0",
    "NID": "517=usQuUgwCdcH9GjiaoqmTcjamf_Lwe71UrlhlzvgkbkiZZf9RouHwAJN6EsMUpkne6RgRvrhS4U62pDX1aF2Tn7mONBtsfEMH4XtgeCChD5SvHZWrRFd0Fa6SjErbUrYJ2p15Relf61vQ9q0Mw00KO_rTMehEDcH-c8ipAyC0cxswf3O3cQRna0nWsyvyTnhjCn8YCKuhQvfni8Pj7vrbYYCCBl3IgImW3fzcz6oe_1lAd0XyowsDt4hO_g",
}
burp0_headers = {
    "Sec-Ch-Ua": '"Chromium";v="127", "Not)A;Brand";v="99"',
    "X-Same-Domain": "1",
    "Accept-Language": "zh-TW",
    "Sec-Ch-Ua-Mobile": "?0",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.6533.100 Safari/537.36",
    "Sec-Ch-Ua-Arch": '""',
    "Sec-Ch-Ua-Form-Factors": "",
    "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8",
    "Sec-Ch-Ua-Full-Version": '""',
    "Sec-Ch-Ua-Platform-Version": '""',
    "Sec-Ch-Ua-Full-Version-List": "",
    "Sec-Ch-Ua-Bitness": '""',
    "Sec-Ch-Ua-Model": '""',
    "Sec-Ch-Ua-Wow64": "?0",
    "Sec-Ch-Ua-Platform": '"Windows"',
    "Accept": "*/*",
    "Origin": "https://play.google.com",
    "X-Client-Data": "CM76ygE=",
    "Sec-Fetch-Site": "same-origin",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Dest": "empty",
    "Referer": "https://play.google.com/",
    "Accept-Encoding": "gzip, deflate, br",
    "Priority": "u=1, i",
}
burp0_data = {
    "f.req": '[[["oCPfdb","[null,[2,1,[20,null,\\"CmkKZzAsMTAwMDAwMC40NjE4MTQyNTQ1LDEwNDQxMjA0NDk1OTQsImh0dHA6Ly9tYXJrZXQuYW5kcm9pZC5jb20vZGV0YWlscz9pZD12Mjpjb20uaWdzLm1qc3RhcjMxOjEiLDEsZmFsc2U\\"],null,[null,null,null,null,null,null,null,null,2]],[\\"com.igs.mjstar31\\",7]]",null,"generic"]]]&'
}
burp0_data = {
    "f.req": '[[["oCPfdb","[null,[2,1,[20,null,\\"CmgKZjAsMTAwMDAwMC41MTk1NTkzODM0LDg4MDQyNjA0Mjg2NSwiaHR0cDovL21hcmtldC5hbmRyb2lkLmNvbS9kZXRhaWxzP2lkPXYyOmNvbS5pZ3MubWpzdGFyMzE6MSIsMSxmYWxzZQ\\"],null,[null,null,null,null,null,null,null,null,2]],[\\"com.igs.mjstar31\\",7]]",null,"generic"]]]&'
}
response = requests.post(
    burp0_url, headers=burp0_headers, cookies=burp0_cookies, data=burp0_data
)

data_1 = response.content.decode("utf-8", errors="replace").replace(
    ")]}'\n\n15976\n", ""
)

import base64
encoded_str = "Cn0KezAsVElNRVNUQU1QICIyMDE4LTExLTA5IDE2OjI5OjU2Ljg0ODk2OCswMCIsOTg5NTIxOTU3MTgwLCJodHRwOi8vbWFya2V0LmFuZHJvaWQuY29tL2RldGFpbHM_aWQ9djI6Y29tLndvbmRlcmNpc2U6MSIsMSxmYWxzZQ"
padding = len(encoded_str) % 4
if padding != 0:
    encoded_str += '=' * (4 - padding)

# Attempt to decode again
decoded_bytes = base64.b64decode(encoded_str,validate=False).decode('utf-8', errors='ignore')
decoded_str = decoded_bytes
decoded_str






string_to_encode = '\n}\n{0,TIMESTAMP "2018-11-09 16:29:56.848968+00",889521957180,"http://market.android.com/details\x1aY\x0f]Kۙ\x19\\\\NH\x0cK\x19[\x1c'
encoded_bytes = base64.b64encode(string_to_encode.encode('utf-8'))
encoded_str = encoded_bytes.decode('utf-8')
encoded_str


import requests

burp0_url = "https://play.google.com:443/_/PlayStoreUi/data/batchexecute?rpcids=oCPfdb&source-path=%2Fstore%2Fapps%2Fdetails&f.sid=-6719535845938859562&bl=boq_playuiserver_20240821.08_p0&hl=zh_TW&authuser&soc-app=121&soc-platform=1&soc-device=1&_reqid=584696&rt=c"
burp0_cookies = {"AEC": "AQTF6HxZp5GFZSTkim6gdIcjMP5sRlMazbkEa1eghJnV569HPwlcHyG0cg", "_gid": "GA1.3.1949168918.1724427093", "_gcl_au": "1.1.753665063.1724427093", "_ga": "GA1.1.1302599864.1724427093", "OTZ": "7702052_24_24__24_", "_ga_6VGGZHMLM2": "GS1.1.1724427093.1.0.1724427099.0.0.0", "NID": "517=usQuUgwCdcH9GjiaoqmTcjamf_Lwe71UrlhlzvgkbkiZZf9RouHwAJN6EsMUpkne6RgRvrhS4U62pDX1aF2Tn7mONBtsfEMH4XtgeCChD5SvHZWrRFd0Fa6SjErbUrYJ2p15Relf61vQ9q0Mw00KO_rTMehEDcH-c8ipAyC0cxswf3O3cQRna0nWsyvyTnhjCn8YCKuhQvfni8Pj7vrbYYCCBl3IgImW3fzcz6oe_1lAd0XyowsDt4hO_g"}
burp0_headers = {"Sec-Ch-Ua": "\"Chromium\";v=\"127\", \"Not)A;Brand\";v=\"99\"", "X-Same-Domain": "1", "Accept-Language": "zh-TW", "Sec-Ch-Ua-Mobile": "?0", "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.6533.100 Safari/537.36", "Sec-Ch-Ua-Arch": "\"\"", "Sec-Ch-Ua-Form-Factors": "", "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8", "Sec-Ch-Ua-Full-Version": "\"\"", "Sec-Ch-Ua-Platform-Version": "\"\"", "Sec-Ch-Ua-Full-Version-List": "", "Sec-Ch-Ua-Bitness": "\"\"", "Sec-Ch-Ua-Model": "\"\"", "Sec-Ch-Ua-Wow64": "?0", "Sec-Ch-Ua-Platform": "\"Windows\"", "Accept": "*/*", "Origin": "https://play.google.com", "X-Client-Data": "CM76ygE=", "Sec-Fetch-Site": "same-origin", "Sec-Fetch-Mode": "cors", "Sec-Fetch-Dest": "empty", "Referer": "https://play.google.com/", "Accept-Encoding": "gzip, deflate, br", "Priority": "u=1, i"}
burp0_data = {"f.req": "[[[\"oCPfdb\",\"[null,[2,1,[20,null,\\\"CmgKZjAsMTAwMDAwMC40MzM3MDE5MDI2LDk0MDIwOTE2NDQ3OCwiaHR0cDovL21hcmtldC5hbmRyb2lkLmNvbS9kZXRhaWxzP2lkPXYyOmNvbS5pZ3MubWpzdGFyMzE6MSIsMSxmYWxzZQ\\\"],null,[null,null,null,null,null,null,null,null,2]],[\\\"com.igs.mjstar31\\\",7]]\",null,\"generic\"]]]&"}
response = requests.post(
    burp0_url, headers=burp0_headers, cookies=burp0_cookies, data=burp0_data
)


import requests

burp0_url = "https://play.google.com:443/_/PlayStoreUi/data/batchexecute?rpcids=oCPfdb&source-path=%2Fstore%2Fapps%2Fdetails&f.sid=-6719535845938859562&bl=boq_playuiserver_20240821.08_p0&hl=zh_TW&authuser&soc-app=121&soc-platform=1&soc-device=1&_reqid=784696&rt=c"
burp0_cookies = {"AEC": "AQTF6HxZp5GFZSTkim6gdIcjMP5sRlMazbkEa1eghJnV569HPwlcHyG0cg", "_gid": "GA1.3.1949168918.1724427093", "_gcl_au": "1.1.753665063.1724427093", "_ga": "GA1.1.1302599864.1724427093", "OTZ": "7702052_24_24__24_", "_ga_6VGGZHMLM2": "GS1.1.1724427093.1.0.1724427099.0.0.0", "NID": "517=usQuUgwCdcH9GjiaoqmTcjamf_Lwe71UrlhlzvgkbkiZZf9RouHwAJN6EsMUpkne6RgRvrhS4U62pDX1aF2Tn7mONBtsfEMH4XtgeCChD5SvHZWrRFd0Fa6SjErbUrYJ2p15Relf61vQ9q0Mw00KO_rTMehEDcH-c8ipAyC0cxswf3O3cQRna0nWsyvyTnhjCn8YCKuhQvfni8Pj7vrbYYCCBl3IgImW3fzcz6oe_1lAd0XyowsDt4hO_g"}
burp0_headers = {"Sec-Ch-Ua": "\"Chromium\";v=\"127\", \"Not)A;Brand\";v=\"99\"", "X-Same-Domain": "1", "Accept-Language": "zh-TW", "Sec-Ch-Ua-Mobile": "?0", "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.6533.100 Safari/537.36", "Sec-Ch-Ua-Arch": "\"\"", "Sec-Ch-Ua-Form-Factors": "", "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8", "Sec-Ch-Ua-Full-Version": "\"\"", "Sec-Ch-Ua-Platform-Version": "\"\"", "Sec-Ch-Ua-Full-Version-List": "", "Sec-Ch-Ua-Bitness": "\"\"", "Sec-Ch-Ua-Model": "\"\"", "Sec-Ch-Ua-Wow64": "?0", "Sec-Ch-Ua-Platform": "\"Windows\"", "Accept": "*/*", "Origin": "https://play.google.com", "X-Client-Data": "CM76ygE=", "Sec-Fetch-Site": "same-origin", "Sec-Fetch-Mode": "cors", "Sec-Fetch-Dest": "empty", "Referer": "https://play.google.com/", "Accept-Encoding": "gzip, deflate, br", "Priority": "u=1, i"}
burp0_data = {"f.req": "[[[\"oCPfdb\",\"[null,[2,1,[20,null,\\\"CmkKZzAsMTAwMDAwMC4yMjgxMjIyNzk2LDEwODExMDc0MDIxNzAsImh0dHA6Ly9tYXJrZXQuYW5kcm9pZC5jb20vZGV0YWlscz9pZD12Mjpjb20uaWdzLm1qc3RhcjMxOjEiLDEsZmFsc2U\\\"],null,[null,null,null,null,null,null,null,null,2]],[\\\"com.igs.mjstar31\\\",7]]\",null,\"generic\"]]]&"}
response = requests.post(
    burp0_url, headers=burp0_headers, cookies=burp0_cookies, data=burp0_data
)

data = response.content.decode("utf-8", errors="replace").replace(")]}'\n\n15976\n", "")


#######

import requests

burp0_url = "https://play.google.com:443/_/PlayStoreUi/data/batchexecute?rpcids=oCPfdb&source-path=%2Fstore%2Fapps%2Fdetails&f.sid=-2270059109566449797&bl=boq_playuiserver_20240821.08_p0&hl=zh_TW&authuser&soc-app=121&soc-platform=1&soc-device=1&_reqid=201598&rt=c"
burp0_cookies = {"AEC": "AQTF6HxZp5GFZSTkim6gdIcjMP5sRlMazbkEa1eghJnV569HPwlcHyG0cg", "_gid": "GA1.3.1949168918.1724427093", "_gcl_au": "1.1.753665063.1724427093", "OTZ": "7702052_24_24__24_", "NID": "517=usQuUgwCdcH9GjiaoqmTcjamf_Lwe71UrlhlzvgkbkiZZf9RouHwAJN6EsMUpkne6RgRvrhS4U62pDX1aF2Tn7mONBtsfEMH4XtgeCChD5SvHZWrRFd0Fa6SjErbUrYJ2p15Relf61vQ9q0Mw00KO_rTMehEDcH-c8ipAyC0cxswf3O3cQRna0nWsyvyTnhjCn8YCKuhQvfni8Pj7vrbYYCCBl3IgImW3fzcz6oe_1lAd0XyowsDt4hO_g", "_gat_UA199959031": "1", "_ga": "GA1.1.1302599864.1724427093", "_ga_6VGGZHMLM2": "GS1.1.1724430394.2.1.1724430397.0.0.0"}
burp0_headers = {"Sec-Ch-Ua": "\"Chromium\";v=\"127\", \"Not)A;Brand\";v=\"99\"", "X-Same-Domain": "1", "Accept-Language": "zh-TW", "Sec-Ch-Ua-Mobile": "?0", "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.6533.100 Safari/537.36", "Sec-Ch-Ua-Arch": "\"\"", "Sec-Ch-Ua-Form-Factors": "", "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8", "Sec-Ch-Ua-Full-Version": "\"\"", "Sec-Ch-Ua-Platform-Version": "\"\"", "Sec-Ch-Ua-Full-Version-List": "", "Sec-Ch-Ua-Bitness": "\"\"", "Sec-Ch-Ua-Model": "\"\"", "Sec-Ch-Ua-Wow64": "?0", "Sec-Ch-Ua-Platform": "\"Windows\"", "Accept": "*/*", "Origin": "https://play.google.com", "X-Client-Data": "CM76ygE=", "Sec-Fetch-Site": "same-origin", "Sec-Fetch-Mode": "cors", "Sec-Fetch-Dest": "empty", "Referer": "https://play.google.com/", "Accept-Encoding": "gzip, deflate, br", "Priority": "u=1, i"}
burp0_data = {"f.req": "[[[\"oCPfdb\",\"[null,[2,2,[20,null,\\\"Cn0KezAsVElNRVNUQU1QICIyMDIxLTA1LTMxIDA0OjI3OjE0LjkxMjkzOSswMCIsNTEwMTg3MzcxNjU0LCJodHRwOi8vbWFya2V0LmFuZHJvaWQuY29tL2RldGFpbHM_aWQ9djI6Y29tLndvbmRlcmNpc2U6MSIsMSxmYWxzZQ\\\"],null,[null,null,null,null,null,null,null,null,2]],[\\\"com.wondercise\\\",7]]\",null,\"generic\"]]]&"}
response = requests.post(
    burp0_url, headers=burp0_headers, cookies=burp0_cookies, data=burp0_data
)

data = response.content.decode("utf-8", errors="replace").replace(")]}'\n\n15976\n", "")


import requests

burp0_url = "https://play.google.com:443/_/PlayStoreUi/data/batchexecute?rpcids=oCPfdb&source-path=%2Fstore%2Fapps%2Fdetails&f.sid=-2270059109566449797&bl=boq_playuiserver_20240821.08_p0&hl=zh_TW&authuser&soc-app=121&soc-platform=1&soc-device=1&_reqid=101598&rt=c"
burp0_cookies = {"AEC": "AQTF6HxZp5GFZSTkim6gdIcjMP5sRlMazbkEa1eghJnV569HPwlcHyG0cg", "_gid": "GA1.3.1949168918.1724427093", "_gcl_au": "1.1.753665063.1724427093", "OTZ": "7702052_24_24__24_", "NID": "517=usQuUgwCdcH9GjiaoqmTcjamf_Lwe71UrlhlzvgkbkiZZf9RouHwAJN6EsMUpkne6RgRvrhS4U62pDX1aF2Tn7mONBtsfEMH4XtgeCChD5SvHZWrRFd0Fa6SjErbUrYJ2p15Relf61vQ9q0Mw00KO_rTMehEDcH-c8ipAyC0cxswf3O3cQRna0nWsyvyTnhjCn8YCKuhQvfni8Pj7vrbYYCCBl3IgImW3fzcz6oe_1lAd0XyowsDt4hO_g", "_gat_UA199959031": "1", "_ga": "GA1.1.1302599864.1724427093", "_ga_6VGGZHMLM2": "GS1.1.1724430394.2.1.1724430397.0.0.0"}
burp0_headers = {"Sec-Ch-Ua": "\"Chromium\";v=\"127\", \"Not)A;Brand\";v=\"99\"", "X-Same-Domain": "1", "Accept-Language": "zh-TW", "Sec-Ch-Ua-Mobile": "?0", "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.6533.100 Safari/537.36", "Sec-Ch-Ua-Arch": "\"\"", "Sec-Ch-Ua-Form-Factors": "", "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8", "Sec-Ch-Ua-Full-Version": "\"\"", "Sec-Ch-Ua-Platform-Version": "\"\"", "Sec-Ch-Ua-Full-Version-List": "", "Sec-Ch-Ua-Bitness": "\"\"", "Sec-Ch-Ua-Model": "\"\"", "Sec-Ch-Ua-Wow64": "?0", "Sec-Ch-Ua-Platform": "\"Windows\"", "Accept": "*/*", "Origin": "https://play.google.com", "X-Client-Data": "CM76ygE=", "Sec-Fetch-Site": "same-origin", "Sec-Fetch-Mode": "cors", "Sec-Fetch-Dest": "empty", "Referer": "https://play.google.com/", "Accept-Encoding": "gzip, deflate, br", "Priority": "u=1, i"}
burp0_data = {"f.req": "[[[\"oCPfdb\",\"[null,[2,2,[20],null,[null,null,null,null,null,null,null,null,2]],[\\\"com.wondercise\\\",7]]\",null,\"generic\"]]]&"}
response = requests.post(
    burp0_url, headers=burp0_headers, cookies=burp0_cookies, data=burp0_data
)

data = response.content.decode("utf-8", errors="replace").replace(")]}'\n\n15976\n", "")


import requests

burp0_url = "https://play.google.com:443/_/PlayStoreUi/data/batchexecute?rpcids=oCPfdb&source-path=%2Fstore%2Fapps%2Fdetails&f.sid=-2270059109566449797&bl=boq_playuiserver_20240821.08_p0&hl=zh_TW&authuser&soc-app=121&soc-platform=1&soc-device=1&_reqid=301598&rt=c"
burp0_cookies = {"AEC": "AQTF6HxZp5GFZSTkim6gdIcjMP5sRlMazbkEa1eghJnV569HPwlcHyG0cg", "_gid": "GA1.3.1949168918.1724427093", "_gcl_au": "1.1.753665063.1724427093", "OTZ": "7702052_24_24__24_", "NID": "517=usQuUgwCdcH9GjiaoqmTcjamf_Lwe71UrlhlzvgkbkiZZf9RouHwAJN6EsMUpkne6RgRvrhS4U62pDX1aF2Tn7mONBtsfEMH4XtgeCChD5SvHZWrRFd0Fa6SjErbUrYJ2p15Relf61vQ9q0Mw00KO_rTMehEDcH-c8ipAyC0cxswf3O3cQRna0nWsyvyTnhjCn8YCKuhQvfni8Pj7vrbYYCCBl3IgImW3fzcz6oe_1lAd0XyowsDt4hO_g", "_gat_UA199959031": "1", "_ga": "GA1.1.1302599864.1724427093", "_ga_6VGGZHMLM2": "GS1.1.1724430394.2.1.1724430397.0.0.0"}
burp0_headers = {"Sec-Ch-Ua": "\"Chromium\";v=\"127\", \"Not)A;Brand\";v=\"99\"", "X-Same-Domain": "1", "Accept-Language": "zh-TW", "Sec-Ch-Ua-Mobile": "?0", "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.6533.100 Safari/537.36", "Sec-Ch-Ua-Arch": "\"\"", "Sec-Ch-Ua-Form-Factors": "", "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8", "Sec-Ch-Ua-Full-Version": "\"\"", "Sec-Ch-Ua-Platform-Version": "\"\"", "Sec-Ch-Ua-Full-Version-List": "", "Sec-Ch-Ua-Bitness": "\"\"", "Sec-Ch-Ua-Model": "\"\"", "Sec-Ch-Ua-Wow64": "?0", "Sec-Ch-Ua-Platform": "\"Windows\"", "Accept": "*/*", "Origin": "https://play.google.com", "X-Client-Data": "CM76ygE=", "Sec-Fetch-Site": "same-origin", "Sec-Fetch-Mode": "cors", "Sec-Fetch-Dest": "empty", "Referer": "https://play.google.com/", "Accept-Encoding": "gzip, deflate, br", "Priority": "u=1, i"}
burp0_data = {"f.req": "[[[\"oCPfdb\",\"[null,[2,2,[20,null,\\\"Cn0KezAsVElNRVNUQU1QICIyMDE4LTExLTA5IDE2OjI5OjU2Ljg0ODk2OCswMCIsOTg5NTIxOTU3MTgwLCJodHRwOi8vbWFya2V0LmFuZHJvaWQuY29tL2RldGFpbHM_aWQ9djI6Y29tLndvbmRlcmNpc2U6MSIsMSxmYWxzZQ\\\"],null,[null,null,null,null,null,null,null,null,2]],[\\\"com.wondercise\\\",7]]\",null,\"generic\"]]]&"}
response = requests.post(
    burp0_url, headers=burp0_headers, cookies=burp0_cookies, data=burp0_data
)

data = response.content.decode("utf-8", errors="replace").replace(")]}'\n\n15976\n", "")


Cn0KezAsVElNRVNUQU1QICIyMDE4LTExLTA5IDE2OjI5OjU2Ljg0ODk2OCswMCIsODg5NTIxOTU3MTgwLCJodHRwOi8vbWFya2V0LmFuZHJvaWQuY29tL2RldGFpbHMaWQ9dS9uZGVxcTkgMSxlbHA

import requests

burp0_url = "https://play.google.com:443/_/PlayStoreUi/data/batchexecute?rpcids=oCPfdb&source-path=%2Fstore%2Fapps%2Fdetails&f.sid=-2270059109566449797&bl=boq_playuiserver_20240821.08_p0&hl=zh_TW&authuser&soc-app=121&soc-platform=1&soc-device=1&_reqid=301598&rt=c"
burp0_cookies = {"AEC": "AQTF6HxZp5GFZSTkim6gdIcjMP5sRlMazbkEa1eghJnV569HPwlcHyG0cg", "_gid": "GA1.3.1949168918.1724427093", "_gcl_au": "1.1.753665063.1724427093", "OTZ": "7702052_24_24__24_", "NID": "517=usQuUgwCdcH9GjiaoqmTcjamf_Lwe71UrlhlzvgkbkiZZf9RouHwAJN6EsMUpkne6RgRvrhS4U62pDX1aF2Tn7mONBtsfEMH4XtgeCChD5SvHZWrRFd0Fa6SjErbUrYJ2p15Relf61vQ9q0Mw00KO_rTMehEDcH-c8ipAyC0cxswf3O3cQRna0nWsyvyTnhjCn8YCKuhQvfni8Pj7vrbYYCCBl3IgImW3fzcz6oe_1lAd0XyowsDt4hO_g", "_gat_UA199959031": "1", "_ga": "GA1.1.1302599864.1724427093", "_ga_6VGGZHMLM2": "GS1.1.1724430394.2.1.1724430397.0.0.0"}
burp0_headers = {"Sec-Ch-Ua": "\"Chromium\";v=\"127\", \"Not)A;Brand\";v=\"99\"", "X-Same-Domain": "1", "Accept-Language": "zh-TW", "Sec-Ch-Ua-Mobile": "?0", "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.6533.100 Safari/537.36", "Sec-Ch-Ua-Arch": "\"\"", "Sec-Ch-Ua-Form-Factors": "", "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8", "Sec-Ch-Ua-Full-Version": "\"\"", "Sec-Ch-Ua-Platform-Version": "\"\"", "Sec-Ch-Ua-Full-Version-List": "", "Sec-Ch-Ua-Bitness": "\"\"", "Sec-Ch-Ua-Model": "\"\"", "Sec-Ch-Ua-Wow64": "?0", "Sec-Ch-Ua-Platform": "\"Windows\"", "Accept": "*/*", "Origin": "https://play.google.com", "X-Client-Data": "CM76ygE=", "Sec-Fetch-Site": "same-origin", "Sec-Fetch-Mode": "cors", "Sec-Fetch-Dest": "empty", "Referer": "https://play.google.com/", "Accept-Encoding": "gzip, deflate, br", "Priority": "u=1, i"}
burp0_data = {"f.req": "[[[\"oCPfdb\",\"[null,[2,2,[20,null,\\\"Cn0KezAsVElNRVNUQU1QICIyMDE4LTExLTA5IDE2OjI5OjU2Ljg0ODk2OCswMCIsODg5NTIxOTU3MTgwLCJodHRwOi8vbWFya2V0LmFuZHJvaWQuY29tL2RldGFpbHMaWQ9dS9uZGVxcTkgMSxlbHAQ\\\"],null,[null,null,null,null,null,null,null,null,2]],[\\\"com.wondercise\\\",7]]\",null,\"generic\"]]]&"}
response = requests.post(
    burp0_url, headers=burp0_headers, cookies=burp0_cookies, data=burp0_data
)

data = response.content.decode("utf-8", errors="replace").replace(")]}'\n\n15976\n", "")
