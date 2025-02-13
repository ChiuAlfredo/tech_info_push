import requests
import json
import os 
import glob
from bs4 import BeautifulSoup
import re


import time
from functools import wraps
import pandas as pd
# 計算時間
def timing_decorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        elapsed_time = end_time - start_time
        print(f"Function {func.__name__} took {elapsed_time:.2f} seconds to run.")
        return result
    return wrapper

# 獲取頁面
def get_page_json(page_number,keyword,**kwargs):


    burp0_url = f"https://openapi.lenovo.com:443/us/en/ofp/search/global/cache/products/get/_tsc?fq=%3F&text={keyword}&rows=60&sort=relevance&display_tab=Products&page={page_number}&more=1"
    # burp0_cookies = {"zipcode": "60654", "leid": "2.jyl8T/tyDem", "AKA_A2": "A", "bm_sz": "98BB93CC1164DE89AD3375F37CF986DF~YAAQzONH0iA7d2KSAQAAEJKYZhl41bBkXSe/zVmTXbEGcpuDvoEgndtORkOIHXJj+hf1YGMx+ZD1cnafMwUZ7W2WaJHBILl60NkKTk009C0LVfAWBPPPHUjIB82sWrDEXAWQU/PcEG5PQAcGy6iz5tJf6Qg3K2tkp4PVR4qJbSg5sV4XfJGCe0JSUl10apPvH1fYpLKkg0p+J6+TVUx66lb98ISC6u04dwaQHtcArQLqD7a624BPHV4pDepKDp3JaVDJlH7jG6p/i6Nad2qYAUO2Pq6Nh3rcJmyjM0qznlVLzv61MwsT+iCGCNnZ4pMU0tXH7ZNURJ3P6nnJmA5hFaZ8kUgSZZCQguSzFUkUF/R0i9csCxPrb2MoSdMHFtF42GV6lVmxXQUhhZTySA==~3486777~4469048", "ak_bmsc": "5F67B13068F8622F7B20F0A929ABD4D6~000000000000000000000000000000~YAAQzONH0h88d2KSAQAAu5iYZhm5js/2uNaq9zMAct/J69obBAsSn5XG4itG4ZkvcJUXj44iWEZbnD2TCvJc6iBvbX9V46jyrwAz37qDGjkpIyB49kGBVSQ9ormcNyj9GoRCobB46Ed77/8lDU/qaWEyAB0CqUcxVLS9GKE2+r8M7hlt96iG3EpD3giHIrzvuWGOxSrgUtSqyLXgg+LD9dPW7Lk8e5FAMNyBGB8AgywfQCsX8vLsL01aCdLf9N3HcebvCXPhlv+CKGAUQT+aRjo4Z4Nd202aajqfFLDtq+UR4XXwgMo+ffjv+7RIPrH5uzICKffNpfzR/s3Gs2YxhCQjHiWm2kKa4zftMw1Pbe5AHd4+Oliczo17lfSi9Hg3DhD+4EA80YUkwa1ipKk5uM+V6eLoJ9N2x+oFIZX+obqOZHohdLpsdN3ctLQcXEuP2IkMow==", "searchabran": "40", "bm_sv": "538D69FC82FB1256C0235CBBF595A86C~YAAQzONH0nc8d2KSAQAAHJuYZhk0Ly2wHqwKVVxfEP0f/nLDZ7XVZhuF4T11y2brRmKBxuKBVUeSYCc2y4lk+a0uu0WUolO7VdsbinjGqVsf0aFHQ8FLBnDDDKqsYd+HECowIVvIR8BdPGdoWm6zzGIfDXnGywUeTKoPzAbIntroydbAbfCRZ6Y7I29DWs1g16J+3W8VmglW/EtUQBJ4fKX5gBU4xS1Y1EfBBanVqfi9WaWP2Oppr9/t5JFTsjIJ~1", "kndctr_F6171253512D2B8C0A490D45_AdobeOrg_cluster": "sgp3", "kndctr_F6171253512D2B8C0A490D45_AdobeOrg_identity": "CiY3OTQ1Mjc1MjU2MjYyNTEwMjY1MzgxMDczODg3NDQ4OTY5MzI2OVITCKm04rSmMhABGAEqBFNHUDMwAKABsLTitKYysAEG8AGptOK0pjI=", "AMCV_F6171253512D2B8C0A490D45%40AdobeOrg": "MCMID|79452752562625102653810738874489693269", "_abck": "B9AB135C27B773BCB14ABE60FD05380A~0~YAAQzONH0qk8d2KSAQAAU5yYZgx6Fd/xic8H3gmCYXLbNPvl4DJvbC4cYAwNzDNQvbu0MVmds2W/hQCHZ5ZZsznGBnIfGsPqK5IS0anFIhTaiQBBWVeiPpAkufHxRHp8YiK/bTuEm5REP9EqhqXR/3euKbczeyRdf0eY4nTKMorlivlsbfLUyjHF+Jg5lGxOdbCc2BMZpb8IFPKkN3iloOeyqm/42B+9DsEf0qd+POOdezwct/mY54rvHxsB3ZhdyFv5UhLHucXfXN6tpIL+/pk1yLxwC3Jmsh7BsxbINbQfSxserMc58qCGPUsH8KelA2Ba930ze8ZoPt8MQ1AuGsl4oYLwqPs5XpiLAEz0/HijQz8LOY5VBk2QBmzJmP7JLaIiL7cFivxVppSKKE3uC3jcb6toKDxqzhv/60CtQKzjtuocRoBcZMRjltEtkywpaNCYB+rGFy24~-1~||0||~1728301730"}
    burp0_headers = {"Sec-Ch-Ua": "\"Chromium\";v=\"127\", \"Not)A;Brand\";v=\"99\"", "Accept-Language": "zh-TW", "Sec-Ch-Ua-Mobile": "?0", "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.6533.100 Safari/537.36", "Sec-Ch-Ua-Platform": "\"Windows\"", "Accept": "*/*", "Origin": "https://www.lenovo.com", "Sec-Fetch-Site": "same-site", "Sec-Fetch-Mode": "cors", "Sec-Fetch-Dest": "empty", "Referer": "https://www.lenovo.com/us/en/search?fq=%3F&text=laptop&rows=20&sort=relevance&display_tab=Products&page=2&more=1", "Accept-Encoding": "gzip, deflate, br", "Priority": "u=1, i"}
    response = requests.get(burp0_url, headers=burp0_headers)

    data_json = response.json()["data"]['data'][0]['products']
    
    for index,i in enumerate(data_json):
        try :i['id']
        except:
            data_json.pop(index)

            

    web_url_list = ['https://www.lenovo.com/us/en/'+i['url'] for i in data_json]
    # for index,i in enumerate(data_json):
    #     i['productName']
    for index,i in enumerate(data_json):
        try :i['productName']
        except:
            i['productName'] = i['summary']
    product_name_list = [i['productName']for i in data_json]
    product_code_list = [i['productCode']for i in data_json]



    # url = f"https://www.lenovo.com/us/en/search?fq=%3F&text={keyword}&rows=60&sort=relevance&display_tab=Products&page={page_number}&more=1"
    # # url = 'https://www.lenovo.com/us/en/search?fq=%3F&text=laptop&rows=20&sort=relevance&display_tab=Products&page=2&more=1'
    # # url ='https://www.lenovo.com/us/en/search?fq={!ex=prodCat}lengs_Product_facet_ProdCategories:PCs%20Tablets&text=Laptops&rows=60&sort=relevance&display_tab=Products&more=1&page=11'
    # payload = {}

   
    # burp0_headers = {"Sec-Ch-Ua": "\"Chromium\";v=\"127\", \"Not)A;Brand\";v=\"99\"", "Sec-Ch-Ua-Mobile": "?0", "Sec-Ch-Ua-Platform": "\"Windows\"", "Accept-Language": "zh-TW", "Upgrade-Insecure-Requests": "1", "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.6533.100 Safari/537.36", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7", "Sec-Fetch-Site": "none", "Sec-Fetch-Mode": "navigate", "Sec-Fetch-User": "?1", "Sec-Fetch-Dest": "document", "Accept-Encoding": "gzip, deflate, br", "Priority": "u=0, i", "Connection": "keep-alive"}
    # response = requests.get(url, headers=burp0_headers)

    # print(page_number)


    # soup = BeautifulSoup(response.text, 'html.parser')
    # # print(soup)
    
    # # len(soup.select('.part_number'))
    
    # web_url_soup = soup.select('.product_item>.product_name>a')
    # product_name_soup = soup.select('.product_item>.product_name')
    # product_code_soup = soup.select('.product_item>.product_name>a')
    
    # web_url_list = [i.get('href') for i in web_url_soup]
    # product_name_list = [i.text for i in product_name_soup]
    # product_code_list = [i.get('data-productcode') for i in product_code_soup]
    
    product_number = len(web_url_list)
    print(len(product_name_list))
    
    return web_url_list,product_name_list,product_code_list,product_number

# 獲取thinksta
def get_page_json_thinksta(page_number,keyword,**kwargs):
    
    burp0_url = f"https://openapi.lenovo.com:443/us/en/ofp/search/global/cache/products/get/_tsc?fq=%7B!ex=prodCat%7Dlengs_Product_facet_ProdCategories:PCs%20Tablets&text={keyword}&rows=60&sort=relevance&display_tab=Products&page={page_number}&more=1"
    # burp0_cookies = {"zipcode": "60654", "leid": "2.jyl8T/tyDem", "AKA_A2": "A", "bm_sz": "98BB93CC1164DE89AD3375F37CF986DF~YAAQzONH0iA7d2KSAQAAEJKYZhl41bBkXSe/zVmTXbEGcpuDvoEgndtORkOIHXJj+hf1YGMx+ZD1cnafMwUZ7W2WaJHBILl60NkKTk009C0LVfAWBPPPHUjIB82sWrDEXAWQU/PcEG5PQAcGy6iz5tJf6Qg3K2tkp4PVR4qJbSg5sV4XfJGCe0JSUl10apPvH1fYpLKkg0p+J6+TVUx66lb98ISC6u04dwaQHtcArQLqD7a624BPHV4pDepKDp3JaVDJlH7jG6p/i6Nad2qYAUO2Pq6Nh3rcJmyjM0qznlVLzv61MwsT+iCGCNnZ4pMU0tXH7ZNURJ3P6nnJmA5hFaZ8kUgSZZCQguSzFUkUF/R0i9csCxPrb2MoSdMHFtF42GV6lVmxXQUhhZTySA==~3486777~4469048", "ak_bmsc": "5F67B13068F8622F7B20F0A929ABD4D6~000000000000000000000000000000~YAAQzONH0h88d2KSAQAAu5iYZhm5js/2uNaq9zMAct/J69obBAsSn5XG4itG4ZkvcJUXj44iWEZbnD2TCvJc6iBvbX9V46jyrwAz37qDGjkpIyB49kGBVSQ9ormcNyj9GoRCobB46Ed77/8lDU/qaWEyAB0CqUcxVLS9GKE2+r8M7hlt96iG3EpD3giHIrzvuWGOxSrgUtSqyLXgg+LD9dPW7Lk8e5FAMNyBGB8AgywfQCsX8vLsL01aCdLf9N3HcebvCXPhlv+CKGAUQT+aRjo4Z4Nd202aajqfFLDtq+UR4XXwgMo+ffjv+7RIPrH5uzICKffNpfzR/s3Gs2YxhCQjHiWm2kKa4zftMw1Pbe5AHd4+Oliczo17lfSi9Hg3DhD+4EA80YUkwa1ipKk5uM+V6eLoJ9N2x+oFIZX+obqOZHohdLpsdN3ctLQcXEuP2IkMow==", "searchabran": "40", "bm_sv": "538D69FC82FB1256C0235CBBF595A86C~YAAQzONH0nc8d2KSAQAAHJuYZhk0Ly2wHqwKVVxfEP0f/nLDZ7XVZhuF4T11y2brRmKBxuKBVUeSYCc2y4lk+a0uu0WUolO7VdsbinjGqVsf0aFHQ8FLBnDDDKqsYd+HECowIVvIR8BdPGdoWm6zzGIfDXnGywUeTKoPzAbIntroydbAbfCRZ6Y7I29DWs1g16J+3W8VmglW/EtUQBJ4fKX5gBU4xS1Y1EfBBanVqfi9WaWP2Oppr9/t5JFTsjIJ~1", "kndctr_F6171253512D2B8C0A490D45_AdobeOrg_cluster": "sgp3", "kndctr_F6171253512D2B8C0A490D45_AdobeOrg_identity": "CiY3OTQ1Mjc1MjU2MjYyNTEwMjY1MzgxMDczODg3NDQ4OTY5MzI2OVITCKm04rSmMhABGAEqBFNHUDMwAKABsLTitKYysAEG8AGptOK0pjI=", "AMCV_F6171253512D2B8C0A490D45%40AdobeOrg": "MCMID|79452752562625102653810738874489693269", "_abck": "B9AB135C27B773BCB14ABE60FD05380A~0~YAAQzONH0qk8d2KSAQAAU5yYZgx6Fd/xic8H3gmCYXLbNPvl4DJvbC4cYAwNzDNQvbu0MVmds2W/hQCHZ5ZZsznGBnIfGsPqK5IS0anFIhTaiQBBWVeiPpAkufHxRHp8YiK/bTuEm5REP9EqhqXR/3euKbczeyRdf0eY4nTKMorlivlsbfLUyjHF+Jg5lGxOdbCc2BMZpb8IFPKkN3iloOeyqm/42B+9DsEf0qd+POOdezwct/mY54rvHxsB3ZhdyFv5UhLHucXfXN6tpIL+/pk1yLxwC3Jmsh7BsxbINbQfSxserMc58qCGPUsH8KelA2Ba930ze8ZoPt8MQ1AuGsl4oYLwqPs5XpiLAEz0/HijQz8LOY5VBk2QBmzJmP7JLaIiL7cFivxVppSKKE3uC3jcb6toKDxqzhv/60CtQKzjtuocRoBcZMRjltEtkywpaNCYB+rGFy24~-1~||0||~1728301730"}
    burp0_headers = {"Sec-Ch-Ua": "\"Chromium\";v=\"127\", \"Not)A;Brand\";v=\"99\"", "Accept-Language": "zh-TW", "Sec-Ch-Ua-Mobile": "?0", "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.6533.100 Safari/537.36", "Sec-Ch-Ua-Platform": "\"Windows\"", "Accept": "*/*", "Origin": "https://www.lenovo.com", "Sec-Fetch-Site": "same-site", "Sec-Fetch-Mode": "cors", "Sec-Fetch-Dest": "empty", "Referer": "https://www.lenovo.com/us/en/search?fq=%3F&text=laptop&rows=20&sort=relevance&display_tab=Products&page=2&more=1", "Accept-Encoding": "gzip, deflate, br", "Priority": "u=1, i"}
    response = requests.get(burp0_url, headers=burp0_headers)

    data_json = response.json()["data"]['data'][0]['products']
    
    for index,i in enumerate(data_json):
        try :i['id']
        except:
            data_json.pop(index)

    web_url_list = ['https://www.lenovo.com/us/en/'+i['url'] for i in data_json]
    product_name_list = [i['productName']for i in data_json]
    product_code_list = [i['productCode']for i in data_json]



    # url = f'https://www.lenovo.com/us/en/search?fq=%7B!ex=prodCat%7Dlengs_Product_facet_ProdCategories:PCs%20Tablets&text={keyword}&rows=60&sort=relevance&display_tab=Products&page={page_number}&more=1'
    # print(url)
    # # url ='https://www.lenovo.com/us/en/search?fq={!ex=prodCat}lengs_Product_facet_ProdCategories:PCs%20Tablets&text=Laptops&rows=60&sort=relevance&display_tab=Products&more=1&page=11'
    # payload = {}
    
    # # headers ={
    # #     'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
    # #     # 'Cookie':'zipcode=60654; leid=2.Y+i9b/nJUlF; searchabran=2; AMCV_F6171253512D2B8C0A490D45%40AdobeOrg=MCMID|22796032703182726071512371125726346184; navposkey=pc_nav; fsid=19; BVBRANDID=da21a037-de34-4ab3-987a-52d6b0be7a7d; ftv_for_usen=%252Fpc%252F; aamtest1=auto%3D549200; Adform%20Cookie%20ID=4059607695632243559; fl_guid=5701551EFF6D83; _ga=GA1.1.1746570426.1696555783; _mibhv=anon-1696555783300-6860938145_4876; _gcl_au=1.1.1993526881.1696555784; _tt_enable_cookie=1; _ttp=TDYcYSlEw5lhQzyTmx1l-lsM8WM; _fbp=fb.1.1696555788053.1759168665; _mkto_trk=id:183-WCT-620&token:_mch-lenovo.com-1696555788090-60972; ki_r=; _rdt_uuid=1696555790511.3082e1b5-8344-465f-8dae-02c1afc93e2e; QuantumMetricUserID=309abf2bad683b1de82791752efec793; algorithmId_adobe=%7B%22algorithmId%22%3Anull%7D; ki_s=199507%3A0.0.0.0.0; bluecoreNV=false; aam_sc=aamsc%3D3901189%7C3872579%7C10138496%7C10137485%7C9562573%7C11003488; _scid=e996b99e-96bd-4d70-a8eb-ca87cc0a0ac4; _scid_r=e996b99e-96bd-4d70-a8eb-ca87cc0a0ac4; _sctr=1%7C1696953600000; apay-session-set=hzQOmnSszVvZwfIIZuAHKg8vrSREuk4Eo7ZDs%2FLOqVjpEhfkYJ5YVAYZyVc29BU%3D; has_consent_cookie=; kndctr_F6171253512D2B8C0A490D45_AdobeOrg_consent=general%3Din; fsid=19; _uetvid=d358ad0063e711ee9310ad79f9d8b198; _evidon_consent_cookie={"consent_date":"2023-10-06T01:45:02.780Z","categories":{"1":{"essential":true,"analytics":true,"advertising":false,"social media":false}},"vendors":{"1":{"11":true,"14":false,"17":false,"31":true,"51":false,"63":true,"66":false,"80":false,"81":false,"82":false,"84":false,"99":false,"103":true,"108":true,"111":true,"128":true,"131":false,"149":false,"167":true,"174":false,"242":true,"249":false,"253":true,"257":false,"259":false,"290":true,"307":true,"321":true,"348":false,"384":false,"395":true,"414":true,"426":false,"442":false,"467":true,"480":true,"523":true,"560":false,"611":true,"662":true,"674":false,"688":true,"828":true,"831":false,"905":false,"933":true,"937":true,"1028":false,"1267":false,"1272":true,"1306":false,"1412":false,"1647":true,"1727":true,"2230":true,"2516":false,"2594":true,"3042":true,"3058":true,"3355":true,"3490":false,"3778":true,"3878":true,"4160":false,"4526":false,"4748":true,"4948":false,"5130":true,"5296":false,"6171":true,"6357":true,"6359":true,"6609":true,"6638":false}},"cookies":{"1":{}},"gpc":1,"consent_type":2}; kndctr_F6171253512D2B8C0A490D45_AdobeOrg_identity=CiYyMjc5NjAzMjcwMzE4MjcyNjA3MTUxMjM3MTEyNTcyNjM0NjE4NFIRCKSl6pSwMRgBKgRTR1AzMAGgAeDRsPq6MagB7%2Dr2vuuQuqZJsAEG8AHq6uPSuzE%3D; LOSAD=1; p3094257258_done=1; p3094257258_done=1; _page_type_=Single%20Model%20PDP; kndctr_F6171253512D2B8C0A490D45_AdobeOrg_cluster=sgp3; s_inv=4580; s_vnc365=1731219983511%26vn%3D18; s_ivc=true; QuantumMetricSessionID=96fc47dbc94f9305c1775d35b71d9d4e; bm_mi=EB868BF2C19A71704F05AFDD4F45A7B0~YAAQz+NH0gqJqKaLAQAAYiEQvRXR9NUAWZ6Q1RxUFtzKMfb81S4y8hkfqekIXJXr02Ge/zPEQl8hrRCZxzEWyxK6FYMH64hllEr6gF5G40GPox5Ajs0G/gX+gk26YGsyVzCYJRPbXGgCi04WeuW6tvpLXV4zsQcKRYZn5cyjVbfzMGV4BCPp5RuDGA/V0IXErP6OMRMLgXlklMSH27CW/bvCehz2cyL+u0saG/sfALiGiJ/Xoku22OHH3oqYifjLMKtrcLArb+2l4Fp7N9c2PVFnkU3wL2aonfS3GGoIhILj2L/jot0kgyLkKOBZtu7DcyHuR7NESJG/yKyMjnmNLPDPeILw8ow1Md+ZDM88RR9OC5bpyCKk092B0wDrSoQOerxrAfOi5tIdMOaP0F6H7gH5hu2PeIllskQ0aUENqJf+WTX6HBWuKGBSfLIB1t0b~1; ak_bmsc=DC14E4D15661434ED05E97878E609BE5~000000000000000000000000000000~YAAQz+NH0tuJqKaLAQAAgicQvRWWDRyYiMu/Fisxozj5i7nR9QbgjE0Pec1cCeaXwBGgUjQmy+gyVCwzQHRZxqLzk+cISswvCYRBL8dISdJ0aUyRsCUHMP+ipe7s81LPczlvvn4lMenHqchuv36bsLd9XQHRG4tiROX521QK2TPquSjoHlRlEPVkkFfhQDO8W+pLel8N+abIPgEKodeyyIW8Sqr1SaMhI4Nq53PAVVAzdqfLPfbxLQLobNKO5lbHJ11luFqa+oVRqRyfa3YVSKFkj2tFcRTVNyD+dcQAx+HmipnqMRjp2eQTlg15g/34zraFqxjPEK3p4AX6XB6NgmKjRch+jDBzZc3uwAAG2IWcr7lTmSt+T+48rtw2QUvvJeON1Heu5hDjQwIgRkvPnZF565hx0MeN1BBD0q62UJFy734j3m8l9+d/jGhLRIkimV6yUktr1N00tzDny6x7Hkl9zFlOaa1+bGLeQY7fTo5hsZSjxMdMGUNukyUt8BGNcgKLmAxRzMLypEQEVKVEMgu4dVhc9OnTpzafkr0aOUjEsFr1bl4r5zOH0YVoQCJV/ZvxuM9Q2+NyKtpY/dXtffjAfjWFniYL3zRsxhreIcevfOCfuzaKHXd7gbD20cy527JwZ8N3mvRS5x++xePKwE7RLQ==; recentlypns=90UX0004US%2C90V7003HUS%2CF0GH00PBUS%2CF0EU00MAUS%2C90VJ000EUS%2C90SM00C5US; fusionEXPID=flash_na_app_qpl_MLR_Flash_NER; s_eVar57=s.products_evar; s_eng_rfd=12.12; AKA_A2=A; _abck=540660EA9576B22ADDEF089463DBB37F~0~YAAQzONH0mzX/K6LAQAAKLxLvQqLxhxYmAUJXu6SytpfaJyyNthvOs7eJl7s51eAflV5WrG67dzAPGxwlsEH0XgheiRXcDoCEsRzbt+0GLS1K+PyzEnueJVL80svaF/DN04MfBBQkqYzhTMqRjTfOCjwHlRv7US5F2MAli9iJAxTDG5rhXSONekSnhgVLUoaa7I+FdIJSNHV0VVA6KOuPVI5lf08BCSRlpsewJ9f+6/1/aSK50HDDwntWAGBJPMYNUmPC4BgI1BiQfOrYJiAhs03XiA2FXmyDO1Cf9W7GO+EzsHmTS/ZXupydWR1sDVTTWJC553t7MXn3VnnTMuPGoqKDsnlXXc1l8Gw4vEVcupmlcX92ehxvWCE0Hn50NLxcQwrYBV7pSZ/xNhr9/7suuET3CqPqGP+~-1~-1~1699691479; s_dur=1699687939130; bc_invalidateUrlCache_targeting=1699687940976; fusionQueryId=bt8y1Pbzwt; bm_sz=91322B11B187BB341CFD60D14829BD09~YAAQzONH0sR6/a6LAQAAEXVSvRXXXcKS8u2cRofODfxYyZ0eyVwHSDinVsSHM67qcCOrrTq0i6wGL7NGVXCmpqw8EA09sw+psYT1P+tFp29KlgLg1XtcuPFm+SVYH/uJjMzk1SjYgWGQyaj3IUIiCofZeahyH+8XbPYSLtNOlps0feoBmbu6VzSDApRcRA87E0QOxR0S+4JnKNhiVLvwC994LzpN2HFnptfxB71xB7I2mmoGQemCRSnrUEug9HOfWPxfUelo+R90/0Crw4Xy82xLI6uf6yXa9XGU3c5I/otFqNu9ubVdMd/rEfB/V5LK7cU7UcFYRHf95+8=~3487793~3294008; s_tslv=1699688394620; s_tot_rfd=0.91; _ga_LXNLK45HZF=GS1.1.1699683982.19.1.1699688395.0.0.0; _ga_1RPSEV71KD=GS1.1.1699683982.15.1.1699688395.60.0.0; ki_t=1696555788502%3B1699683986706%3B1699688395656%3B8%3B155; mp_lenovo_us_mixpanel=%7B%22distinct_id%22%3A%20%2218b029ad5ce1b8-0872ace045a4a8-18525634-13c680-18b029ad5d535%22%2C%22bc_persist_updated%22%3A%201696555783639%7D; _ga_X0H82YEL7G=GS1.1.1699683982.15.1.1699688395.60.0.0; inside-us3=218290524-1731bf7cf3f5fc6879fd48c675d59188f8407b850772e0f9b48518d68faa898b-0-0; exitsurveynotdisplayed=Page%20count%20not%20met; RT="z=1&dm=lenovo.com&si=a29aea7b-13e3-4d20-ae35-c5c617791161&ss=lotqb8z0&sl=5&tt=cqn&bcn=%2F%2F684d0d47.akstat.io%2F&ld=9ucc&ul=9y77&hd=9yc3"; akavpau_WaitingRoomController=1699688708~id=6b8e1423783b8921e58e3c7f473e425b; bm_sv=BB9422D2F2F866366D19CF4F4932BA8B~YAAQzONH0iWG/a6LAQAAI+ZSvRVD6CFZ4m6Uo/FbmAeEs5xc75gFf974VaQs4DOx86aW7yyI/L7N7Sunr9qDTOLrPed5TaL0GNz0XPgdLWnDbz4Xm698xgFS35KhS135WbYHswaNLTGo5POTPM38ejHeQ4h1beYY6FEYzqNIVDF/ztkGTv+4RP/wwsVsRQBCMHzuiXj3GpVpGMIB915Z8BvEFxPpN1aN6nlZRk7A29WSkideZPvyeW2A4sKWT7jm9ngifDnUhbP+~1',
    # #     'Upgrade-Insecure-Requests': '1'
    # # }
    
    # burp0_headers = {"Sec-Ch-Ua": "\"Chromium\";v=\"127\", \"Not)A;Brand\";v=\"99\"", "Sec-Ch-Ua-Mobile": "?0", "Sec-Ch-Ua-Platform": "\"Windows\"", "Accept-Language": "zh-TW", "Upgrade-Insecure-Requests": "1", "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.6533.100 Safari/537.36", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7", "Sec-Fetch-Site": "none", "Sec-Fetch-Mode": "navigate", "Sec-Fetch-User": "?1", "Sec-Fetch-Dest": "document", "Accept-Encoding": "gzip, deflate, br", "Priority": "u=0, i", "Connection": "keep-alive"}

    # response = requests.request("GET", url,headers=burp0_headers)

    # print(page_number)


    # soup = BeautifulSoup(response.text, 'html.parser')
    # # print(soup)
    
    # # len(soup.select('.part_number'))
    
    # web_url_soup = soup.select('.product_item>.product_name>a')
    # product_name_soup = soup.select('.product_item>.product_name')
    # product_code_soup = soup.select('.product_item>.product_name>a')
    
    # web_url_list = [i.get('href') for i in web_url_soup]
    # product_name_list = [i.text for i in product_name_soup]
    # product_code_list = [i.get('data-productcode') for i in product_code_soup]
    
    product_number = len(web_url_list)
    print(len(product_name_list))
    
    return web_url_list,product_name_list,product_code_list,product_number


# 儲存json檔案
def save_json(data, filepath):
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
# web_url = hp_lap.web_url_list[0]

# 建立資料夾
def create_directory(path):
    if not os.path.exists(path):
        os.makedirs(path)
        

# 獲取更多資訊
# web_url = hp_lap.web_url_list[0]
def get_product_info_more(product_code,file_name,n):
    

    url = f"https://openapi.lenovo.com/us/en/online/product/getTechSpecs?productNumber={product_code}"

    payload = {}
    headers = {
    'Origin': 'https://www.lenovo.com',
    'Referer': 'https://www.lenovo.com/us/en/p/laptops/thinkpad/thinkpadl/l13-gen-2-(13-inch-amd)/21abs02s00',
    'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    print(product_code)
    
    json_data = json.loads(response.text)
    # product_json = json_data['data']['tables'][0]['specs']
    
    create_directory(f'data/lenovo/{file_name}_content_more/')
    save_json(json_data,f'data/lenovo/{file_name}_content_more/{n}.json')
    return json_data


# 獲取商品資訊
def get_product_info(product_code,file_name,n):
    

    url = f"https://openapi.lenovo.com/us/en/product/singleModelPDP/get?groupCodes=1000001&productNumber={product_code}"

    payload = {}
    headers = {
    'Origin': 'https://www.lenovo.com',
    'Referer': 'https://www.lenovo.com/us/en/p/laptops/thinkpad/thinkpadl/l13-gen-2-(13-inch-amd)/21abs02s00',
    'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    print(product_code)
    
    json_data = json.loads(response.text)
    # product_json = json_data['data']['classification'][0]['specs']
    
    create_directory(f'data/lenovo/{file_name}_content/')
    save_json(json_data,f'data/lenovo/{file_name}_content/{n}.json')
    return json_data

# 獲取商品價格
def get_product_price(product_code,file_name,n):

    url = f"https://openapi.lenovo.com/us/en/detail/price/batch/get?preSelect=1&mcode={product_code}&configId=&enteredCode="

    payload = {}
    headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
    'Referer': 'https://www.lenovo.com/us/en/search',
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    print(response.text)

    
    json_data = json.loads(response.text)
    
    try:
        price = json_data['data'][product_code][4]
    except:
        response = requests.request("GET", url, headers=headers, data=payload)
        json_data = json.loads(response.text)
        price = json_data['data'][product_code][4]
    
    price_json = {'price':price}
    
    create_directory(f'data/lenovo/{file_name}_price/')
    save_json(price_json,f'data/lenovo/{file_name}_price/{n}.json')
    return price_json



# 檢查檔案是否存在
def check_is_crawl(file_path,file_name):
    if os.path.isfile(file_path):
        return True
    else:
        return False
# 檢查路徑是否存在
def check_is_crawl_path(file_path,file_name):
    if os.path.exists(file_path):
        return True
    else:
        return False

# 排序
def sort_key(file):
    # Extract the number from the filename
    number = int(re.search(r'\d+', file).group())
    return number

# 讀取json檔案
def read_json(file_path):
    # Get a list of all JSON files in the directory
    json_files = sorted(glob.glob(f'{file_path}/*.json'), key=sort_key)


    # Initialize an empty list to store the data
    data = []

    # Loop over all files and read them into a Python object
    for file in json_files:
        with open(file, 'r', encoding='utf-8') as f:
            data.append(json.load(f))
            
    return data


class lenovo_crawl():
    def __init__(self,keyword ,**kwargs):
        self.keyword = keyword
        self.file_name = f"{self.keyword}"
        
        self.product_list = None
        self.is_crawl_web_url = check_is_crawl(f'data/lenovo/{self.file_name}/{self.file_name}_.json',self.file_name)
        self.is_crawl_content = check_is_crawl_path(f'data/lenovo/{self.file_name}_content/',self.file_name)
        
        if self.is_crawl_web_url:
            self.page_info = self.get_page_info()
            self.web_url_list = self.get_web_url_list()
            self.product_name = self.get_product_name()
            self.product_code = self.get_product_code()
            self.total_rows = self.get_total_rows()
            self.all_product_data = None
            self.all_product_price = None
            self.all_product_data_more = None
        elif self.is_crawl_content:
            self.all_product_data = self.get_all_product_data()
            self.all_product_data_more = self.get_all_product_data_more()
            self.all_product_price = self.get_product_price()
        else:
            self.page_info = None
            self.web_url_list = None
            self.product_price = None
            self.product_name = None
            self.product_code = None
            self.total_rows =None
            self.all_product_data = None
            self.all_product_price = None
            self.all_product_data_more = None
    # 讀取product_data
    def get_all_product_data(self):
        if self.is_crawl_content:
            self.all_product_data = read_json(f'data/lenovo/{self.file_name}_content/')
            return self.all_product_data
        else:
            pass
    # 讀取product_data_more
    def get_all_product_data_more(self):
        if self.is_crawl_content:
            self.all_product_data = read_json(f'data/lenovo/{self.file_name}_content_more/')
            return self.all_product_data
        else:
            pass
    # 讀取web_url
    def get_web_url_list(self):
        if self.is_crawl_web_url:
            with open(f'data/lenovo/{self.file_name}/{self.file_name}_.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
        
            self.web_url_list = data['web_url']
            return data['web_url']
        else:
            pass
    # 讀取product_code
    def get_product_code(self):
        if self.is_crawl_web_url:
            with open(f'data/lenovo/{self.file_name}/{self.file_name}_.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
        
            self.product_code = data['product_code']
            return data['product_code']
        else:
            pass
    # 讀取page_info
    def get_page_info(self):
        if self.is_crawl_web_url:
            with open(f'data/lenovo/{self.file_name}/{self.file_name}_.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
                
            self.page_info = data
            return data
        else:
            pass
    # 讀取total_rows
    def get_total_rows(self):
        if self.is_crawl_web_url:
            with open(f'data/lenovo/{self.file_name}/{self.file_name}_.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
                
            self.total_rows = len(data['web_url'])
            return len(data['web_url'])
        else:
            pass
    # 讀取product_name
    def get_product_name(self):
        if self.is_crawl_web_url:
            with open(f'data/lenovo/{self.file_name}/{self.file_name}_.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
                
            self.product_name = data['product_name']
            return data['product_name']
        else:
            pass

    # 讀取product_price
    def get_prodct_price(self):
        if self.is_crawl_web_url:
            with open(f'data/lenovo/{self.file_name}/{self.file_name}_.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
                
            self.product_price = data['price']
            return data['price']
        else:
            pass



    # 讀取資料
    def load_data(self):
        self.web_url_list = self.get_web_url_list()
        self.product_price = self.get_prodct_price()
        self.product_name = self.get_product_name()
        
        
    # 獲取web_url
    def get_web_url(self,**kwargs):
        if self.is_crawl_web_url:
            pass
        else:
            create_directory(f'data/lenovo/{self.file_name}/')
            
            web_url_list =[]
            product_name_list = []
            product_code_list = []
            page_number = 1
            temp_number = 1
            part_web_url_list,part_product_name_list,part_product_code_list,product_number = get_page_json(page_number=page_number,keyword=self.keyword)

            while product_number !=0 or temp_number!=0:
                if product_number ==0:
                    temp_number=0
                part_web_url_list,part_product_name_list,part_product_code_list,product_number = get_page_json(page_number=page_number,keyword=self.keyword)
                web_url_list.extend(part_web_url_list)
                product_name_list.extend(part_product_name_list)
                product_code_list.extend(part_product_code_list)
                
                page_number +=1
                
            self.web_url_list = web_url_list
            self.product_name = product_name_list
            self.product_code = product_code_list
            self.total_rows = len(web_url_list)
            print(self.total_rows )
            
            # Combine the lists into a dictionary
            combined_dict = { 'product_name':product_name_list,'web_url': web_url_list, 'product_code': product_code_list} 
            self.page_info = combined_dict
            save_json(combined_dict, f'data/lenovo/{self.file_name}/{self.file_name}_.json')
            # self.is_crawl = True
            self.is_crawl_web_url = True
            
    def get_web_url_thinsta(self,**kwargs):
        if self.is_crawl_web_url:
            pass
        else:
            create_directory(f'data/lenovo/{self.file_name}/')
            
            web_url_list =[]
            product_name_list = []
            product_code_list = []
            page_number = 1
            temp_number = 1
            part_web_url_list,part_product_name_list,part_product_code_list,product_number = get_page_json_thinksta(page_number=page_number,keyword=self.keyword)

            while product_number !=0 or temp_number!=0:
                if product_number ==0:
                    temp_number=0
                part_web_url_list,part_product_name_list,part_product_code_list,product_number = get_page_json_thinksta(page_number=page_number,keyword=self.keyword)
                web_url_list.extend(part_web_url_list)
                product_name_list.extend(part_product_name_list)
                product_code_list.extend(part_product_code_list)
                
                page_number +=1
                
            self.web_url_list = web_url_list
            self.product_name = product_name_list
            self.product_code = product_code_list
            self.total_rows = len(web_url_list)
            print(self.total_rows )
            
            # Combine the lists into a dictionary
            combined_dict = { 'product_name':product_name_list,'web_url': web_url_list, 'product_code': product_code_list} 
            self.page_info = combined_dict
            save_json(combined_dict, f'data/lenovo/{self.file_name}/{self.file_name}_.json')
            # self.is_crawl = True
            self.is_crawl_web_url = True
            
    # 獲取資料
    def get_data_normal(self):
        if self.is_crawl_content:
            pass
        else:
            product_code = self.product_code
            all_product_data = [get_product_info(i,self.file_name,n) for n,i in enumerate(product_code)]
            all_product_data_more = [get_product_info_more(i,self.file_name,n) for n,i in enumerate(product_code)]
            all_product_data_price = [get_product_price(i,self.file_name,n) for n,i in enumerate(product_code)]
            self.all_product_data  =all_product_data
            self.all_product_data_more = all_product_data_more
            self.all_product_price = all_product_data_price
            self.is_crawl_content = True
            # all_product_data_spec = [i['data']['page']['pageComponents']['pdpTechSpecs']['technical_specifications'] for i in all_product_data]

    # 清理資料
    def clean(self):
        if self.is_crawl_content:
            self.all_product_data = read_json(f'data/lenovo/{self.file_name}_content/')
            self.all_product_data_more = read_json(f'data/lenovo/{self.file_name}_content_more/')
            self.all_product_price = read_json(f'data/lenovo/{self.file_name}_price/')
        all_product_data = []
        for i in self.all_product_data:
            try:
                new_dict = {}
                for n in i['data']['classification'][0]['specs'] :
                    new_dict.update({n['a']:n['b']})
                all_product_data.append(new_dict)
            except:
                all_product_data.append({})
        
        all_product_data_more = []
        for i in self.all_product_data_more:
            try:
                new_dict = {}
                for n in i['data']['tables'] :
                    temp_headline = ''
                    for a in n['specs']:
                        if temp_headline == a['headline']:
                            new_dict.update({f'{a["headline"]}1':a['text']})
                        else:
                            new_dict.update({a['headline']:a['text']})
                        temp_headline = a['headline']
                        
                all_product_data_more.append(new_dict)
            except:
                all_product_data_more.append({})
                
        all_product_price = self.all_product_price

        self.data_list = list(zip(self.product_name,self.web_url_list,all_product_price,all_product_data,all_product_data_more))
        save_json(self.data_list,f'data/lenovo/{self.file_name}_product.json')
        
        
def desktop_detail():
    with open('data/lenovo/Desktops_product.json', 'r', encoding='utf-8') as f:
        data_1 = json.load(f)
    with open('data/lenovo/thinkstation_product.json', 'r', encoding='utf-8') as f:
        data_2 = json.load(f)
        
    data = data_1 + data_2
    
    data_list =[]
    product_name = [{'Model Name':i[0]} for i in data]
    web_url = [{'Web Link':i[1]} for i in data]
    price = [{'Official Price':i[2]} for i in data]
    feature = [i[3] for i in data]
    dimension, port, weight = [],[],[]
    
    def clean_html(html_string):
        soup = BeautifulSoup(html_string, 'html.parser')
        return soup.get_text(separator='\n').strip()
    
    for i in data:
        try:
            dimension.append({'Dimensions (H x W x D)':clean_html(i[4]['Dimensions (H x W x D)'])})
        except:
            dimension.append({'Dimensions (H x W x D)':''})
        try:
            port.append({'Ports/Slots':clean_html(i[4]['Ports/Slots'])})
        except:
            port.append({'Ports/Slots':''})
        try:
            weight.append({'Weight':clean_html(i[4]['Weight'])})
        except:
            weight.append({'Weight':''})
    for i,data_ in enumerate(data):
        data_list.append({**product_name[i],**web_url[i],**price[i],**feature[i],**dimension[i],**port[i],**weight[i]})



    df = pd.DataFrame(data_list)
    df['Type'] = df['Model Name'].apply(lambda x: 'Chrome' if 'chrome' in x.lower() else 'Workstation' if 'workstation' in x.lower() else 'Gaming' if 'omen' in x.lower() or 'victus' in x.lower() else 'Commercial' if 'thin client' in x.lower() or 'pro' in x.lower() or 'elite' in x.lower() or 't550' in x.lower() else 'Consumer' if 'pavilion' in x.lower() or 'envy' in x.lower() else 'None Type_DT')
    
    
    df["Ports/Slots"] = df["Ports/Slots"].fillna("")
    df["Ports"] = df["Ports"].fillna("")
    df["Ports & Slots"] = df["Ports/Slots"] + "\n" + df["Ports"]
    
    df['Graphics Card'] = df['Graphic Card']
    
    df['Hard Drive'] = df['Storage']
    
    df['Operating System'] = df['Operating System']
    
    df['Audio and Speakers'] = None
    
    df['Power Supply'] = df['AC Adapter / Power Supply'].apply(lambda x: x if pd.notna(x) else None)
    # Function to convert inches to centimeters
    def inches_to_cm(inches):
        return round(inches * 2.54, 2)

    # Function to extract and convert dimensions
    def convert_dimensions(dimensions):
        # dimensions = df["Dimensions (H x W x D)"][2]
        if dimensions!='':
            match = re.search(r"(\d+\.?\d*)mm x (\d+\.?\d*)mm x (\d+\.?\d*)mm", dimensions)
            
            if match:
                height_mm = float(match.group(1))
                width_mm = float(match.group(2))
                depth_mm = float(match.group(3))
                    
                        
                    
                return height_mm, width_mm, depth_mm
            else:
                return '', '', ''
                
        else:
            return '', '', ''
    df["Dimensions (H x W x D)"].fillna("", inplace=True)
    df[["Height(mm)", "Width(mm)", "Depth(mm)"]] = df["Dimensions (H x W x D)"].apply(convert_dimensions).apply(pd.Series)
    
    def extract_and_convert_to_kg(weight_str):
        if pd.notna(weight_str):
        
            match = re.search(r"(\d+(\.\d+)?)\s*kg", weight_str)
            if match:
                weight_lb = float(match.group(1))
                weight_kg = round(weight_lb, 2)
                return weight_kg
            return None
        return None

    df["Weight"].fillna("", inplace=True)
    df["Weight(kg)"] = df["Weight"].apply(extract_and_convert_to_kg)
    
    df['Brand'] = "Lenovo"
    
    df['Model Name'] = df['Model Name']
    
    

    columns_to_output = [
            "Type",
            "Brand",
            "Model Name",
            "Official Price",
            "Ports & Slots",
            "Display",
            "Processor",
            "Graphics Card",
            "Hard Drive",
            "Memory",
            "Operating System",
            "Audio and Speakers",
            "Height(mm)",
            "Width(mm)",
            "Depth(mm)",
            "Weight(kg)",
            "Power Supply",
            "Web Link",
        ]
    df[columns_to_output].to_csv(
        f"./data/lenovo/desktop.csv", encoding="utf-8-sig", index=False
    )
def laptop_detail():

    with open('data/lenovo/Laptops_product.json', 'r', encoding='utf-8') as f:
        data_1 = json.load(f)
        
    data = data_1 
    
    data_list =[]
    product_name = [{'Model Name':i[0]} for i in data]
    web_url = [{'Web Link':i[1]} for i in data]
    price = [{'Official Price':i[2]} for i in data]
    feature = [i[3] for i in data]
    dimension, port, weight,audio,Camera,battery = [],[],[],[],[],[]
    other_list = [str(i[4]) for i in data]
    
    def clean_html(html_string):
        if not html_string:
            return ''
        # html_string = "<span style=""white-space:nowrap;"">Windows 11</span> Home</br> Lenovo recommends Windows 11 Pro for business."
        # Parse HTML content
        soup = BeautifulSoup(html_string, 'html.parser')
        # Extract text and clean up
        text = soup.get_text(separator='\n').strip()
        # Remove any remaining HTML tags and excessive whitespace
        clean_text = re.sub(r'<[^>]+>', '', text)
        clean_text = re.sub(r'\s+', ' ', clean_text)
        return clean_text
    
    for i in data:
        try:
            # Find any key containing 'dimensions' (case-insensitive)
            dimension_key = next((key for key in i[4].keys() if 'dimensions' in key.lower()), None)
            if dimension_key:
                dimension.append({'Dimensions (H x W x D)': clean_html(i[4][dimension_key])})
            else:
                dimension.append({'Dimensions (H x W x D)': ''})
        except:
            dimension.append({'Dimensions (H x W x D)':''})
        try:
            port.append({'Ports/Slots':clean_html(i[4]['Ports/Slots'])})
        except:
            port.append({'Ports/Slots':''})
        try:
            weight.append({'Weight':clean_html(i[4]['Weight'])})
        except:
            weight.append({'Weight':''})
        try:
            audio.append({'Audio and Speakers':clean_html(i[4]['Audio and Speakers'])})
        except:
            audio.append({'Audio and Speakers':''})
        try:
            Camera.append({'Camera':clean_html(i[4]['Camera'])})
        except:
            Camera.append({'Camera':''})
        try:
            battery.append({'Primary Battery':clean_html(i[4]['Primary Battery'])})
        except:
            battery.append({'Primary Battery':''})
            
    for i,data_ in enumerate(data):
        data_list.append({**product_name[i],**web_url[i],**price[i],**feature[i],**dimension[i],**port[i],**weight[i],**audio[i],**Camera[i]})



    df = pd.DataFrame(data_list)
    df['Type'] = df['Model Name'].apply(lambda x: 'Chrome' if 'chrome' in x.lower() else 'Workstation' if 'workstation' in x.lower() else 'Gaming' if 'omen' in x.lower() or 'victus' in x.lower() else 'Commercial' if 'thin client' in x.lower() or 'pro' in x.lower() or 'elite' in x.lower() or 't550' in x.lower() else 'Consumer' if 'pavilion' in x.lower() or 'envy' in x.lower() else 'None Type_DT')
    
    
    df["Ports/Slots"] = df["Ports/Slots"].fillna("")
    df["Ports"] = df["Ports"].fillna("")
    df["Ports & Slots"] = df["Ports/Slots"] + "\n" + df["Ports"]
    
    df['Graphics Card'] = df['Graphic Card']
    
    df['Hard Drive'] = df['Storage']
    
    df['Operating System'] = df['Operating System']
    
    df['Audio and Speakers'] = df['Audio and Speakers']
    
    df['Power Supply'] = df['AC Adapter / Power Supply'].apply(lambda x: x if pd.notna(x) else None)
    
    df['Primary Battery'] = df['Battery']
    
    # Function to convert inches to centimeters
    def inches_to_cm(inches):
        return round(inches * 2.54, 2)

    # Function to extract and convert dimensions
    def convert_dimensions(dimensions):
        # dimensions = df["Dimensions (H x W x D)"][2]

        dimensions = str(dimensions).strip()

        # 正则表达式
        if dimensions:
            # 匹配每个数值支持范围和单位
            match = re.search(
                r"(?:[^\d]*?)(\d+\.?\d*)(?:-\d+\.?\d*)?\s*(?:mm)?\s*x\s*"
                r"(?:[^\d]*?)(\d+\.?\d*)(?:-\d+\.?\d*)?\s*(?:mm)?\s*x\s*"
                r"(?:[^\d]*?)(\d+\.?\d*)(?:-\d+\.?\d*)?\s*(?:mm)?",
                dimensions,
                re.IGNORECASE
            )
            if match:
            # 提取维度数值
                height_mm = float(match.group(1)) if match.group(1) else None
                width_mm = float(match.group(2)) if match.group(2) else None
                depth_mm = float(match.group(3)) if match.group(3) else None
                return height_mm, width_mm, depth_mm
        # 无法匹配返回空值
        return None, None, None

    df["Dimensions (H x W x D)"].fillna("", inplace=True)
    
    df[["Height(mm)", "Width(mm)", "Depth(mm)"]] = df["Dimensions (H x W x D)"].apply(convert_dimensions).apply(pd.Series)
    
    # df_1 = df[["Dimensions (H x W x D)","Height(mm)","Width(mm)","Depth(mm)",'Web Link']]
    
    def extract_and_convert_to_kg(weight_str):
        if pd.notna(weight_str):
        
            match = re.search(r"(\d+(\.\d+)?)\s*kg", weight_str)
            if match:
                weight_lb = float(match.group(1))
                weight_kg = round(weight_lb, 2)
                return weight_kg
            return None
        return None

    df["Weight"].fillna("", inplace=True)
    df["Weight(kg)"] = df["Weight"].apply(extract_and_convert_to_kg)
    
    df['Brand'] = "Lenovo"
    
    df['Model Name'] = df['Model Name']
    
    
    df['NFC'] = None
    df['FPR_model'] = None
    for index,i in enumerate(other_list):
        # index = 0
        # i = disclaim_list[index]
        
        if '4G' in i:
            # print(index)
            df.loc[index,'WWAN'] = '4G'
        elif '5G' in i:
            df.loc[index,'WWAN'] = '5G'
            
        if 'NFC' in i:
            df.loc[index,'NFC'] = 'Yes'
            
        if 'Fingerprint' in i:
            df.loc[index,'FPR'] = 'Yes'
            

    
    
    

    columns_to_output = [
        "Type",
        "Brand",
        "Model Name",
        "Official Price",
        "Ports & Slots",
        "Camera",
        "Display",
        "Primary Battery",
        "Processor",
        "Graphics Card",
        "Hard Drive",
        "Memory",
        "Operating System",
        "Audio and Speakers",
        "Height(mm)",
        "Width(mm)",
        "Depth(mm)",
        "Weight(kg)",
        "WWAN",
        "NFC",
        "FPR_model",
        "FPR",
        "Power Supply",
        "Web Link",
    ]
    for column in columns_to_output:
        df[column] = df[column].apply(lambda x: clean_html(str(x)))
    
    df[columns_to_output].to_csv(
        f"./data/lenovo/laptop.csv", encoding="utf-8-sig", index=False
    )
def docking_detail():
    with open('data/lenovo/Docking_product.json', 'r', encoding='utf-8') as f:
        data_1 = json.load(f)
   
    data = data_1 
    
    data_list =[]
    product_name = [{'Model Name':i[0]} for i in data]
    web_url = [{'Web Link':i[1]} for i in data]
    price = [{'Official Price':i[2]} for i in data]
    feature = [i[3] for i in data]
    dimension, port, weight = [],[],[]
    
    def clean_html(html_string):
        soup = BeautifulSoup(html_string, 'html.parser')
        return soup.get_text(separator='\n').strip()
    
    for i in data:
        try:
            dimension.append({'Dimensions (H x W x D)':clean_html(i[4]['Dimensions (H x W x D)'])})
        except:
            dimension.append({'Dimensions (H x W x D)':''})
        try:
            port.append({'Ports/Slots':clean_html(i[4]['Ports/Slots'])})
        except:
            port.append({'Ports/Slots':''})
        try:
            weight.append({'Weight':clean_html(i[4]['Weight'])})
        except:
            weight.append({'Weight':''})
    for i,data_ in enumerate(data):
        data_list.append({**product_name[i],**web_url[i],**price[i],**feature[i],**dimension[i],**port[i],**weight[i]})



    df = pd.DataFrame(data_list)
    df['Type'] = df['Model Name'].apply(lambda x: 'Chrome' if 'chrome' in x.lower() else 'Workstation' if 'workstation' in x.lower() else 'Gaming' if 'omen' in x.lower() or 'victus' in x.lower() else 'Commercial' if 'thin client' in x.lower() or 'pro' in x.lower() or 'elite' in x.lower() or 't550' in x.lower() else 'Consumer' if 'pavilion' in x.lower() or 'envy' in x.lower() else 'None Type_DT')
    
    
    df["Charging Port"] = df["Charging Port"].fillna("")
    df['Thunderbolt Port'] = df['Thunderbolt Port'].fillna("")
    df['USB Ports'] = df['USB Ports'].fillna("")
    df['Video Ports'] = df['Video Ports'].fillna("")
    df['Ethernet'] = df['Ethernet'].fillna("")
    
    df["Ports & Slots"] = df["Ports/Slots"] 
    
   

    df['Output Power'] = df['Output Power'].fillna("")
    df['Input Power'] = df['Input Power'].fillna("")

    df['Power Supply'] = df['Output Power'] + "\n" + df['Input Power']
    # Function to convert inches to centimeters
   
    def extract_and_convert_to_kg(weight_str):
        if pd.notna(weight_str):
        
            match = re.search(r"(\d+(\.\d+)?)\s*kg", weight_str)
            if match:
                weight_lb = float(match.group(1))
                weight_kg = round(weight_lb, 2)
                return weight_kg
            return None
        return None

    df["Weight"].fillna("", inplace=True)
    df["Weight(kg)"] = df["Weight"].apply(extract_and_convert_to_kg)
    
    df['Brand'] = "Lenovo"
    
    df['Model Name'] = df['Model Name']
    
    
    columns_to_output = [
        "Type",
        "Brand",
        "Model Name",
        "Official Price",
        "Ports & Slots",
        "Weight(kg)",
        "Power Supply",
        "Web Link",

    ]
    df[columns_to_output].to_csv(
        f"./data/lenovo/docking.csv", encoding="utf-8-sig", index=False
    )
    
    

# @timing_decorator
# def try_time():
        
lenovo_desktop = lenovo_crawl(keyword='Desktops')
lenovo_desktop.get_web_url()
lenovo_desktop.get_data_normal()
lenovo_desktop.clean()

lenovo_thinksta = lenovo_crawl(keyword='thinkstation')
lenovo_thinksta.get_web_url_thinsta()
lenovo_thinksta.get_data_normal()
lenovo_thinksta.clean()

desktop_detail()


lenovo_lap = lenovo_crawl(keyword='Laptops')
lenovo_lap.get_web_url()
lenovo_lap.get_data_normal()
lenovo_lap.clean()

laptop_detail()

lenovo_dock = lenovo_crawl(keyword='Docking')
lenovo_dock.get_web_url()
lenovo_dock.get_data_normal()
lenovo_dock.clean()

docking_detail()




# try_time()



