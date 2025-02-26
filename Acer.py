import requests
import re
import json
from bs4 import BeautifulSoup
from tqdm import tqdm
import pandas as pd


def search_crawl_store(keyword):

    burp0_url = f"https://store.acer.com/en-us/catalogsearch/result/?q={keyword}&product_list_limit=all"
    burp0_headers = {
        "Sec-Ch-Ua": '"Not/A)Brand";v="8", "Chromium";v="126"',
        "Sec-Ch-Ua-Mobile": "?0",
        "Sec-Ch-Ua-Platform": '"Windows"',
        "Accept-Language": "zh-TW",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.6478.57 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-User": "?1",
        "Sec-Fetch-Dest": "document",
        "Accept-Encoding": "gzip, deflate, br",
        "Priority": "u=0, i",
        "Connection": "keep-alive",
    }

    response = requests.get(burp0_url, headers=burp0_headers)
    soup = BeautifulSoup(response.content, "html.parser")

    # 網頁顯示129筆，但是可以根據每個產品的關鍵字查詢，只有128筆
    product_soup = soup.select(".products.list.items.product-items>li")

    product_name_list = [
        i.select(".product-item-link")[0].text.strip() for i in product_soup
    ]
    link_list = [i.select(".product-item-link")[0]["href"] for i in product_soup]
    price_list = [
        i.select(".price")[0].text.strip().replace(",", "") for i in product_soup
    ]
    price_list = [re.findall(r"\$(\d+\.\d+)", price)[0] for price in price_list]
    partnumber_list = [
        i.select(".sku-wrapper>span")[0].text.strip() for i in product_soup
    ]

    # Combine the lists into a list of dictionaries
    products_list = [
        {
            "Model Name": name,
            "Official Price": price,
            "Web Link": link,
            "partnumber": partnumber,
        }
        for name, price, link, partnumber in zip(
            product_name_list, price_list, link_list, partnumber_list
        )
    ]
    print(len(products_list))
    # Write the JSON data to a file
    with open(f"./{company}/{keyword}_store_search.json", "w") as f:
        json.dump(products_list, f)
    return products_list


def detail_crawl_store(keyword, company):
    with open(f"./{company}/{keyword}_store_search.json", "r") as f:
        products_list = json.load(f)

    product_detail_list = []
    error_link = []

    # products_list = products_list[:10]
    for product in tqdm(products_list):
        # product = products_list[2]
        # product['Web Link'] = 'https://store.acer.com/en-us/acer-usb-type-c-gen-1-dock-adk233'
        try:
            print(product["Web Link"])

            burp0_url = product["Web Link"]
            # burp0_cookies = {"form_key": "vgoj3duqryArpQRO", "PHPSESSID": "b50755b3141b8456b2f6aa398b7bf610", "mage-messages": "", "amzn-checkout-session": "{}", "mage-banners-cache-storage": "{}", "acer_cdn_uc": "TW", "cjConsent": "MHxOfDB8Tnww", "cjUser": "ab0e0111-61eb-4ac4-b1f7-e921152b0868", "BVBRANDID": "a5951b5b-505c-46a7-a592-5eafabfd8f61", "ak_bmsc": "F93DB5F97A6D34D99A0A55F1D7A8C0D2~000000000000000000000000000000~YAAQRVFFy7JqvU6QAQAAUtPVVxhjQnHbS7cFx5SokKUPLFWDB8CO46580aXt9bEsFC3hxU2sq8pzUooSnh8na0MVATmkGIM/ZWdKE/Do8Jk4yyrC/7aaPUFg/dbedSOhbClBLO+kZ1yJAwxSZXdPq4bsJlY+lj6wDBh81LyUTXe5ymFkwplSpYrK8my0kr1LzZRxFtBQLO8/wTnWrYCIFydnsrwGn+FSrMyIwnQcQn5E1Vcz5uZDviU2LoWJ88aXeyVn4rwuHICWB5xNLcHIUKR9TBqA50Meke86yrN+aagIsFtRaLNIA6lZuWZjbPw5Ly3FjI2jnrDyfOhqS8HQxBMaWt5vLYsuqWNRY08tifeN1XTo5+jbBCYee8Fuh/s/q0OZ4cOGGqgV8CrxnvKVBK+wDQgIwqeoDK2Sp/ynpnuUFZ9H8M+c2p9oL1XDQA9sLPjy/zXvk4u0TQ==", "form_key": "vgoj3duqryArpQRO", "mage-cache-storage": "{}", "mage-cache-storage-section-invalidation": "{}", "mage-cache-sessid": "true", "X-Magento-Vary": "440e2bacebf967713a94f59932925c19e0b350405ae8d56fb6ce07ee046d6626", "new_location_accept_7": "survive", "recently_viewed_product": "{}", "recently_viewed_product_previous": "{}", "recently_compared_product": "{}", "recently_compared_product_previous": "{}", "product_data_storage": "{}", "_gid": "GA1.2.58257579.1719460552", "_clck": "dcwk9g%7C2%7Cfmz%7C0%7C1639", "tracker_device": "f0a94017-3ac2-49bd-8567-3aab032a4877", "OptanonAlertBoxClosed": "2024-06-27T03:55:53.501Z", "_gcl_au": "1.1.1899292473.1719460554", "__pdst": "96f79cf66cb346809a150daf94a30669", "_fbp": "fb.1.1719460554379.329306018587320999", "_tt_enable_cookie": "1", "_ttp": "HbHppfKdngt7VD_jmrPbjI4Cs7M", "rskxRunCookie": "0", "rCookie": "tg7y0arqz488e5dojsgg2lxwqf36h", "sa-user-id": "s%253A0-b4683bf3-578c-560c-7c22-cd27c72f45e7.%252F2%252FIbopRoo49fbps5yOB68nvghqOoICZJ36rW1YEmXM", "sa-user-id-v2": "s%253AtGg781eMVgx8Is0nxy9F53IgRFk.vBV40ameKrCaGlTapIkb9h9%252B%252F1Ns2T%252F%252FhLk%252BAlTur7U", "optiMonkClientId": "c773677b-1b48-b038-1c53-243e4adafd48", "optiMonkSession": "1719460558", "select_item_attribution_table": "eyJOUC5CQUcxMS4wMTQiOnsiaXRlbV9pZCI6Ik5QLkJBRzExLjAxNCIsIml0ZW1fbGlzdF9uYW1lIjoiYWNlcl9zdG9yZXx8b3RoZXJzfHxzZWFyY2hfcmVzdWx0cyJ9fQ==", "_hjSessionUser_1568973": "eyJpZCI6ImRhYWMyNzMzLTZjZWItNWQ2MS1hODQ2LTliNWEyN2UzMzJkOCIsImNyZWF0ZWQiOjE3MTk0NjA1NTI1ODYsImV4aXN0aW5nIjp0cnVlfQ==", "OptanonConsent": "isGpcEnabled=0&datestamp=Thu+Jun+27+2024+11%3A59%3A44+GMT%2B0800+(%E5%8F%B0%E5%8C%97%E6%A8%99%E6%BA%96%E6%99%82%E9%96%93)&version=202401.2.0&browserGpcFlag=0&isIABGlobal=false&hosts=&consentId=bfb34329-6f88-44de-83de-469de3b5ac63&interactionCount=1&landingPath=NotLandingPage&groups=C0001%3A1%2CC0003%3A1%2CC0002%3A1%2CC0004%3A1%2CC0007%3A1&geolocation=TW%3BNWT&AwaitingReconsent=false", "private_content_version": "7b62f377306442b142e02dba67762e5e", "_ga": "GA1.2.2096787537.1719460552", "_uetsid": "26ccba10343911ef8b8615064b00734c", "_uetvid": "26cce670343911efaccb97d36d8c7f24", "_rdt_uuid": "1719460554616.08424c82-5457-4f9c-8a3f-8830da844087", "sa-user-id-v3": "s%253AAQAKIO3OP2uqNimWCDE0oVHtTdMj2Q2GY4gUaNFonqElPYzeEAEYAyCxx_OzBjABOgRW4AZNQgRvPXQx.93yS22vUWn4UXSde49s46yG7xtkRTS1AYdMR15QIMxk", "optiMonkClient": "N4IgjAbBAMDMAsIBcoDGBDZwC+AaEAZgG7JgDsYAnPDAKy0T4A2JS5VN0ZAHIyAHYB7AA6tY2bEA", "bm_sv": "A02C64D5FBEC888EB9291CF256612E86~YAAQRVFFy8NuvU6QAQAAAXPZVxgIqS+j+0DIQB6e5s2zU33++Pve3d1MB5AZLho2BPDSkdYaeXI22sm7ViSBxjeye2p1DBCQZdkxtxqF2VIqFPhWy8N9+ae1o0k4YM70zDFpgCCW6EjZZYhuqURS6iwyL+9GAFAUvlF9fuVJWJxfvwZYYJqXbCYrJKf3+FvEedtDSFzell4ai+coNrxwY8zxZ1noFYT6IJRrG/WPwazc/WjT64w/sHcRS7mMd1k=~1", "lastRskxRun": "1719460788567", "section_data_ids": "{%22company%22:1719460785%2C%22customer-type%22:1719460785%2C%22customer%22:1719460551}", "_ga_22YFFZRGG3": "GS1.1.1719460551.1.1.1719461617.60.0.0", "_ga_6G48RXXLNZ": "GS1.1.1719460551.1.1.1719461617.60.0.0", "_clsk": "pwbsfz%7C1719464976448%7C1%7C1%7Ct.clarity.ms%2Fcollect"}
            burp0_headers = {
                "Sec-Ch-Ua": '"Not/A)Brand";v="8", "Chromium";v="126"',
                "Sec-Ch-Ua-Mobile": "?0",
                "Sec-Ch-Ua-Platform": '"Windows"',
                "Accept-Language": "zh-TW",
                "Upgrade-Insecure-Requests": "1",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.6478.57 Safari/537.36",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
                "Sec-Fetch-Site": "none",
                "Sec-Fetch-Mode": "navigate",
                "Sec-Fetch-User": "?1",
                "Sec-Fetch-Dest": "document",
                "Accept-Encoding": "gzip, deflate, br",
                "Priority": "u=0, i",
            }
            response = requests.get(burp0_url, headers=burp0_headers)

            soup = BeautifulSoup(response.content, "html.parser")
            product_soup_key = soup.select(".table>tbody>tr>.col.label")
            product_soup_value = soup.select(".table>tbody>tr>.col.data")

            spect_dict = {}
            for key, value in zip(product_soup_key, product_soup_value):
                spect_dict[key.text.strip().lower()] = value.text.strip()
            
            # 抓產品敘述
            if keyword =="docking":
                spect_dict["Ports & Slots"] = ','.join([i.text.strip() for i in soup.select(".clearfix>li")])

            if soup.select(".rich-content-container"):
                rich_number = soup.select(".rich-content-container")[0]["src"].split(
                    "/"
                )[-2]
                rich_search_link = f"https://reseller.spexaccess.net/service/rest/spexWidget?method=getSpexWidgetContent&authKey=b6dc21f90311162668556f204182e625&profileId=9&locale=en_us&disableGeneratedOverview=false&partNumber={rich_number}&mfgName=Acer%2C%20Inc&callback=spexWidgetContent.loadProductData"
                burp0_headers = {
                    "Sec-Ch-Ua": '"Not/A)Brand";v="8", "Chromium";v="126"',
                    "Sec-Ch-Ua-Mobile": "?0",
                    "Sec-Ch-Ua-Platform": '"Windows"',
                    "Accept-Language": "zh-TW",
                    "Upgrade-Insecure-Requests": "1",
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.6478.57 Safari/537.36",
                    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
                    "Sec-Fetch-Site": "none",
                    "Sec-Fetch-Mode": "navigate",
                    "Sec-Fetch-User": "?1",
                    "Sec-Fetch-Dest": "document",
                    "Accept-Encoding": "gzip, deflate, br",
                    "Priority": "u=0, i",
                    "Connection": "keep-alive",
                }
                response_search_rich = requests.get(
                    rich_search_link, headers=burp0_headers
                )
                data = response_search_rich.content.decode("utf-8")

                rich_link = re.findall(
                    r"https://content\.etilize\.com/rich-marketing/en_us/\d+\.html",
                    data,
                )[0]

                response_search_rich = requests.get(rich_link, headers=burp0_headers)

                response_search_rich_soup = BeautifulSoup(
                    response_search_rich.content, "html.parser"
                )

                content_text = "".join(
                    [i.text.lower() for i in response_search_rich_soup.select("p")]
                )
                re.findall(r"4g(?!b|hz)", content_text)
                if re.findall(r"4g(?!b|hz)", content_text) :
                    spect_dict["wwan"] = "4G"
                elif re.findall(r"5g(?!b|hz)", content_text):
                    spect_dict["wwan"] = "5G"
                elif re.findall(r"5g(?!b|hz)", content_text) and re.findall(r"4g(?!b|hz)", content_text):
                    spect_dict["wwan"] = "4G/5G"

                if "nfc" in content_text:
                    spect_dict["nfc"] = "Yes"
                else:
                    spect_dict["nfc"] = None

                if "fingerprint" in content_text:
                    spect_dict["FPR"] = "Yes"
                    
            
                

            product_detail_list.append({**product, **spect_dict})
        except:
            error_link.append(product["Web Link"])

    with open(f"./{company}/{keyword}_store_detail_list.json", "w") as f:
        json.dump(product_detail_list, f)

    with open(f"./{company}/{keyword}_store_error_link_list.json", "w") as f:
        json.dump(error_link, f)

    return product_detail_list, error_link


def search_crawl(keyword):

    data = []
    for page in range(1, 3):
        # page=1
        print(page)
        burp0_url = "https://www.acer.com:443/us-en/MicroService/search/"
        burp0_cookies = {
            "cjConsent": "MHxOfDB8Tnww",
            "cjUser": "ab0e0111-61eb-4ac4-b1f7-e921152b0868",
            "BVBRANDID": "a5951b5b-505c-46a7-a592-5eafabfd8f61",
            "_gid": "GA1.2.58257579.1719460552",
            "_clck": "dcwk9g%7C2%7Cfmz%7C0%7C1639",
            "OptanonAlertBoxClosed": "2024-06-27T03:55:53.501Z",
            "_gcl_au": "1.1.1899292473.1719460554",
            "_fbp": "fb.1.1719460554379.329306018587320999",
            "_tt_enable_cookie": "1",
            "_ttp": "HbHppfKdngt7VD_jmrPbjI4Cs7M",
            "rskxRunCookie": "0",
            "rCookie": "tg7y0arqz488e5dojsgg2lxwqf36h",
            "select_item_attribution_table": "eyJOUC5CQUcxMS4wMTQiOnsiaXRlbV9pZCI6Ik5QLkJBRzExLjAxNCIsIml0ZW1fbGlzdF9uYW1lIjoiYWNlcl9zdG9yZXx8b3RoZXJzfHxzZWFyY2hfcmVzdWx0cyJ9fQ==",
            "_hjSessionUser_1568973": "eyJpZCI6ImRhYWMyNzMzLTZjZWItNWQ2MS1hODQ2LTliNWEyN2UzMzJkOCIsImNyZWF0ZWQiOjE3MTk0NjA1NTI1ODYsImV4aXN0aW5nIjp0cnVlfQ==",
            "_uetsid": "26ccba10343911ef8b8615064b00734c",
            "_uetvid": "26cce670343911efaccb97d36d8c7f24",
            "lastRskxRun": "1719465001726",
            "_ga_22YFFZRGG3": "GS1.1.1719478266.3.0.1719478266.60.0.0",
            "ASP.NET_SessionId": "veqt2jzo5dcjviu2wcxmuo41",
            "acer_cdn_uc": "TW",
            "acer_cdn_ulc": "us-en",
            "_vwo_uuid_v2": "DCE36CECF852D10592B2B7A7A67FC5ADC|10026b2e2820af9c0896ad67519bba22",
            "_ga": "GA1.2.2096787537.1719460552",
            "ak_bmsc": "6AB3B1C25BB1F98C477FE337A228380C~000000000000000000000000000000~YAAQhlFFy37xd0mQAQAAW5CCWhgoP+9D1qeeBUe/Y7k2tyfqeo7eINv1ledpGMl4VnYSwauIKvAhGorKQe3s4Twx7OdStHFFDK2lr4xrKRnVTKvR33RAcP1Xmmyud6hYLN+DRemCBhJMWZlx8kEGsyrmfCs3yYLuBODAERnH8goIsD4Huf/DkJYSNcUthevZfsnazA8FpQjr+UUC/32UjgXm5qJaBN0NoBz2xIcpJcTOy7V2ZGDzjfrkLp4umANpB/YD5lP3dui9/WdnBy6wg2aS7nBaUW0rqLAJd3c+rhpVl/TFUAvamXNjxrksDRRFoJ1g6Qps6nQFLyuYaKD15fBpWrdaerkiAe2WTL+dE6I0urd538P0xRgVCwqz/QBAVPjw0BzL+jaNaIvrnIxa/UAJQZq7U/pzmizjB5QvKnZhLaMYbYNsed9hiIzjLh5XAuWV+HWzqvcNSA==",
            "OptanonConsent": "isGpcEnabled=0&datestamp=Fri+Jun+28+2024+00%3A23%3A45+GMT%2B0800+(%E5%8F%B0%E5%8C%97%E6%A8%99%E6%BA%96%E6%99%82%E9%96%93)&version=202401.2.0&browserGpcFlag=0&isIABGlobal=false&hosts=&consentId=bfb34329-6f88-44de-83de-469de3b5ac63&interactionCount=1&landingPath=NotLandingPage&groups=C0001%3A1%2CC0003%3A1%2CC0002%3A1%2CC0004%3A1%2CC0007%3A1&geolocation=TW%3BNWT&AwaitingReconsent=false",
            "__pdst": "247a6bf5b3af4437be7a5cbd6fc954d9",
            "tfpsi": "8e33acae-2878-4990-b179-d7acfc344cac",
            "_rdt_uuid": "1719460554616.08424c82-5457-4f9c-8a3f-8830da844087",
            "sa-user-id": "s%253A0-b4683bf3-578c-560c-7c22-cd27c72f45e7.%252F2%252FIbopRoo49fbps5yOB68nvghqOoICZJ36rW1YEmXM",
            "sa-user-id-v2": "s%253AtGg781eMVgx8Is0nxy9F53IgRFk.vBV40ameKrCaGlTapIkb9h9%252B%252F1Ns2T%252F%252FhLk%252BAlTur7U",
            "sa-user-id-v3": "s%253AAQAKIO3OP2uqNimWCDE0oVHtTdMj2Q2GY4gUaNFonqElPYzeEAEYAyCSpPazBjABOgRW4AZNQgRez3Uo.mt8TNwS2mjE%252BgWl6kD4z0tK2%252FLzwiFd2DWTkLQGBiiI",
            "_clsk": "15hq792%7C1719505427517%7C1%7C1%7Ct.clarity.ms%2Fcollect",
            "bm_sv": "B85D96383FD1E35438AF00B15B2EFEF5~YAAQhlFFy6bxd0mQAQAAdK+CWhjOKRQ1m8kifYg86iCVOIP0njAb6V3C6Mua5R7iW9/WutN7mL7wKO611l8pdqzIY7RjYN+uz8rbLZHL47YZJKe7g25ATzKU6zX9c1cWkeMcFDq4NBz5xPYMoQGtmV+Atc9sP4ZvSWwylS4BrvqHPtUFYPXEZ9FX3SkMATMi40hcqEj5Ph9S8DyPmHGkXdEJYSSdU5m7KhAja3xqjuOnxZcuL1+U38sAtUClkA==~1",
            "_gat_UA-18261064-1": "1",
            "_ga_6G48RXXLNZ": "GS1.1.1719505424.4.1.1719505501.58.0.0",
            "_ga_LFZ641THDF": "GS1.1.1719505424.1.1.1719505501.58.0.0",
        }
        burp0_headers = {
            "Sec-Ch-Ua": '"Not/A)Brand";v="8", "Chromium";v="126"',
            "Tracestate": "1445366@nr=0-1-3050433-1400769139-6ebdc545c0a7f057----1719505502688",
            "Traceparent": "00-63b538f4a964060708b19f208721873b-6ebdc545c0a7f057-01",
            "Accept-Language": "zh-TW",
            "Sec-Ch-Ua-Mobile": "?0",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.6478.57 Safari/537.36",
            "Newrelic": "eyJ2IjpbMCwxXSwiZCI6eyJ0eSI6IkJyb3dzZXIiLCJhYyI6IjMwNTA0MzMiLCJhcCI6IjE0MDA3NjkxMzkiLCJpZCI6IjZlYmRjNTQ1YzBhN2YwNTciLCJ0ciI6IjYzYjUzOGY0YTk2NDA2MDcwOGIxOWYyMDg3MjE4NzNiIiwidGkiOjE3MTk1MDU1MDI2ODgsInRrIjoiMTQ0NTM2NiJ9fQ==",
            "Content-Type": "text/plain;charset=UTF-8",
            "Sec-Ch-Ua-Platform": '"Windows"',
            "Accept": "*/*",
            "Origin": "https://www.acer.com",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Dest": "empty",
            "Referer": "https://www.acer.com/us-en/search/search-explore?search=laptop",
            "Accept-Encoding": "gzip, deflate, br",
            "Priority": "u=1, i",
        }
        burp0_json = {
            "filter": {"category": "explore", "section_name": "products"},
            "page_infor": {"page": page, "size": 300},
            "pdp_results": "600",
            "query_string": keyword,
            "sort_by": {"type": "relevance"},
        }
        response = requests.post(
            burp0_url, headers=burp0_headers, cookies=burp0_cookies, json=burp0_json
        )

        data.extend(response.json()["searchResult"])

    product_name_list = [i["ProductName"] for i in data]
    link_list = ["https://www.acer.com" + i["PDPUrl"] for i in data]
    partnumber_list = [i["PartNumber"] for i in data]
    # price_list = [i['Price'] for i in data ]

    # Combine the lists into a list of dictionaries
    products_list = [
        {"Model Name": name, "Web Link": link, "partnumber": partnumber}
        for name, link, partnumber in zip(product_name_list, link_list, partnumber_list)
    ]
    print(len(products_list))
    # Write the JSON data to a file
    with open(f"./{company}/{keyword}_search.json", "w") as f:
        json.dump(products_list, f)
    return products_list


def detail_crawl(keyword, company):
    with open(f"./{company}/{keyword}_search.json", "r") as f:
        products_list = json.load(f)

    product_detail_list = []
    error_link = []

    # products_list = products_list[:50]
    for product in tqdm(products_list):
        # product = products_list[307]
        # product['Web Link'] = 'https://www.acer.com/us-en/laptops/aspire/aspire-5-intel/pdp/NX.KN3AA.006'
        try:

            


            print(product["Web Link"])
            spect_dict = {}
            

            burp0_url = product["Web Link"]+"#addtion"
            
            # burp0_cookies = {"form_key": "vgoj3duqryArpQRO", "PHPSESSID": "b50755b3141b8456b2f6aa398b7bf610", "mage-messages": "", "amzn-checkout-session": "{}", "mage-banners-cache-storage": "{}", "acer_cdn_uc": "TW", "cjConsent": "MHxOfDB8Tnww", "cjUser": "ab0e0111-61eb-4ac4-b1f7-e921152b0868", "BVBRANDID": "a5951b5b-505c-46a7-a592-5eafabfd8f61", "ak_bmsc": "F93DB5F97A6D34D99A0A55F1D7A8C0D2~000000000000000000000000000000~YAAQRVFFy7JqvU6QAQAAUtPVVxhjQnHbS7cFx5SokKUPLFWDB8CO46580aXt9bEsFC3hxU2sq8pzUooSnh8na0MVATmkGIM/ZWdKE/Do8Jk4yyrC/7aaPUFg/dbedSOhbClBLO+kZ1yJAwxSZXdPq4bsJlY+lj6wDBh81LyUTXe5ymFkwplSpYrK8my0kr1LzZRxFtBQLO8/wTnWrYCIFydnsrwGn+FSrMyIwnQcQn5E1Vcz5uZDviU2LoWJ88aXeyVn4rwuHICWB5xNLcHIUKR9TBqA50Meke86yrN+aagIsFtRaLNIA6lZuWZjbPw5Ly3FjI2jnrDyfOhqS8HQxBMaWt5vLYsuqWNRY08tifeN1XTo5+jbBCYee8Fuh/s/q0OZ4cOGGqgV8CrxnvKVBK+wDQgIwqeoDK2Sp/ynpnuUFZ9H8M+c2p9oL1XDQA9sLPjy/zXvk4u0TQ==", "form_key": "vgoj3duqryArpQRO", "mage-cache-storage": "{}", "mage-cache-storage-section-invalidation": "{}", "mage-cache-sessid": "true", "X-Magento-Vary": "440e2bacebf967713a94f59932925c19e0b350405ae8d56fb6ce07ee046d6626", "new_location_accept_7": "survive", "recently_viewed_product": "{}", "recently_viewed_product_previous": "{}", "recently_compared_product": "{}", "recently_compared_product_previous": "{}", "product_data_storage": "{}", "_gid": "GA1.2.58257579.1719460552", "_clck": "dcwk9g%7C2%7Cfmz%7C0%7C1639", "tracker_device": "f0a94017-3ac2-49bd-8567-3aab032a4877", "OptanonAlertBoxClosed": "2024-06-27T03:55:53.501Z", "_gcl_au": "1.1.1899292473.1719460554", "__pdst": "96f79cf66cb346809a150daf94a30669", "_fbp": "fb.1.1719460554379.329306018587320999", "_tt_enable_cookie": "1", "_ttp": "HbHppfKdngt7VD_jmrPbjI4Cs7M", "rskxRunCookie": "0", "rCookie": "tg7y0arqz488e5dojsgg2lxwqf36h", "sa-user-id": "s%253A0-b4683bf3-578c-560c-7c22-cd27c72f45e7.%252F2%252FIbopRoo49fbps5yOB68nvghqOoICZJ36rW1YEmXM", "sa-user-id-v2": "s%253AtGg781eMVgx8Is0nxy9F53IgRFk.vBV40ameKrCaGlTapIkb9h9%252B%252F1Ns2T%252F%252FhLk%252BAlTur7U", "optiMonkClientId": "c773677b-1b48-b038-1c53-243e4adafd48", "optiMonkSession": "1719460558", "select_item_attribution_table": "eyJOUC5CQUcxMS4wMTQiOnsiaXRlbV9pZCI6Ik5QLkJBRzExLjAxNCIsIml0ZW1fbGlzdF9uYW1lIjoiYWNlcl9zdG9yZXx8b3RoZXJzfHxzZWFyY2hfcmVzdWx0cyJ9fQ==", "_hjSessionUser_1568973": "eyJpZCI6ImRhYWMyNzMzLTZjZWItNWQ2MS1hODQ2LTliNWEyN2UzMzJkOCIsImNyZWF0ZWQiOjE3MTk0NjA1NTI1ODYsImV4aXN0aW5nIjp0cnVlfQ==", "OptanonConsent": "isGpcEnabled=0&datestamp=Thu+Jun+27+2024+11%3A59%3A44+GMT%2B0800+(%E5%8F%B0%E5%8C%97%E6%A8%99%E6%BA%96%E6%99%82%E9%96%93)&version=202401.2.0&browserGpcFlag=0&isIABGlobal=false&hosts=&consentId=bfb34329-6f88-44de-83de-469de3b5ac63&interactionCount=1&landingPath=NotLandingPage&groups=C0001%3A1%2CC0003%3A1%2CC0002%3A1%2CC0004%3A1%2CC0007%3A1&geolocation=TW%3BNWT&AwaitingReconsent=false", "private_content_version": "7b62f377306442b142e02dba67762e5e", "_ga": "GA1.2.2096787537.1719460552", "_uetsid": "26ccba10343911ef8b8615064b00734c", "_uetvid": "26cce670343911efaccb97d36d8c7f24", "_rdt_uuid": "1719460554616.08424c82-5457-4f9c-8a3f-8830da844087", "sa-user-id-v3": "s%253AAQAKIO3OP2uqNimWCDE0oVHtTdMj2Q2GY4gUaNFonqElPYzeEAEYAyCxx_OzBjABOgRW4AZNQgRvPXQx.93yS22vUWn4UXSde49s46yG7xtkRTS1AYdMR15QIMxk", "optiMonkClient": "N4IgjAbBAMDMAsIBcoDGBDZwC+AaEAZgG7JgDsYAnPDAKy0T4A2JS5VN0ZAHIyAHYB7AA6tY2bEA", "bm_sv": "A02C64D5FBEC888EB9291CF256612E86~YAAQRVFFy8NuvU6QAQAAAXPZVxgIqS+j+0DIQB6e5s2zU33++Pve3d1MB5AZLho2BPDSkdYaeXI22sm7ViSBxjeye2p1DBCQZdkxtxqF2VIqFPhWy8N9+ae1o0k4YM70zDFpgCCW6EjZZYhuqURS6iwyL+9GAFAUvlF9fuVJWJxfvwZYYJqXbCYrJKf3+FvEedtDSFzell4ai+coNrxwY8zxZ1noFYT6IJRrG/WPwazc/WjT64w/sHcRS7mMd1k=~1", "lastRskxRun": "1719460788567", "section_data_ids": "{%22company%22:1719460785%2C%22customer-type%22:1719460785%2C%22customer%22:1719460551}", "_ga_22YFFZRGG3": "GS1.1.1719460551.1.1.1719461617.60.0.0", "_ga_6G48RXXLNZ": "GS1.1.1719460551.1.1.1719461617.60.0.0", "_clsk": "pwbsfz%7C1719464976448%7C1%7C1%7Ct.clarity.ms%2Fcollect"}
            burp0_headers = {"Sec-Ch-Ua": "\"Chromium\";v=\"131\", \"Not_A Brand\";v=\"24\"", "Sec-Ch-Ua-Mobile": "?0", "Sec-Ch-Ua-Platform": "\"Windows\"", "Accept-Language": "zh-TW,zh;q=0.9", "Upgrade-Insecure-Requests": "1", "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.6778.140 Safari/537.36", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7", "Sec-Fetch-Site": "none", "Sec-Fetch-Mode": "navigate", "Sec-Fetch-User": "?1", "Sec-Fetch-Dest": "document", "Accept-Encoding": "gzip, deflate, br", "Priority": "u=0, i", "Connection": "keep-alive"}
            response = requests.get(burp0_url, headers=burp0_headers)

            soup = BeautifulSoup(response.content, "html.parser")
            
            
            
            try:
                price = json.loads(soup.select_one(".main.gtm-data-push")['data-eec-product-detail-info'])['price']
                spect_dict['Official Price'] = price
            except:
                spect_dict['Official Price'] = soup.find('meta', {'itemprop': 'price'})['content']

            
            product_soup_key = soup.select(".spec-table__th")
            product_soup_value = soup.select(".spec-table__td")
            if product_soup_key == []:
                product_soup_key = soup.select(".col.label")
                product_soup_value = soup.select(".col.data")
                

            for key, value in zip(product_soup_key, product_soup_value):
                spect_dict[key.text.strip().lower()] = value.text.strip()

            content_text = "".join([i.text.lower() for i in soup.select("p")])

            if "4g" in content_text:
                spect_dict["wwan"] = "4G"
            elif "5g" in content_text:
                spect_dict["wwan"] = "5G"
            elif "4g" and "5g" in content_text:
                spect_dict["wwan"] = "4G/5G"

            if "nfc" in content_text:
                spect_dict["nfc"] = "Yes"
            else:
                spect_dict["nfc"] = None

            if "fingerprint" in content_text:
                spect_dict["FPR"] = "Yes"
                
                
            if product['Model Name'] == '':
                try:
                    product['Model Name'] = soup.select_one(".agw-fs-display-m").text.strip()
                except:
                    product['Model Name'] = soup.select_one(".page-title").text.strip()
                

            product_detail_list.append({**product, **spect_dict})
        except:
            print("not "+product["Web Link"])
            error_link.append(product["Web Link"])

    with open(f"./{company}/{keyword}_detail_list.json", "w") as f:
        json.dump(product_detail_list, f)

    with open(f"./{company}/{keyword}_error_link_list.json", "w") as f:
        json.dump(error_link, f)

    return product_detail_list, error_link




def laptop_store(company,keyword):

    # laptop
    with open(f"./{company}/{keyword}_store_detail_list.json", "r") as f:
        product_detail_list = json.load(f)

    df_laptop = pd.DataFrame(product_detail_list)

    # Function to consolidate specified columns into a dictionary for each row
    ports_columns_list = [
        "hdmi®",
        "usb",
        "number of usb 2.0 ports",
        "number of usb 3.1 gen 2 type-c ports",
        "total number of usb ports",
        "network (rj-45)",
        "audio line in",
        "audio line out",
        "headphone jack",
        "number of hdmi® ports",
        "number of 3.2 gen 2 ports (usb type-c)",
        "number of thunderbolt™ 4 (usb 3.2) ports",
        "vga",
        "number of usb 3.1 gen 1 type-a ports",
    ]


    def consolidate_row_columns(row, columns_list):
        # 检查指定的列是否全部为NaN
        if all(pd.isna(row[col]) for col in columns_list if col in row):
            return None
        else:
            # 返回一个字典，仅包含非NaN的列名和值
            return {
                col: row[col]
                for col in columns_list
                if col in row and not pd.isna(row[col])
            }


    df_laptop["Ports & Slots"] = df_laptop.apply(
        consolidate_row_columns, axis=1, columns_list=ports_columns_list
    )
    
    # drive_columns = [col for col in df_laptop.columns if 'cam' in col.lower()]
    # print(drive_columns)
    
    cam_columns_list = [
        "webcam",
        # "front camera/webcam video resolution",
        "webcam resolution (front)",

    ]
    
    df_laptop["Camera"]  = df_laptop[cam_columns_list].apply(
        lambda x: ", ".join(x.dropna().astype(str)), axis=1
    )
    

    # df_laptop["Camera"] = (
    #     df_laptop["webcam"] + ", " + df_laptop["webcam resolution (front)"]
    # )

    display_columns_list = [
        "display screen type",
        "display screen technology",
        "screen mode",
        "backlight technology",
        "screen resolution",
    ]
    df_laptop["Display"] = df_laptop.apply(
        consolidate_row_columns, axis=1, columns_list=display_columns_list
    )
    # if 'Maximum Battery Run Time' in df_laptop.columns:
    #     df_laptop["Primary Battery"] = (
    #         df_laptop["maximum battery run time"] + "," + df_laptop["battery chemistry"]
    #     )
    # else:
    #     df_laptop["Primary Battery"] = df_laptop["battery chemistry"]
        
    # drive_columns = [col for col in df_laptop.columns if 'batter' in col.lower()]
    # print(drive_columns)
    
    battery_columns_list = [
        "maximum battery run time",
        "battery capacity",
        # "front camera/webcam video resolution",
        # "webcam resolution (front)",

    ]
    
    df_laptop["Primary Battery"]  = df_laptop[battery_columns_list].apply(
        lambda x: ", ".join(x.dropna().astype(str)), axis=1
    )
    

    df_laptop["Processor"] = df_laptop[
        [
            "processor type",
            "processor model",
            "processor speed",
            "processor speed (turbo)",
            "processor core",
        ]
    ].apply(lambda x: ", ".join(x.dropna().astype(str)), axis=1)

    df_laptop["graphics"].fillna(df_laptop["graphics controller model"], inplace=True)
    graphics_columns_list = [
        "graphics controller manufacturer",
        "graphics",
        "graphics memory capacity",
        "graphics memory technology",
        "graphics memory accessibility",
    ]
    df_laptop["Graphics Card"] = df_laptop[graphics_columns_list].apply(
        lambda x: ", ".join(x.dropna().astype(str)), axis=1
    )

    df_laptop["Hard Drive"] = df_laptop["total solid state drive capacity"]

    df_laptop["Memory"] = df_laptop["standard memory"]
        
    # memory_columns_list = [
    #     "standard memory",
    #     # "maximum memory",
    #     # "front camera/webcam video resolution",
    #     # "webcam resolution (front)",

    # ]
    
    # df_laptop["Memory"]  = df_laptop[memory_columns_list].apply(
    #     lambda x: ", ".join(x.dropna().astype(str)), axis=1
    # )
    
    # # drive_columns = [col for col in df_laptop.columns if 'memory' in col.lower()]
    # # print(drive_columns)

    df_laptop["Operating System"] = df_laptop["operating system"]

    df_laptop["Audio and Speakers"] = df_laptop.apply(
        consolidate_row_columns,
        axis=1,
        columns_list=["hd audio", "speakers", "number of speakers	speaker output mode"],
    )


    def get_inches(x):
        try:
            return re.findall(r'(\d+(?:\.\d+)?)"', x)[0]
        except:
            return None


    def inch_to_mm(inch):
        try:
            return round(float(inch) * 25.4, 2)
        except:
            return None


    df_laptop["Height(mm)"] = df_laptop["height"].apply(get_inches).apply(inch_to_mm)
    df_laptop["Width(mm)"] = df_laptop["width"].apply(get_inches).apply(inch_to_mm)
    df_laptop["Depth(mm)"] = df_laptop["depth"].apply(get_inches).apply(inch_to_mm)


    def convert_to_kg(weight_str):
        # print(weight_str)
        weight_str = str(weight_str).lower()
        # 定义正则表达式
        kg_pattern = re.compile(r"(\d+(\.\d+)?)\s*kg")
        lbs_pattern = re.compile(r"(\d+(\.\d+)?)\s*lb")
        inch_pattern = re.compile(r'(\d+(\.\d+)?)\s*"')  # 新增匹配英寸作为磅的模式
        g_pattern = re.compile(r"(\d+(\.\d+)?)\s*g")
        oz_pattern = re.compile(r"(\d+(\.\d+)?)\s*oz")

        # 匹配kg
        kg_match = kg_pattern.match(weight_str)
        if kg_match:
            return round(float(kg_match.group(1)), 2)

        # 匹配lbs和kg
        lbs_match = lbs_pattern.match(weight_str)
        if lbs_match:
            return round(float(lbs_match.group(1)) * 0.45359237, 2)

        # 匹配英寸作为lbs
        inch_match = inch_pattern.match(weight_str)
        if inch_match:
            return round(float(inch_match.group(1)) * 0.45359237, 2)  # 假设1英寸等于1磅

        # 匹配g
        g_match = g_pattern.match(weight_str)
        if g_match:
            return round(float(g_match.group(1)) * 0.001, 2)

        # 匹配oz
        oz_match = oz_pattern.match(weight_str)
        if oz_match:
            return round(float(oz_match.group(1)) * 0.02834952, 2)

        # 如果没有匹配到任何单位，返回None
        return None


    df_laptop["Weight(kg)"] = df_laptop["weight (approximate)"].apply(convert_to_kg)

    if "wwan" not in df_laptop.columns:
        df_laptop["wwan"] = None
    df_laptop["WWAN"] = df_laptop["wwan"]

    if "nfc" not in df_laptop.columns:
        df_laptop["nfc"] = None
    df_laptop["NFC"] = df_laptop["nfc"]


    def set_fpr(row):
        # 检查'fingerprint reader'字段是否为'yes'
        if row["FPR"] == "Yes":
            return "Yes"
        if str(row["fingerprint reader"]).lower() == "yes":
            return "Yes"
        # 检查'security features'字段是否包含'fingerprint'
        elif "fingerprint" in str(row["security features"]).lower():
            return "Yes"
        else:
            return None

    if "FPR" not in df_laptop.columns:
        df_laptop["FPR"] = None
    df_laptop["FPR"] = df_laptop.apply(set_fpr, axis=1)
    df_laptop["FPR_model"] = None

    df_laptop["Power Supply"] = df_laptop["maximum power supply wattage"].fillna(
            df_laptop["power supply"]
        )


    df_laptop["Brand"] = "Acer"
    
    df_laptop = df_laptop[df_laptop['Model Name'].str.contains('laptop', case=False, na=False)]
    

    # 指定要输出的字段列表
    columns_to_output = [
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
        "partnumber",
    ]
    # df_laptop = df_laptop[columns_to_output]
    
    df_laptop[columns_to_output].to_csv(
        f"./{company}/{keyword}_store.csv", encoding="utf-8-sig", index=False
    )

    df_laptop_store = df_laptop[columns_to_output]
    
    return df_laptop_store

def desktop_store(company,keyword):

    # desktop
    with open(f"./{company}/{keyword}_store_detail_list.json", "r") as f:
        product_detail_list = json.load(f)

    df_desktop = pd.DataFrame(product_detail_list)
    
    # df_desktop.to_csv('acer_desktop.csv',index=False,encoding='utf-8-sig')

    # Function to consolidate specified columns into a dictionary for each row
    ports_columns_list = [
        "number of pci slots",
        "number of pci express x1 slots",
        "number of pci express x16 slots",
        "total number of usb ports",
        "number of hdmi® ports",
        "hdmi®",
        "displayport",
        "usb",
        "number of usb 2.0 ports",
        "network (rj-45)",
        "audio line in",
        "audio line out",
        "headphone jack",
        "number of pci-x slots",
        "number of total expansion slots",
        "number of pci express slots",
        "number of hard drives",
        "number of 3.5\" bays",
        "number of usb 3.1 gen 2 type-c ports"
    ]
    def consolidate_row_columns(row, columns_list):
        # 检查指定的列是否全部为NaN
        if all(pd.isna(row[col]) for col in columns_list if col in row):
            return None
        else:
            # 返回一个字典，仅包含非NaN的列名和值
            return {
                col: row[col]
                for col in columns_list
                if col in row and not pd.isna(row[col])
            }


    df_desktop["Ports & Slots"] = df_desktop.apply(
        consolidate_row_columns, axis=1, columns_list=ports_columns_list
    )

    # df_desktop["Camera"] = (
    #     df_desktop["webcam"] + ", " + df_desktop["webcam resolution (front)"]
    # )

    # display_columns_list = [
    #     "display screen type",
    #     "display screen technology",
    #     "screen mode",
    #     "backlight technology",
    #     "screen resolution",
    #     "aspect ratio"
    # ]
    # df_desktop["Display"] = df_desktop.apply(
    #     consolidate_row_columns, axis=1, columns_list=display_columns_list
    # )
    
    display_columns_list = [
        "display screen type",
        "display screen technology",
        # "screen mode",
        # "backlight technology",
        "screen resolution",
        "Standard Refresh Rate",
        "Aspect Ratio"
        
    ]
    df_desktop["Display"] = df_desktop[display_columns_list].apply(
        lambda x: ", ".join(filter(None, x.dropna().astype(str))), axis=1
    )
    

    df_desktop["Processor"] = df_desktop[
        [
            "processor type",
            "processor model",
            "processor speed",
            "processor speed (turbo)",
            "processor core",
        ]
    ].apply(lambda x: ", ".join(x.dropna().astype(str)), axis=1)

    df_desktop["graphics"].fillna(df_desktop["graphics controller model"], inplace=True)
    graphics_columns_list = [
        "graphics controller manufacturer",
        "graphics",
        "graphics memory capacity",
        "graphics memory technology",
        "graphics memory accessibility",
    ]
    df_desktop["Graphics Card"] = df_desktop[graphics_columns_list].apply(
        lambda x: ", ".join(x.dropna().astype(str)), axis=1
    )

    df_desktop["Hard Drive"] = df_desktop["total solid state drive capacity"]

    df_desktop["Memory"] = df_desktop["standard memory"] + df_desktop["memory technology"]

    df_desktop["Operating System"] = df_desktop["operating system"]

    df_desktop["Audio and Speakers"] = df_desktop.apply(
        consolidate_row_columns,
        axis=1,
        columns_list=["hd audio", "speakers", "number of speakers	speaker output mode"],
    )


    def get_inches(x):
        try:
            return re.findall(r'(\d+(?:\.\d+)?)"', x)[0]
        except:
            return None


    def inch_to_mm(inch):
        try:
            return round(float(inch) * 25.4, 2)
        except:
            return None


    df_desktop["Height(mm)"] = df_desktop["height"].apply(get_inches).apply(inch_to_mm)
    df_desktop["Width(mm)"] = df_desktop["width"].apply(get_inches).apply(inch_to_mm)
    df_desktop["Depth(mm)"] = df_desktop["depth"].apply(get_inches).apply(inch_to_mm)


    def convert_to_kg(weight_str):
        # print(weight_str)
        weight_str = str(weight_str).lower()
        # 定义正则表达式
        kg_pattern = re.compile(r"(\d+(\.\d+)?)\s*kg")
        lbs_pattern = re.compile(r"(\d+(\.\d+)?)\s*lb")
        inch_pattern = re.compile(r'(\d+(\.\d+)?)\s*"')  # 新增匹配英寸作为磅的模式
        g_pattern = re.compile(r"(\d+(\.\d+)?)\s*g")
        oz_pattern = re.compile(r"(\d+(\.\d+)?)\s*oz")

        # 匹配kg
        kg_match = kg_pattern.match(weight_str)
        if kg_match:
            return round(float(kg_match.group(1)), 2)

        # 匹配lbs和kg
        lbs_match = lbs_pattern.match(weight_str)
        if lbs_match:
            return round(float(lbs_match.group(1)) * 0.45359237, 2)

        # 匹配英寸作为lbs
        inch_match = inch_pattern.match(weight_str)
        if inch_match:
            return round(float(inch_match.group(1)) * 0.45359237, 2)  # 假设1英寸等于1磅

        # 匹配g
        g_match = g_pattern.match(weight_str)
        if g_match:
            return round(float(g_match.group(1)) * 0.001, 2)

        # 匹配oz
        oz_match = oz_pattern.match(weight_str)
        if oz_match:
            return round(float(oz_match.group(1)) * 0.02834952, 2)

        # 如果没有匹配到任何单位，返回None
        return None


    df_desktop["Weight(kg)"] = df_desktop["weight (approximate)"].apply(convert_to_kg)




    df_desktop["Power Supply"] = df_desktop["input voltage"]


    df_desktop["Brand"] = "Acer"

    # 指定要输出的字段列表
    columns_to_output = [
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
        "partnumber",
    ]
    df_desktop[columns_to_output].to_csv(
        f"./{company}/{keyword}_store.csv", encoding="utf-8-sig", index=False
    )

    df_desktop_store = df_desktop[columns_to_output]
    
    return df_desktop_store

def docking_store(company,keyword):

    # docking
    with open(f"./{company}/{keyword}_store_detail_list.json", "r") as f:
        product_detail_list = json.load(f)

    df_docking = pd.DataFrame(product_detail_list)
    
    # df_docking.to_csv('acer_docking.csv',index=False,encoding='utf-8-sig')

    df_docking["Ports & Slots"] = df_docking["Ports & Slots"] 



    def convert_to_kg(weight_str):
        # print(weight_str)
        weight_str = str(weight_str).lower()
        # 定义正则表达式
        kg_pattern = re.compile(r"(\d+(\.\d+)?)\s*kg")
        lbs_pattern = re.compile(r"(\d+(\.\d+)?)\s*lb")
        inch_pattern = re.compile(r'(\d+(\.\d+)?)\s*"')  # 新增匹配英寸作为磅的模式
        g_pattern = re.compile(r"(\d+(\.\d+)?)\s*g")
        oz_pattern = re.compile(r"(\d+(\.\d+)?)\s*oz")

        # 匹配kg
        kg_match = kg_pattern.match(weight_str)
        if kg_match:
            return round(float(kg_match.group(1)), 2)

        # 匹配lbs和kg
        lbs_match = lbs_pattern.match(weight_str)
        if lbs_match:
            return round(float(lbs_match.group(1)) * 0.45359237, 2)

        # 匹配英寸作为lbs
        inch_match = inch_pattern.match(weight_str)
        if inch_match:
            return round(float(inch_match.group(1)) * 0.45359237, 2)  # 假设1英寸等于1磅

        # 匹配g
        g_match = g_pattern.match(weight_str)
        if g_match:
            return round(float(g_match.group(1)) * 0.001, 2)

        # 匹配oz
        oz_match = oz_pattern.match(weight_str)
        if oz_match:
            return round(float(oz_match.group(1)) * 0.02834952, 2)

        # 如果没有匹配到任何单位，返回None
        return None


    df_docking["Weight(kg)"] = df_docking["weight (approximate)"].apply(convert_to_kg)




    df_docking["Power Supply"] = df_docking['input voltage']


    df_docking["Brand"] = "Acer"

    # 指定要输出的字段列表
    columns_to_output = [
        "Brand",
        "Model Name",
        "Official Price",
        "Ports & Slots",
        "Weight(kg)",
        "Power Supply",
        "Web Link",
        "partnumber",
    ]
    df_docking[columns_to_output].to_csv(
        f"./{company}/{keyword}_store.csv", encoding="utf-8-sig", index=False
    )

    df_docking_store = df_docking[columns_to_output]
    
    return df_docking_store



# df_laptop.to_csv(f'./{company}/{keyword}_detail_list.csv',index=False,encoding = 'utf-8-sig')

def laptop_official(company,keyword):
    # laptop
    with open(f"./{company}/{keyword}_detail_list.json", "r") as f:
        product_detail_list = json.load(f)

    df_laptop = pd.DataFrame(product_detail_list)

    # Function to consolidate specified columns into a dictionary for each row
    ports_columns_list = [
        "hdmi®",
        "usb",
        "number of usb 2.0 ports",
        "number of usb 3.1 gen 2 type-c ports",
        "total number of usb ports",
        "network (rj-45)",
        "audio line in",
        "audio line out",
        "headphone jack",
        "number of hdmi® ports",
        "number of 3.2 gen 2 ports (usb type-c)",
        "number of thunderbolt™ 4 (usb 3.2) ports",
        "vga",
        "number of usb 3.1 gen 1 type-a ports",
    ]


    def consolidate_row_columns(row, columns_list):
        # 检查指定的列是否全部为NaN
        if all(pd.isna(row[col]) for col in columns_list if col in row):
            return None
        else:
            # 返回一个字典，仅包含非NaN的列名和值
            return {
                col: row[col]
                for col in columns_list
                if col in row and not pd.isna(row[col])
            }


    df_laptop["Ports & Slots"] = df_laptop.apply(
        consolidate_row_columns, axis=1, columns_list=ports_columns_list
    )

    # df_laptop['Camera'] = df_laptop['webcam']+', '+ df_laptop['webcam resolution (front)']
    df_laptop["Camera"] = None
    
    cam_columns_list = [
        "webcam",
        # "front camera/webcam video resolution",
        "webcam resolution (front)",

    ]
    
    df_laptop["Camera"]  = df_laptop[cam_columns_list].apply(
        lambda x: ", ".join(x.dropna().astype(str)), axis=1
    )

    # display_columns_list = [
    #     "display screen type",
    #     "display screen technology",
    #     "screen mode",
    #     "backlight technology",
    #     "screen resolution",
    # ]
    # df_laptop["Display"] = df_laptop.apply(
    #     consolidate_row_columns, axis=1, columns_list=display_columns_list
    # )
    
    display_columns_list = [
        "display screen type",
        "display screen technology",
        # "screen mode",
        # "backlight technology",
        "screen resolution",
        "Standard Refresh Rate",
        "Aspect Ratio"
        
    ]
    df_laptop["Display"] = df_laptop[display_columns_list].apply(
        lambda x: ", ".join(filter(None, x.dropna().astype(str))), axis=1
    )
    

    # df_laptop["Primary Battery"] = (
    #     df_laptop["maximum battery run time"] + "," + df_laptop["battery chemistry"]+ "," + df_laptop["battery energy"]
    # )
    battery_columns_list = [
        "maximum battery run time",
        "battery chemistry",
        "battery energy",
    ]
    df_laptop["Primary Battery"] = df_laptop[battery_columns_list].apply(
        lambda x: ", ".join(x.dropna().astype(str)), axis=1
    )
    
    # drive_columns = [col for col in df_laptop.columns if 'battery' in col.lower()]
    # print(drive_columns)


    df_laptop["Processor"] = df_laptop[
        [
            "processor type",
            "processor model",
            "processor generation",
            "processor speed",
            "processor core",
        ]
    ].apply(lambda x: ", ".join(x.dropna().astype(str)), axis=1)


    graphics_columns_list = [
        "graphics controller manufacturer",
        "graphics controller model",
        "graphics memory capacity",
        "graphics memory technology",
        "graphics memory accessibility",
    ]
    df_laptop["Graphics Card"] = df_laptop[graphics_columns_list].apply(
        lambda x: ", ".join(x.dropna().astype(str)), axis=1
    )
    # drive_columns = [col for col in df_laptop.columns if 'graphics' in col.lower()]
    # print(drive_columns)

    # df_laptop["Hard Drive"] = df_laptop["total solid state drive capacity"] +df_laptop['flash memory capacity']
    
    drive_columns_list = [
        "total solid state drive capacity",
        "flash memory capacity",

    ]
    
    df_laptop["Hard Drive"]  = df_laptop[drive_columns_list].apply(
        lambda x: ", ".join(x.dropna().astype(str)), axis=1
    )
    
    # df_laptop["Memory"] = (
    #     df_laptop["total installed system memory"] + df_laptop["system memory technology"]
    # )
    
    memory_columns_list = [
        "total installed system memory",
        "system memory technology",
        "standard memory",
    ]
    
    df_laptop["Memory"]  = df_laptop[memory_columns_list].apply(
        lambda x: ", ".join(x.dropna().astype(str)), axis=1
    )
    # drive_columns = [col for col in df_laptop.columns if 'memory' in col.lower()]
    # print(drive_columns)
    

    df_laptop["Operating System"] = df_laptop["operating system"]

    df_laptop["Audio and Speakers"] = df_laptop.apply(
        consolidate_row_columns,
        axis=1,
        columns_list=["hd audio", "speakers", "number of speakers	speaker output mode"],
    )


    def get_inches(x):
        try:
            return re.findall(r'(\d+(?:\.\d+)?)"', x)[0]
        except:
            return None


    def inch_to_mm(inch):
        try:
            return round(float(inch) * 25.4, 2)
        except:
            return None


    df_laptop["Height(mm)"] = df_laptop["height"].apply(get_inches).apply(inch_to_mm)
    df_laptop["Width(mm)"] = df_laptop["width"].apply(get_inches).apply(inch_to_mm)
    df_laptop["Depth(mm)"] = df_laptop["depth"].apply(get_inches).apply(inch_to_mm)


    def convert_to_kg(weight_str):
        # print(weight_str)
        weight_str = str(weight_str).lower()
        # 定义正则表达式
        kg_pattern = re.compile(r"(\d+(\.\d+)?)\s*kg")
        lbs_pattern = re.compile(r"(\d+(\.\d+)?)\s*lb")
        inch_pattern = re.compile(r'(\d+(\.\d+)?)\s*"')  # 新增匹配英寸作为磅的模式
        g_pattern = re.compile(r"(\d+(\.\d+)?)\s*g")
        oz_pattern = re.compile(r"(\d+(\.\d+)?)\s*oz")

        # 匹配kg
        kg_match = kg_pattern.match(weight_str)
        if kg_match:
            return round(float(kg_match.group(1)), 2)

        # 匹配lbs和kg
        lbs_match = lbs_pattern.match(weight_str)
        if lbs_match:
            return round(float(lbs_match.group(1)) * 0.45359237, 2)

        # 匹配英寸作为lbs
        inch_match = inch_pattern.match(weight_str)
        if inch_match:
            return round(float(inch_match.group(1)) * 0.45359237, 2)  # 假设1英寸等于1磅

        # 匹配g
        g_match = g_pattern.match(weight_str)
        if g_match:
            return round(float(g_match.group(1)) * 0.001, 2)

        # 匹配oz
        oz_match = oz_pattern.match(weight_str)
        if oz_match:
            return round(float(oz_match.group(1)) * 0.02834952, 2)

        # 如果没有匹配到任何单位，返回None
        return None


    df_laptop["Weight(kg)"] = df_laptop["weight (approximate)"].apply(convert_to_kg)

    if "wwan" not in df_laptop.columns:
        df_laptop["WWAN"] = None
    else:
        df_laptop["WWAN"] = df_laptop["wwan"]

    df_laptop["NFC"] = df_laptop["nfc"]


    def set_fpr(row):
        # 检查'fingerprint reader'字段是否为'yes'
        if row["FPR"] == "Yes":
            return "Yes"
        if str(row["finger print reader"]).lower() == "yes":
            return "Yes"
        # 检查'security features'字段是否包含'fingerprint'
        elif "fingerprint" in str(row["security features"]).lower():
            return "Yes"
        else:
            return None


    df_laptop["FPR"] = df_laptop.apply(set_fpr, axis=1)
    df_laptop["FPR_model"] = None

    df_laptop["Power Supply"] = df_laptop["maximum power supply wattage"]
    df_laptop["Brand"] = "Acer"

    # 指定要输出的字段列表
    columns_to_output = [
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
        "partnumber",
    ]
    df_laptop[columns_to_output].to_csv(
        f"./{company}/{keyword}_official.csv", encoding="utf-8-sig", index=False
    )

    df_laptop_official = df_laptop[columns_to_output]
    return df_laptop_official


def desktop_official(company,keyword):
    # desktop
    with open(f"./{company}/{keyword}_detail_list.json", "r") as f:
        product_detail_list = json.load(f)

    df_desktop = pd.DataFrame(product_detail_list)
    
    # df_desktop.to_csv(f'./{company}/{keyword}_detail_list.csv',index=False,encoding = 'utf-8-sig')

    # Function to consolidate specified columns into a dictionary for each row
    ports_columns_list = [
        "hdmi",
        "displayport",
        "number of usb 2.0 ports",
        "number of usb 3.2 gen 1 type-a ports",
        "number of usb 3.2 gen 2 type-a ports",
        "number of usb 3.2 gen 2 type-c ports",
        "usb type-c",
        "number of usb 3.2 gen 2x2 type-c ports",
        "total number of usb ports",
        "network (rj-45)",
        "audio line in",
        "audio line out",
        "number of total expansion slots",
        "number of pci express x1 slots",
        "number of pci express x16 slots",
        "number of m.2 interfaces",
        "number of hdmi outputs",
        "number of usb 3.2 gen 1 type-c ports",
        "dvi-d",
        "vga",
        "number of pci slots",
        "number of pci express x4 slots",
        "number of pci express x8 slots",
        "number of displayport outputs"
    ]


    def consolidate_row_columns(row, columns_list):
        # 检查指定的列是否全部为NaN
        if all(pd.isna(row[col]) for col in columns_list if col in row):
            return None
        else:
            # 返回一个字典，仅包含非NaN的列名和值
            return {
                col: row[col]
                for col in columns_list
                if col in row and not pd.isna(row[col])
            }


    df_desktop["Ports & Slots"] = df_desktop.apply(
        consolidate_row_columns, axis=1, columns_list=ports_columns_list
    )

    # df_desktop['Camera'] = df_desktop['webcam']+', '+ df_desktop['webcam resolution (front)']

    # display_columns_list = [
    #     "display screen type",
    #     "display screen technology",
    #     "screen mode",
    #     "backlight technology",
    #     "screen resolution",
    # ]
    # df_desktop["Display"] = df_desktop.apply(
    #     consolidate_row_columns, axis=1, columns_list=display_columns_list
    # )
    
    display_columns_list = [
        "display screen type",
        "display screen technology",
        # "screen mode",
        # "backlight technology",
        "screen resolution",
        "Standard Refresh Rate",
        "Aspect Ratio"
        
    ]
    df_desktop["Display"] = df_desktop[display_columns_list].apply(
        lambda x: ", ".join(filter(None, x.dropna().astype(str))), axis=1
    )
    


    df_desktop["Processor"] = df_desktop[
       [
        "processor manufacturer",
        "processor type",
        "processor model",
        "processor speed",
        "processor core"
    ]
    ].apply(lambda x: ", ".join(x.dropna().astype(str)), axis=1)


    graphics_columns_list = [
        "graphics controller manufacturer",
        "graphics controller model",
        "graphics memory capacity",
        "graphics memory technology",
        "graphics memory accessibility",
    ]
    df_desktop["Graphics Card"] = df_desktop[graphics_columns_list].apply(
        lambda x: ", ".join(x.dropna().astype(str)), axis=1
    )

    # df_desktop["Hard Drive"] = df_desktop["total solid state drive capacity"]
    
    drive_columns_list = [
        "total solid state drive capacity",
        "flash memory capacity",
        "total solid state drive capacity",

    ]
    
    df_desktop["Hard Drive"]  = df_desktop[drive_columns_list].apply(
        lambda x: ", ".join(x.dropna().astype(str)), axis=1
    )
    

    # df_desktop["Memory"] = (
    #     df_desktop["standard memory"] 
    # )
    
    memory_columns_list = [
        "total installed system memory",
        "system memory technology",
        "standard memory",
    ]
    
    df_desktop["Memory"]  = df_desktop[memory_columns_list].apply(
        lambda x: ", ".join(x.dropna().astype(str)), axis=1
    )
    

    df_desktop["Operating System"] = df_desktop["operating system"]

    df_desktop["Audio and Speakers"] = df_desktop.apply(
        consolidate_row_columns,
        axis=1,
        columns_list=["hd audio", "speakers", "number of speakers	speaker output mode"],
    )


    def get_inches(x):
        try:
            return re.findall(r'(\d+(?:\.\d+)?)"', x)[0]
        except:
            return None


    def inch_to_mm(inch):
        try:
            return round(float(inch) * 25.4, 2)
        except:
            return None


    df_desktop["Height(mm)"] = df_desktop["height"].apply(get_inches).apply(inch_to_mm)
    df_desktop["Width(mm)"] = df_desktop["width"].apply(get_inches).apply(inch_to_mm)
    df_desktop["Depth(mm)"] = df_desktop["depth"].apply(get_inches).apply(inch_to_mm)


    def convert_to_kg(weight_str):
        # print(weight_str)
        weight_str = str(weight_str).lower()
        # 定义正则表达式
        kg_pattern = re.compile(r"(\d+(\.\d+)?)\s*kg")
        lbs_pattern = re.compile(r"(\d+(\.\d+)?)\s*lb")
        inch_pattern = re.compile(r'(\d+(\.\d+)?)\s*"')  # 新增匹配英寸作为磅的模式
        g_pattern = re.compile(r"(\d+(\.\d+)?)\s*g")
        oz_pattern = re.compile(r"(\d+(\.\d+)?)\s*oz")

        # 匹配kg
        kg_match = kg_pattern.match(weight_str)
        if kg_match:
            return round(float(kg_match.group(1)), 2)

        # 匹配lbs和kg
        lbs_match = lbs_pattern.match(weight_str)
        if lbs_match:
            return round(float(lbs_match.group(1)) * 0.45359237, 2)

        # 匹配英寸作为lbs
        inch_match = inch_pattern.match(weight_str)
        if inch_match:
            return round(float(inch_match.group(1)) * 0.45359237, 2)  # 假设1英寸等于1磅

        # 匹配g
        g_match = g_pattern.match(weight_str)
        if g_match:
            return round(float(g_match.group(1)) * 0.001, 2)

        # 匹配oz
        oz_match = oz_pattern.match(weight_str)
        if oz_match:
            return round(float(oz_match.group(1)) * 0.02834952, 2)

        # 如果没有匹配到任何单位，返回None
        return None


    df_desktop["Weight(kg)"] = df_desktop["weight (approximate)"].apply(convert_to_kg)




    df_desktop["Power Supply"] = df_desktop["maximum power supply wattage"]
    df_desktop["Brand"] = "Acer"

    # 指定要输出的字段列表
    columns_to_output = [
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
        "partnumber",
    ]
    df_desktop[columns_to_output].to_csv(
        f"./{company}/{keyword}_official.csv", encoding="utf-8-sig", index=False
    )

    df_desktop_official = df_desktop[columns_to_output]
    return df_desktop_official

def docking_official(company,keyword):
    # docking
    with open(f"./{company}/{keyword}_detail_list.json", "r") as f:
        product_detail_list = json.load(f)

    df_docking = pd.DataFrame(product_detail_list)
    
    # df_docking.to_csv('acer_docking.csv',index=False,encoding='utf-8-sig')

    ports_columns_list = [
        "hdmi",
        "displayport",
        "number of usb 2.0 ports",
        "number of usb 3.2 gen 1 type-a ports",
        "number of usb 3.2 gen 2 type-a ports",
        "number of usb 3.2 gen 2 type-c ports",
        "usb type-c",
        "number of usb 3.2 gen 2x2 type-c ports",
        "total number of usb ports",
        "network (rj-45)",
        "audio line in",
        "audio line out",
        "number of total expansion slots",
        "number of pci express x1 slots",
        "number of pci express x16 slots",
        "number of m.2 interfaces",
        "number of hdmi outputs",
        "number of usb 3.2 gen 1 type-c ports",
        "dvi-d",
        "vga",
        "number of pci slots",
        "number of pci express x4 slots",
        "number of pci express x8 slots",
        "number of displayport outputs"
    ]


    def consolidate_row_columns(row, columns_list):
        # 检查指定的列是否全部为NaN
        if all(pd.isna(row[col]) for col in columns_list if col in row):
            return None
        else:
            # 返回一个字典，仅包含非NaN的列名和值
            return {
                col: row[col]
                for col in columns_list
                if col in row and not pd.isna(row[col])
            }


    df_docking["Ports & Slots"] = df_docking.apply(
        consolidate_row_columns, axis=1, columns_list=ports_columns_list
    )


    def convert_to_kg(weight_str):
        # print(weight_str)
        weight_str = str(weight_str).lower()
        # 定义正则表达式
        kg_pattern = re.compile(r"(\d+(\.\d+)?)\s*kg")
        lbs_pattern = re.compile(r"(\d+(\.\d+)?)\s*lb")
        inch_pattern = re.compile(r'(\d+(\.\d+)?)\s*"')  # 新增匹配英寸作为磅的模式
        g_pattern = re.compile(r"(\d+(\.\d+)?)\s*g")
        oz_pattern = re.compile(r"(\d+(\.\d+)?)\s*oz")

        # 匹配kg
        kg_match = kg_pattern.match(weight_str)
        if kg_match:
            return round(float(kg_match.group(1)), 2)

        # 匹配lbs和kg
        lbs_match = lbs_pattern.match(weight_str)
        if lbs_match:
            return round(float(lbs_match.group(1)) * 0.45359237, 2)

        # 匹配英寸作为lbs
        inch_match = inch_pattern.match(weight_str)
        if inch_match:
            return round(float(inch_match.group(1)) * 0.45359237, 2)  # 假设1英寸等于1磅

        # 匹配g
        g_match = g_pattern.match(weight_str)
        if g_match:
            return round(float(g_match.group(1)) * 0.001, 2)

        # 匹配oz
        oz_match = oz_pattern.match(weight_str)
        if oz_match:
            return round(float(oz_match.group(1)) * 0.02834952, 2)

        # 如果没有匹配到任何单位，返回None
        return None


    df_docking["Weight(kg)"] = df_docking["weight (approximate)"].apply(convert_to_kg)

    df_docking["Power Supply"] = df_docking['input voltage']

    df_docking["Brand"] = "Acer"

    # 指定要输出的字段列表
    columns_to_output = [
        "Brand",
        "Model Name",
        "Official Price",
        "Ports & Slots",
        "Weight(kg)",
        "Power Supply",
        "Web Link",
        "partnumber",
    ]
    df_docking[columns_to_output].to_csv(
        f"./{company}/{keyword}_official.csv", encoding="utf-8-sig", index=False
    )

    df_docking_official = df_docking[columns_to_output]
    
    return df_docking_official


def merge(df_official,df_store,keyword,company,columns_to_output):
    # 根据partnumber进行外连接合并
    df_merged = pd.merge(df_official, df_store, on='partnumber', how='outer', suffixes=('_official', '_store'))

    # 获取所有列名
    columns = list(df_official.columns)
    columns.remove('partnumber')

    def is_emty_use_store(x,column):
        if x[f"{column}_official"] is None or pd.isna(x[f"{column}_official"]):
            return x[f"{column}_store"]
        else:
            return x[f"{column}_official"]
        

    # 处理重复的列
    for column in columns:
        # column = columns[1]
        df_merged[column] = df_merged.apply(
                    lambda row: is_emty_use_store(row,column), axis=1)
    
    df_merged[columns_to_output].to_csv(f"./{company}/{keyword}.csv", encoding="utf-8-sig", index=False)
    
    return df_merged[columns_to_output]

def merge_docking(df_store,keyword,company,columns_to_output):
    # 根据partnumber进行外连接合并
    # df_merged = pd.merge(df_official, df_store, on='partnumber', how='outer', suffixes=('_official', '_store'))

    # 获取所有列名
    columns = list(df_store.columns)
    columns.remove('partnumber')

    # def is_emty_use_store(x,column):
    #     if x[f"{column}_official"] is None or pd.isna(x[f"{column}_official"]):
    #         return x[f"{column}_store"]
    #     else:
    #         return x[f"{column}_official"]
        

    # # 处理重复的列
    # for column in columns:
    #     # column = columns[1]
    #     df_store[column] = df_store.apply(
    #                 lambda row: is_emty_use_store(row,column), axis=1)
    
    df_store[columns_to_output].to_csv(f"./{company}/{keyword}.csv", encoding="utf-8-sig", index=False)
    
    return df_store[columns_to_output]

keyword_list = ["laptop", "desktop", "docking"]
company = "Acer"

for keyword in keyword_list:
    # keyword = keyword_list[2]

    products_store_list = search_crawl_store(keyword)
    product_detail_store_list, error_store_link = detail_crawl_store(keyword, company)
    
    products_list = search_crawl(keyword)
    product_detail_list, error_link = detail_crawl(keyword, company)

    if keyword == 'laptop':
        df_store = laptop_store(company,keyword)
        df_official = laptop_official(company,keyword)
        columns_to_output = [
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
        df = merge(df_official,df_store,keyword,company,columns_to_output)
        df.to_csv(f"./{company}/{keyword}.csv", encoding="utf-8-sig", index=False)
    
    elif keyword == 'desktop':
        df_desktop_store = desktop_store(company,keyword)
        df_desktop_official = desktop_official(company,keyword)
        columns_to_output = [
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
        df = merge(df_desktop_store,df_desktop_official,keyword,company,columns_to_output)
        df.to_csv(f"./{company}/{keyword}.csv", encoding="utf-8-sig", index=False)
                 
    elif keyword == 'docking':
        df_docking_store = docking_store(company,keyword)
        df_docking_official = docking_official(company,keyword)
        columns_to_output = [
            "Brand",
            "Model Name",
            "Official Price",
            "Ports & Slots",
            "Weight(kg)",
            "Power Supply",
            "Web Link",
        ]
        df = merge_docking(df_docking_store,keyword,company,columns_to_output)
        df = df[columns_to_output]
        df.to_csv(f"./{company}/{keyword}.csv", encoding="utf-8-sig", index=False)
