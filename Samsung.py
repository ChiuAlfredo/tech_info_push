import requests

from bs4 import BeautifulSoup
import json
import pandas as pd




def crawl_product(company, keyword):
    # burp0_url = "https://www.samsung.com:443/us/product-finder/shop/pf_search/s/?category_code=n0003068&taxonomy_code=n0003068&from=0&size=24&sort=featured"
    burp0_url = "https://www.samsung.com:443/us/product-finder/shop/pf_search/s/?category_code=n0003068&taxonomy_code=n0003068&from=0&size=24&sort=featured"
    burp0_cookies = {
        "s_fpid": "ca51c01d-5ee9-446d-8e2a-417c7c1ce864",
        "s_ecid": "MCMID%7C87417855217938127472167537113158430229",
        "AAMC_samsungelectronicsamericainc_0": "REGION%7C11",
        "aam_sc": "aamsc%3D4718718",
        "aam_uuid": "87457814995313514472169307816733127305",
        "_ga": "GA1.1.754102624.1719999038",
        "_gcl_au": "1.1.456890997.1719999042",
        "_fbp": "fb.1.1719999042694.603133754775108845",
        "__attentive_id": "759ce5410a6841909f6661476d2c54cd",
        "_attn_": "eyJ1Ijoie1wiY29cIjoxNzE5OTk5MDQzNDU0LFwidW9cIjoxNzE5OTk5MDQzNDU0LFwibWFcIjoyMTkwMCxcImluXCI6ZmFsc2UsXCJ2YWxcIjpcIjc1OWNlNTQxMGE2ODQxOTA5ZjY2NjE0NzZkMmM1NGNkXCJ9In0=",
        "__attentive_cco": "1719999043456",
        "mdLogger": "false",
        "kampyle_userid": "4761-c365-dda2-97ef-2d5b-d8a1-a8d4-36a7",
        "sa_did": "TpTIOzjXFYVNjKfDximQCUExfnkhRQFZ",
        "sa_773-397-549898": '{"US":{"status":"GRANTED","updated":"2024-07-03T09:30:44.077Z","clientId":"kv5di1wr19","deviceId":"TpTIOzjXFYVNjKfDximQCUExfnkhRQFZ"}}',
        "_aeaid": "85b707ca-7980-4559-bfab-12ef78f3aaf5",
        "aelastsite": "IqynIxmTpWLTmucVE6VJcc93GvEXZoAScAF4P8JKEh9cCxYtr%2FMAw5Qj62MwuOMg",
        "__idcontext": "eyJjb29raWVJRCI6IjJpakxUVXFPRFYzRlRTNVhtV3J5RERWaFdMRiIsImRldmljZUlEIjoiMmlqTFRYQTNKU0t3OTg0MWI1cTl0SnQ4MDRyIiwiaXYiOiIiLCJ2IjoiIn0%3D",
        "iadvize-6528-vuid": "aaea3f6dc7fe4601934c09788763232752a9f5bb7d2f4",
        "BVBRANDID": "0bd2e407-e2a2-4ddc-ae6a-da0ee66d51ba",
        "aam_test": "segs%3D7431031",
        "country_region": "CA-ON",
        "country_codes": "tw",
        "device_type": "pc",
        "__COM_SPEED": "H",
        "ecom_vi_USA": "TUNNSUQlN0M4NzQxNzg1NTIxNzkzODEyNzQ3MjE2NzUzNzExMzE1ODQzMDIyOQ==",
        "ecom_session_id_USA": "M2Y4NmIzNTQtODY4YS00NTJhLTkwZWYtMjI4NjkxM2FlNzMz",
        "TS011dc0a2": "016abffc7f79f3b3c1e5aa11c1854b3cb432edbb3f7540c440e758243b9f448c716e15797df9cc3a9eeafdb6f7c5313c3cabd6c596",
        "TS0171c81e": "016abffc7f79f3b3c1e5aa11c1854b3cb432edbb3f7540c440e758243b9f448c716e15797df9cc3a9eeafdb6f7c5313c3cabd6c596",
        "at_check": "true",
        "AMCVS_48855C6655783A647F000101%40AdobeOrg": "1",
        "AMCV_48855C6655783A647F000101%40AdobeOrg": "1585540135%7CMCIDTS%7C19922%7CMCMID%7C87417855217938127472167537113158430229%7CMCAID%7CNONE%7CMCOPTOUT-1721194309s%7CNONE%7CMCAAMLH-1721791909%7C11%7CMCAAMB-1721791909%7Cj8Odv6LonN4r3an7LhD3WZrU1bUpAkFkkiY1ncBR96t2PTI%7CvVersion%7C4.4.0%7CMCCIDH%7C617300242",
        "DATradein": "true",
        "platform": "windows",
        "aelreadersettings": "%7B%22c_big%22%3A0%2C%22rg%22%3A0%2C%22memph%22%3A0%2C%22contrast_setting%22%3A0%2C%22colorshift_setting%22%3A0%2C%22text_size_setting%22%3A0%2C%22space_setting%22%3A0%2C%22font_setting%22%3A0%2C%22k%22%3A0%2C%22k_disable_default%22%3A0%2C%22hlt%22%3A0%2C%22disable_animations%22%3A0%2C%22display_alt_desc%22%3A0%7D",
        "AKA_A2": "A",
        "cookie_country": "us",
        "targetUrl": "https://www.samsung.com/us/support/account",
        "recentlyViewed": "[]",
        "AMP_VID": "87417855217938127472167537113158430229",
        "mboxEdgeCluster": "32",
        "OptanonConsent": "isGpcEnabled=0&datestamp=Wed+Jul+17+2024+12%3A34%3A28+GMT%2B0800+(%E5%8F%B0%E5%8C%97%E6%A8%99%E6%BA%96%E6%99%82%E9%96%93)&version=202307.1.0&browserGpcFlag=0&isIABGlobal=false&hosts=&consentId=6e84f1e6-7025-40cd-92e7-7815681c8f8e&interactionCount=1&landingPath=NotLandingPage&groups=C0001%3A1%2CC0003%3A1%2CC0002%3A1%2CBG17%3A1%2CC0004%3A1&AwaitingReconsent=false",
        "s_pers": "%201%3D1%7C1721192668692%3B%20first_page_visit%3Dhttps%253A%252F%252Fwww.samsung.com%252Fus%252Fcomputing%252Fgalaxy-books%252Fall-galaxy-books%252F%7C1721192668693%3B%20s_nr%3D1721190868693-Repeat%7C1723782868693%3B%20gpv_pn%3Dhttps%253A%252F%252Fwww.samsung.com%252Fus%252Fcomputing%252Fgalaxy-books%252Fall-galaxy-books%7C1721192668693%3B%20s_fbsr%3D1%7C1721192668694%3B",
        "da_sid": "7AD0997C8E38AE891F33AA13A4E8807F5C.0|4|0|3",
        "da_lid": "54092D7898F9EA120504BB99E623DC888D|0|0|0",
        "da_intState": "",
        "kampyleUserSession": "1721190876291",
        "kampyleUserSessionsCount": "4",
        "kampyleSessionPageCounter": "1",
        "tfpsi": "6a9aaa87-ff1d-4893-ae65-a92e091fe753",
        "_beu_utm_source": "__null__",
        "_beu_utm_medium": "__null__",
        "_beu_utm_campaign": "__null__",
        "_beu_utm_term": "__null__",
        "_beu_utm_content": "__null__",
        "_beu_cid": "__null__",
        "_samsungrtetSessId": "9QMN8KE",
        "_samsungrtetSessPageSeq": "0",
        "_uetsid": "1f914fc043ed11ef8084ad2219debf21",
        "_uetvid": "e8e16910391e11efb4bc1da188de5359",
        "__attentive_dv": "1",
        "__attentive_pv": "1",
        "__attentive_ss_referrer": "ORGANIC",
        "utag_main": "v_id:019077ee63e00006b857e634d6ed05073003106b009dcsamsung_live$_sn:3$_se:4$_ss:0$_st:1721192715196$tapid_reset:true%3Bexp-1751535034159$dc_visit:3$ses_id:1721190864174%3Bexp-session$_pn:1%3Bexp-session$dc_event:4%3Bexp-session$_prevpage:%3Bexp-1721194515201$adobe_mcid:87417855217938127472167537113158430229%3Bexp-session$aa_vid:%3Bexp-session$dc_region:ap-east-1%3Bexp-session",
        "s_sess": "%20c_m%3DundefinedTyped%252FBookmarkedTyped%252FBookmarkedundefined%3B%20s_ppvl%3Dhttps%25253A%252F%252Fwww.samsung.com%252Fus%252Fcomputing%252Fgalaxy-books%252Fgalaxy-book4-edge%252Fbuy%252Fgalaxy-book4-edge-14-qualcomm-snapdragon-x-elite-512gb-sapphire-blue-np940xma-kb1us%252C19%252C41%252C1550%252C807%252C738%252C1536%252C864%252C1.25%252CL%3B%20s_sq%3D%3B%20s_cc%3Dtrue%3B%20s_ppv%3Dhttps%25253A%252F%252Fwww.samsung.com%252Fus%252Fcomputing%252Fgalaxy-books%252Fall-galaxy-books%252C17%252C28%252C1213%252C807%252C738%252C1536%252C864%252C1.25%252CL%3B",
        "RT": '"z=1&dm=samsung.com&si=b47a61a0-913c-4cae-bef2-577b455043de&ss=lypclkm0&sl=0&tt=0&bcn=%2F%2F684d0d4a.akstat.io%2F&ld=28n8m&nu=10djg8u0g&cl=t1z&hd=1bw5"',
        "_ga_0JTZHYKZ5Z": "GS1.1.1721190869.3.1.1721190923.6.0.0",
        "mbox": "PC#33eb4a24a67a45f087aed19c4979daaf.32_0#1784435665|session#0860f7787d484834819168368b3b659a#1721192785",
    }
    burp0_headers = {
        "Sec-Ch-Ua": '"Not/A)Brand";v="8", "Chromium";v="126"',
        "Accept-Language": "zh-TW",
        "Sec-Ch-Ua-Mobile": "?0",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.6478.127 Safari/537.36",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Accept": "*/*",
        "X-Requested-With": "XMLHttpRequest",
        "Sec-Ch-Ua-Platform": '"Windows"',
        "Origin": "https://www.samsung.com",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": "https://www.samsung.com/us/computing/galaxy-books/all-galaxy-books/",
        "Accept-Encoding": "gzip, deflate, br",
        "Priority": "u=1, i",
    }
    burp0_data = {"origUrl": "L3VzL2NvbXB1dGluZy9nYWxheHktYm9va3MvYWxsLWdhbGF4eS1ib29rcw=="}
    response = requests.post(
        burp0_url, headers=burp0_headers, cookies=burp0_cookies, data=burp0_data
    )
    products_dict = json.loads(response.text)

    product_list = []
    for product in products_dict["products"]:
        product_dict = {}
        if product["haDeepLink"]:
            link = product["haDeepLink"]
        elif product["linkUrl"]:
            link = product["linkUrl"]
        product_dict["Web Link"] = "https://www.samsung.com" + link

        product_list.append(product_dict)


    product_spec_list = []
    for product in product_list:
        print(product)
        # product = product_list[0]
        # burp0_url = 'https://www.samsung.com/us/computing/galaxy-books/galaxy-book4-ultra/galaxy-book4-ultra-16-intel-core-ultra-9-1tb-moonstone-gray-np960xgl-xg1us/'
        burp0_url = product["Web Link"]

        burp0_cookies = {
            "s_fpid": "ca51c01d-5ee9-446d-8e2a-417c7c1ce864",
            "s_ecid": "MCMID%7C87417855217938127472167537113158430229",
            "AAMC_samsungelectronicsamericainc_0": "REGION%7C11",
            "aam_sc": "aamsc%3D4718718",
            "aam_uuid": "87457814995313514472169307816733127305",
            "_ga": "GA1.1.754102624.1719999038",
            "_gcl_au": "1.1.456890997.1719999042",
            "_fbp": "fb.1.1719999042694.603133754775108845",
            "__attentive_id": "759ce5410a6841909f6661476d2c54cd",
            "_attn_": "eyJ1Ijoie1wiY29cIjoxNzE5OTk5MDQzNDU0LFwidW9cIjoxNzE5OTk5MDQzNDU0LFwibWFcIjoyMTkwMCxcImluXCI6ZmFsc2UsXCJ2YWxcIjpcIjc1OWNlNTQxMGE2ODQxOTA5ZjY2NjE0NzZkMmM1NGNkXCJ9In0=",
            "__attentive_cco": "1719999043456",
            "mdLogger": "false",
            "kampyle_userid": "4761-c365-dda2-97ef-2d5b-d8a1-a8d4-36a7",
            "sa_did": "TpTIOzjXFYVNjKfDximQCUExfnkhRQFZ",
            "sa_773-397-549898": '{"US":{"status":"GRANTED","updated":"2024-07-03T09:30:44.077Z","clientId":"kv5di1wr19","deviceId":"TpTIOzjXFYVNjKfDximQCUExfnkhRQFZ"}}',
            "_aeaid": "85b707ca-7980-4559-bfab-12ef78f3aaf5",
            "aelastsite": "IqynIxmTpWLTmucVE6VJcc93GvEXZoAScAF4P8JKEh9cCxYtr%2FMAw5Qj62MwuOMg",
            "__idcontext": "eyJjb29raWVJRCI6IjJpakxUVXFPRFYzRlRTNVhtV3J5RERWaFdMRiIsImRldmljZUlEIjoiMmlqTFRYQTNKU0t3OTg0MWI1cTl0SnQ4MDRyIiwiaXYiOiIiLCJ2IjoiIn0%3D",
            "iadvize-6528-vuid": "aaea3f6dc7fe4601934c09788763232752a9f5bb7d2f4",
            "BVBRANDID": "0bd2e407-e2a2-4ddc-ae6a-da0ee66d51ba",
            "AMCV_48855C6655783A647F000101%40AdobeOrg": "1585540135%7CMCIDTS%7C19908%7CMCMID%7C87417855217938127472167537113158430229%7CMCAID%7CNONE%7CMCOPTOUT-1720007487s%7CNONE%7CMCAAMLH-1720605087%7C11%7CMCAAMB-1720605087%7Cj8Odv6LonN4r3an7LhD3WZrU1bUpAkFkkiY1ncBR96t2PTI%7CvVersion%7C4.4.0%7CMCCIDH%7C617300242",
            "mbox": "session#33eb4a24a67a45f087aed19c4979daaf#1720002149|PC#33eb4a24a67a45f087aed19c4979daaf.32_0#1783245088",
            "OptanonConsent": "isGpcEnabled=0&datestamp=Wed+Jul+03+2024+17%3A51%3A29+GMT%2B0800+(%E5%8F%B0%E5%8C%97%E6%A8%99%E6%BA%96%E6%99%82%E9%96%93)&version=202307.1.0&browserGpcFlag=0&isIABGlobal=false&hosts=&consentId=6e84f1e6-7025-40cd-92e7-7815681c8f8e&interactionCount=1&landingPath=NotLandingPage&groups=C0001%3A1%2CC0003%3A1%2CC0002%3A1%2CBG17%3A1%2CC0004%3A1&AwaitingReconsent=false",
            "s_pers": "%201%3D1%7C1720002090377%3B%20first_page_visit%3Dhttps%253A%252F%252Fwww.samsung.com%252Fus%252Fcomputing%252Fgalaxy-books%252Fgalaxy-book4-series%252Fbuy%252Fgalaxy-book4-360-15-6-intel-core-7-1tb-gray-np750qgk-kg1us%252F%7C1720002090378%3B%20s_nr%3D1720000290378-New%7C1722592290378%3B%20gpv_pn%3Dhttps%253A%252F%252Fwww.samsung.com%252Fus%252Fcomputing%252Fgalaxy-books%252Fgalaxy-book4-series%252Fbuy%252Fgalaxy-book4-360-15-6-intel-core-7-1tb-gray-np750qgk-kg1us%7C1720002090379%3B%20s_fbsr%3D1%7C1720002090381%3B",
            "aam_test": "segs%3D7431031",
            "da_lid": "54092D7898F9EA120504BB99E623DC888D|0|0|0",
            "kampyleUserSession": "1720000291781",
            "kampyleUserSessionsCount": "2",
            "kampyleSessionPageCounter": "1",
            "_uetvid": "e8e16910391e11efb4bc1da188de5359",
            "utag_main": "v_id:019077ee63e00006b857e634d6ed05073003106b009dcsamsung_live$_sn:1$_se:13$_ss:0$_st:1720002095891$ses_id:1719999030242%3Bexp-session$_pn:2%3Bexp-session$tapid_reset:true%3Bexp-1751535034159$dc_visit:1$dc_event:12%3Bexp-session$_prevpage:%3Bexp-1720003895898$adobe_mcid:87417855217938127472167537113158430229%3Bexp-session$aa_vid:%3Bexp-session$dc_region:ap-east-1%3Bexp-session",
            "_ga_0JTZHYKZ5Z": "GS1.1.1719999038.1.1.1720000536.60.0.0",
        }
        burp0_headers = {
            "Sec-Ch-Ua": '"Not/A)Brand";v="8", "Chromium";v="126"',
            "Sec-Ch-Ua-Mobile": "?0",
            "Sec-Ch-Ua-Platform": '"Windows"',
            "Accept-Language": "zh-TW",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.6478.127 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
            "Sec-Fetch-Site": "none",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-User": "?1",
            "Sec-Fetch-Dest": "document",
            "Accept-Encoding": "gzip, deflate, br",
            "Priority": "u=0, i",
            "Connection": "keep-alive",
        }
        response = requests.get(burp0_url, headers=burp0_headers, cookies=burp0_cookies)

        soup = BeautifulSoup(response.text, "html.parser")

        json_nex = soup.find("script", id="__NEXT_DATA__", type="application/json")
        data = json.loads(json_nex.text)

        # Extracting the specific part of the data
        extracted_data = data["props"]["pageProps"]

        # extracted_data["productData"]["products"]
        group_id = data["props"]["pageProps"]['groupId']
        
        
        

        # product_info = products[0]

        
        for product_info in extracted_data["productData"]["products"]:
            spec_dict = {}
            # product_info = extracted_data["productData"]["products"][0]
            spec_dict["model_code"] = product_info["modelCode"]
            spec_dict["price"] = product_info["currentPrice"]

            spec_dict["Model Name"] = product_info["productTitle"]

            spec_dict["Web Link"] = "https://www.samsung.com" + product_info["buySpaUrl"]

            for key, value in product_info["attributes"].items():
                spec_dict[key.lower()] = value
            
            if spec_dict not in product_spec_list:
                product_spec_list.append(spec_dict)
            

        burp0_url = f"https://www.samsung.com:443/us/api/v1/bridge/cacheable/bridge-data?data_type=Specs&store_type=B2C&group_id={group_id}&modelCode={spec_dict['model_code']}"
        burp0_headers = {
            "Sec-Ch-Ua": '"Not/A)Brand";v="8", "Chromium";v="126"',
            "Tracestate": "983838@nr=0-1-983838-1834968853-50cb96b2ff373c41----1721194364587",
            "Traceparent": "00-18894aa59ca55b39f4fd5b3a68c43df3-50cb96b2ff373c41-01",
            "Accept-Language": "zh-TW",
            "Sec-Ch-Ua-Mobile": "?0",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.6478.127 Safari/537.36",
            "Newrelic": "eyJ2IjpbMCwxXSwiZCI6eyJ0eSI6IkJyb3dzZXIiLCJhYyI6Ijk4MzgzOCIsImFwIjoiMTgzNDk2ODg1MyIsImlkIjoiNTBjYjk2YjJmZjM3M2M0MSIsInRyIjoiMTg4OTRhYTU5Y2E1NWIzOWY0ZmQ1YjNhNjhjNDNkZjMiLCJ0aSI6MTcyMTE5NDM2NDU4N319",
            "Sec-Ch-Ua-Platform": '"Windows"',
            "Accept": "*/*",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Dest": "empty",
            "Referer": f"{spec_dict['Web Link']}",
            "Accept-Encoding": "gzip, deflate, br",
            "Priority": "u=1, i",
        }
        response = requests.get(burp0_url, headers=burp0_headers)

        spec_data_more_list = json.loads(response.text)

        products_spec = [ i for i in spec_data_more_list]
        for product_sepc in products_spec:
            # product_spec = products_spec[0]
            for index, spec in enumerate(product_spec_list):
                
                if product_sepc['modelCode'] == product_spec_list[index]['model_code']:
                    key_list = [i['specList'][0]['name'].lower()for i in product_sepc['fullSpecs']]
                    value_list = [i['specList'][0]['value']for i in product_sepc['fullSpecs']]
                    for key, value in zip(key_list, value_list):
                        product_spec_list[index][key] = value
                else:
                    continue
        
    temp_list = []
    for d in product_spec_list:
        if d not in temp_list:
            temp_list.append(d)
    product_spec_list = temp_list
    with open(f"./data/{company}/{keyword}_detail_list.json", "w") as f:
        json.dump(product_spec_list, f)
        
    return product_spec_list
        
    
def crawl_compar(company, keyword):
    burp0_url = "https://www.samsung.com:443/us/smg/content/samsung/content-library/prepurchase/configurator/features/computing.json"
    burp0_cookies = {"s_fpid": "ca51c01d-5ee9-446d-8e2a-417c7c1ce864", "s_ecid": "MCMID%7C87417855217938127472167537113158430229", "AAMC_samsungelectronicsamericainc_0": "REGION%7C11", "aam_sc": "aamsc%3D4718718", "aam_uuid": "87457814995313514472169307816733127305", "_ga": "GA1.1.754102624.1719999038", "_gcl_au": "1.1.456890997.1719999042", "_fbp": "fb.1.1719999042694.603133754775108845", "__attentive_id": "759ce5410a6841909f6661476d2c54cd", "_attn_": "eyJ1Ijoie1wiY29cIjoxNzE5OTk5MDQzNDU0LFwidW9cIjoxNzE5OTk5MDQzNDU0LFwibWFcIjoyMTkwMCxcImluXCI6ZmFsc2UsXCJ2YWxcIjpcIjc1OWNlNTQxMGE2ODQxOTA5ZjY2NjE0NzZkMmM1NGNkXCJ9In0=", "__attentive_cco": "1719999043456", "mdLogger": "false", "kampyle_userid": "4761-c365-dda2-97ef-2d5b-d8a1-a8d4-36a7", "sa_did": "TpTIOzjXFYVNjKfDximQCUExfnkhRQFZ", "sa_773-397-549898": "{\"US\":{\"status\":\"GRANTED\",\"updated\":\"2024-07-03T09:30:44.077Z\",\"clientId\":\"kv5di1wr19\",\"deviceId\":\"TpTIOzjXFYVNjKfDximQCUExfnkhRQFZ\"}}", "_aeaid": "85b707ca-7980-4559-bfab-12ef78f3aaf5", "aelastsite": "IqynIxmTpWLTmucVE6VJcc93GvEXZoAScAF4P8JKEh9cCxYtr%2FMAw5Qj62MwuOMg", "__idcontext": "eyJjb29raWVJRCI6IjJpakxUVXFPRFYzRlRTNVhtV3J5RERWaFdMRiIsImRldmljZUlEIjoiMmlqTFRYQTNKU0t3OTg0MWI1cTl0SnQ4MDRyIiwiaXYiOiIiLCJ2IjoiIn0%3D", "iadvize-6528-vuid": "aaea3f6dc7fe4601934c09788763232752a9f5bb7d2f4", "BVBRANDID": "0bd2e407-e2a2-4ddc-ae6a-da0ee66d51ba", "aam_test": "segs%3D7431031", "country_region": "CA-ON", "country_codes": "tw", "device_type": "pc", "__COM_SPEED": "H", "ecom_vi_USA": "TUNNSUQlN0M4NzQxNzg1NTIxNzkzODEyNzQ3MjE2NzUzNzExMzE1ODQzMDIyOQ==", "ecom_session_id_USA": "M2Y4NmIzNTQtODY4YS00NTJhLTkwZWYtMjI4NjkxM2FlNzMz", "TS0171c81e": "016abffc7f79f3b3c1e5aa11c1854b3cb432edbb3f7540c440e758243b9f448c716e15797df9cc3a9eeafdb6f7c5313c3cabd6c596", "at_check": "true", "AMCVS_48855C6655783A647F000101%40AdobeOrg": "1", "DATradein": "true", "aelreadersettings": "%7B%22c_big%22%3A0%2C%22rg%22%3A0%2C%22memph%22%3A0%2C%22contrast_setting%22%3A0%2C%22colorshift_setting%22%3A0%2C%22text_size_setting%22%3A0%2C%22space_setting%22%3A0%2C%22font_setting%22%3A0%2C%22k%22%3A0%2C%22k_disable_default%22%3A0%2C%22hlt%22%3A0%2C%22disable_animations%22%3A0%2C%22display_alt_desc%22%3A0%7D", "cookie_country": "us", "targetUrl": "https://www.samsung.com/us/support/account", "recentlyViewed": "[]", "AMP_VID": "87417855217938127472167537113158430229", "__attentive_dv": "1", "da_lid": "54092D7898F9EA120504BB99E623DC888D|0|0|0", "TS011dc0a2": "016abffc7f43ee4e69d070cbe238b1d10c086fd8f5f39e1cd96b0e8da620c050225cf5c7c1a7bfddf97fb8143e81b0b71c862b68ad", "AMCV_48855C6655783A647F000101%40AdobeOrg": "1585540135%7CMCIDTS%7C19922%7CMCMID%7C87417855217938127472167537113158430229%7CMCAID%7CNONE%7CMCOPTOUT-1721201557s%7CNONE%7CMCAAMLH-1721799157%7C11%7CMCAAMB-1721799157%7Cj8Odv6LonN4r3an7LhD3WZrU1bUpAkFkkiY1ncBR96t2PTI%7CvVersion%7C4.4.0%7CMCCIDH%7C617300242", "eddzipcode": "96952", "AKA_A2": "A", "BVBRANDSID": "97cc909f-5755-4934-b14c-7ca94030aeca", "mboxEdgeCluster": "32", "tfpsi": "3f7e49b2-fd26-4227-ba91-5e27fc4f043a", "__attentive_pv": "1", "__attentive_ss_referrer": "ORGANIC", "RT": "\"z=1&dm=samsung.com&si=b47a61a0-913c-4cae-bef2-577b455043de&ss=lyphw11c&sl=2&tt=1sp&bcn=%2F%2F684d0d46.akstat.io%2F&ld=jj07\"", "s_pers": "%201%3D1%7C1721202466674%3B%20first_page_visit%3Dhttps%253A%252F%252Fwww.samsung.com%252Fus%252Fcomputing%252Fgalaxy-books%252Fgalaxy-book4-series%252Fbuy%252Fgalaxy-book4-360-15-6-intel-core-7-1tb-gray-np750qgk-kg1us%252F%7C1721202466675%3B%20s_nr%3D1721200666675-Repeat%7C1723792666675%3B%20gpv_pn%3Dhttps%253A%252F%252Fwww.samsung.com%252Fus%252Fcomputing%252Fgalaxy-books%252Fgalaxy-book4-edge%252Fbuy%252Fgalaxy-book4-edge-16-qualcomm-snapdragon-x-elite-1tb-sapphire-blue-np960xmb-kb1us%7C1721202466676%3B%20s_fbsr%3D1%7C1721202466678%3B", "OptanonConsent": "isGpcEnabled=0&datestamp=Wed+Jul+17+2024+15%3A17%3A48+GMT%2B0800+(%E5%8F%B0%E5%8C%97%E6%A8%99%E6%BA%96%E6%99%82%E9%96%93)&version=202307.1.0&browserGpcFlag=0&isIABGlobal=false&hosts=&consentId=6e84f1e6-7025-40cd-92e7-7815681c8f8e&interactionCount=1&landingPath=NotLandingPage&groups=C0001%3A1%2CC0003%3A1%2CC0002%3A1%2CBG17%3A1%2CC0004%3A1&AwaitingReconsent=false", "_ga_0JTZHYKZ5Z": "GS1.1.1721199747.5.1.1721200668.49.0.0", "kampyleUserSession": "1721200670030", "kampyleUserSessionsCount": "7", "kampyleSessionPageCounter": "1", "_uetsid": "1f914fc043ed11ef8084ad2219debf21", "_uetvid": "e8e16910391e11efb4bc1da188de5359", "platform": "Windows", "utag_main": "v_id:019077ee63e00006b857e634d6ed05073003106b009dcsamsung_live$_sn:5$_se:24$_ss:0$_st:1721202534258$tapid_reset:true%3Bexp-1751535034159$dc_visit:5$ses_id:1721199752560%3Bexp-session$_pn:3%3Bexp-session$dc_event:22%3Bexp-session$_prevpage:%3Bexp-1721204334263$adobe_mcid:87417855217938127472167537113158430229%3Bexp-session$aa_vid:%3Bexp-session$dc_region:ap-east-1%3Bexp-session", "s_sess": "%20c_m%3DundefinedTyped%252FBookmarkedTyped%252FBookmarkedundefined%3B%20s_ppvl%3Dhttps%25253A%252F%252Fwww.samsung.com%252Fus%252Fcomputing%252Fgalaxy-books%252Fgalaxy-book4-series%252Fbuy%252Fgalaxy-book4-360-15-6-intel-core-7-1tb-gray-np750qgk-kg1us%252C20%252C20%252C738%252C807%252C738%252C1536%252C864%252C1.25%252CL%3B%20s_cc%3Dtrue%3B%20s_sq%3D%3B%20s_ppv%3Dhttps%25253A%252F%252Fwww.samsung.com%252Fus%252Fcomputing%252Fgalaxy-books%252Fgalaxy-book4-edge%252Fbuy%252Fgalaxy-book4-edge-16-qualcomm-snapdragon-x-elite-1tb-sapphire-blue-np960xmb-kb1us%252C19%252C78%252C4958%252C807%252C738%252C1536%252C864%252C1.25%252CL%3B", "mbox": "PC#33eb4a24a67a45f087aed19c4979daaf.32_0#1784445463|session#99e84de24e884b9eb8e5819e022a1efe#1721202603"}
    burp0_headers = {"Sec-Ch-Ua": "\"Not/A)Brand\";v=\"8\", \"Chromium\";v=\"126\"", "Accept-Language": "zh-TW", "Sec-Ch-Ua-Mobile": "?0", "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.6478.127 Safari/537.36", "Sec-Ch-Ua-Platform": "\"Windows\"", "Accept": "*/*", "Sec-Fetch-Site": "same-origin", "Sec-Fetch-Mode": "cors", "Sec-Fetch-Dest": "empty", "Referer": "https://www.samsung.com/us/comparepop/?categories=computing&familyType=galaxy-book4-edge", "Accept-Encoding": "gzip, deflate, br", "Priority": "u=1, i"}
    response = requests.get(burp0_url, headers=burp0_headers, cookies=burp0_cookies)

    compare_data_list = json.loads(response.text)['devices']

    transformed_list = []

    for item in compare_data_list:
        transformed_dict = {}
        transformed_dict['product_name'] = item['id'].replace('-',' ')
        for i in item['features'].keys():
            try:
                transformed_dict[i.lower()] = item['features'][i]['text']
            except:
                print('0')
        transformed_list.append(transformed_dict)
        
    with open(f"./data/{company}/{keyword}_compare_list.json", "w") as f:
        json.dump(transformed_list, f)
    return transformed_list

def detail_laptop(company, keyword):
    with open(f"./data/{company}/{keyword}_detail_list.json", "r") as f:
        product_detail_list = json.load(f)

    with open(f"./data/{company}/{keyword}_compare_list.json", "r") as f:
        compare_list = json.load(f)
        
    df_product_details = pd.DataFrame(product_detail_list)
    df_compare_list = pd.DataFrame(compare_list)

    df_product_details['merge_key'] = df_product_details['Model Name'].apply(lambda x: x.split(',')[0].lower().replace("\"", "").replace("14", "").replace("16", "").replace(" ", ""))
    df_compare_list['merge_key'] = df_compare_list['product_name'].apply(lambda x:x.replace(" ", ""))

    merged_df = pd.merge(df_product_details, df_compare_list, on='merge_key', how='left')
    
    # merged_df.to_csv(f"./data/{company}/{keyword}_merged.csv", index=False,encoding='utf-8-sig')
    
    merged_df['Official Price'] = merged_df['price']
    merged_df['Ports & Slots'] = merged_df['otherconnectivity']
    merged_df['Camera'] = merged_df['webcam']
    merged_df['Display'] = merged_df['screendisplay']
    merged_df['Primary Battery'] = merged_df['battery']
    merged_df['Processor'] = merged_df['processor_x']
    merged_df['Graphics Card'] = merged_df['graphics']
    merged_df['Hard Drive'] = merged_df['storage_x'].apply(lambda x: x.split('+')[1])
    merged_df['Memory'] = merged_df['storage_x'].apply(lambda x: x.split('+')[0])
    merged_df['Operating System'] = merged_df['operating system']
    merged_df['Audio and Speakers'] = merged_df['speakers']
    
    def demension_part(row):
        parts = row['dimensions'].split('<br/>')
        print(parts)

        if '14' in row['display']and '14' in row['dimensions']:
            # Extract and store 14" dimensions
            return parts[0].split('14”:')[-1].strip()
        elif '16' in row['display']and '16' in row['dimensions']:
            # Extract and store 16" dimensions
            return parts[1].split('16”:')[-1].strip()
        else:
            # Handling single dimension entries (assuming they are 14" or 16" based on context or default)
            # Here, you might need a more sophisticated logic based on your requirements
            return parts[0]
        
    merged_df['Dimensions'] = merged_df.apply(demension_part, axis=1)
    
    import re 
    def extract_dimensions(row):
        # Define the regular expression pattern for matching numbers
        pattern = r'(\d+\.?\d*)”'
        
        # Extract all numbers from the 'Dimensions' string
        numbers = re.findall(pattern, row['Dimensions'])
        
        # Check if three numbers (length, width, height) are found
        if len(numbers) == 3:
            # Convert numbers to float and multiply by 25.4 to convert inches to millimeters
            length_mm, width_mm, height_mm = [float(num) * 25.4 for num in numbers]
            return length_mm, width_mm, height_mm
        else:
            # Return None or some default values if the expected three numbers are not found
            return None, None, None

    # Apply the function to each row and create new columns for Length, Width, and Height in millimeters
    merged_df[['Depth(mm)', 'Width(mm)', 'Height(mm)']] = merged_df.apply(lambda row: extract_dimensions(row), axis=1, result_type='expand')

    def lbs_to_kg(weight_str):
        weight_str = str(weight_str)
        if weight_str == "NaN":
            return None
        # Regular expression to find the numeric value in the weight string
        match = re.search(r'(\d+(\.\d+)?)\s*lb', weight_str)
        if match:
            # Extract the numeric value and convert it to float
            weight_lbs = float(match.group(1))
            # Convert lbs to kg (1 lb = 0.453592 kg)
            weight_kg = weight_lbs * 0.453592
            return weight_kg
        else:
            # Return the original string if no match is found
            return weight_str
    
    merged_df['Weight(kg)'] =  merged_df['weight_x'].apply(lbs_to_kg)
    merged_df['WWAN'] = 'TBD'
    
    #TODO keyboard中也會出現
    def set_fpr(row):
        # 检查'fingerprint reader'字段是否为'yes'
        if "finger" in str(row["security"]).lower():
            return "Yes"

        else:
            return None

    merged_df['FPR_model'] = None
    merged_df["FPR"] = merged_df.apply(set_fpr, axis=1)
    
    merged_df['NFC'] = 'TBD'
    
    merged_df['Power Supply'] = 'TBD'
    
    merged_df['Type'] = None
    
    merged_df['Brand'] = company
    
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
    
    
    merged_df[columns_to_output].to_csv(
        f"./data/{company}/{keyword}.csv", encoding="utf-8-sig", index=False
    )
    
    
    
    
    


company = "Samsung"
keyword_list =['laptop','desktop','docking']
keyword = keyword_list[0]

crawl_product(company, keyword)
crawl_compar(company, keyword)