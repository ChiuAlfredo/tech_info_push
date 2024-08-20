import requests
import re
import json
from bs4 import BeautifulSoup
from tqdm import tqdm
import pandas as pd
from requests.exceptions import TooManyRedirects



def search_crawl(keyword, company):
    number_count = 0
    number_on_page = 12
    page = 1
    products_list = []

    while True:
        burp0_url = f"https://www.dell.com:443/en-us/search/{keyword}?p={page}&r=36679&t={keyword}&t=Product"
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
        response = requests.get(burp0_url, headers=burp0_headers)
        soup = BeautifulSoup(response.content, "html.parser")

        total_page = int(
            soup.find("div", attrs={"data-result-count": True})["data-result-count"]
        )

        articles = soup.select(".dell-ps.ps>article")

        for article in articles:
            # article = articles[0]
            # 將HTML實體轉換為普通字符

            title = article.select_one(".ps-title").get_text(strip=True)
            web_link = "https:" + article.select_one(".ps-title>a")["href"]
            price = article.select_one(".ps-dell-price.ps-simplified").get_text(
                strip=True
            )
            products_list.append(
                {"Model Name": title, "Web Link": web_link, "Official Price": price}
            )

            print(title)

        number_count += number_on_page

        if number_count >= total_page:
            break
        print(f"Page: {page}")
        # print(products_list)

        page += 1

    with open(f"./data/{company}/{keyword}_search.json", "w") as f:
        json.dump(products_list, f)

    return products_list


def detail_crawl(keyword, company):
    with open(f"./data/{company}/{keyword}_search.json", "r") as f:
        products_list = json.load(f)

    product_detail_list = []
    error_link = []
    for product in tqdm(products_list):
        # product = products_list[404]
        try:
            # burp0_url = 'https://www.dell.com/en-us/shop/dell-computer-laptops/mobile-precision-5690-ai-ready/spd/precision-16-5690-laptop/xctop5690usaivp'
            burp0_url = product["Web Link"]

            # burp0_cookies = {"search-visitorId": "fa91cb13-eefa-4498-af12-3da6919d5160", "akGD": "%7B%22country%22%3A%22TW%22%2C%22region%22%3A%22%22%7D", "s_ecid": "MCMID%7C05594863603858791913966452533384812014", "AMCV_4DD80861515CAB990A490D45%40AdobeOrg": "179643557%7CMCIDTS%7C19916%7CMCMID%7C05594863603858791913966452533384812014%7CMCAID%7CNONE%7CMCOPTOUT-1720686051s%7CNONE%7CvVersion%7C5.5.0", "lwp": "c=us&l=en&s=bsd&cs=04", "__privaci_cookie_consent_uuid": "f07ce1a7-c924-44fc-90dc-b2b5ebed872b:46", "__privaci_cookie_consent_generated": "f07ce1a7-c924-44fc-90dc-b2b5ebed872b:46", "_gcl_au": "1.1.1678367427.1720678865", "d_vi": "848a45cbb45a0300d0798f662600000023010000", "_cls_v": "9dc90fc3-cbe6-42d5-9542-c7a2df6a2cf6", "_ga": "GA1.1.1795885693.1720678865", "ajs_anonymous_id": "023e8c65-3bbf-4224-bdaa-323eed962092", "_cs_c": "0", "_fbp": "fb.1.1720678865737.353943247", "FPID": "FPID2.2.b1WEQc6AyZu2v%2FWqvf%2BaIOi88m1Jllk49mo8i5jMQ8c%3D.1720678865", "FPAU": "1.1.1678367427.1720678865", "_scid": "f94d06f3-93c1-4bb2-bbb9-8b5ed088a785", "_gd_visitor": "1a3db6f0-2c82-4a4b-8857-38041b965e6e", "_sctr": "1%7C1720627200000", "_evga_b184": "{%22uuid%22:%220bf99460a2cca1a8%22}", "_sfid_c405": "{%22anonymousId%22:%220bf99460a2cca1a8%22%2C%22consents%22:[]}", "_fbp": "fb.1.1720678865737.353943247", "_tt_enable_cookie": "1", "_ttp": "rwG7PC8y1a_ZaSYIm0cIeWWELW8", "_pin_unauth": "dWlkPU5HUXhPR05rWW1FdFlqZzRZeTAwTUdOaExXRmhNemt0TVRjMU1XVTRaVFZqTWpCbA", "__qca": "P0-557024765-1720685693346", "s_vnc365": "1752287676089%26vn%3D3", "mbox": "PC#81a2e7edaca34af1838859a74a05ec00.32_0#1783996481|session#3108bd02081b4c0aaa3bc521b0eadea5#1720753541", "adcloud": "{%22_les_v%22:%22y%2Cdell.com%2C1720753480%22}", "_rdt_uuid": "1720685694616.e8c35a74-6347-4f53-80a5-b5c301820c60", "_uetvid": "a72e9a603f5d11ef9e9f83c81ad3cedd", "_scid_r": "f94d06f3-93c1-4bb2-bbb9-8b5ed088a785", "BVBRANDID": "b50f55fd-fa93-44e7-ae4d-faac503eb833", "p13np": "dhs", "_abck": "115AC061C9005533F55227986749F8A0~0~YAAQxONH0iWOfquQAQAAMqjPsAwl55mGitTzibc6hcli5BvO7ploBgxMZkPOG1PERJeVs9n96FUuC4GZdWydCOcRxvdFfaaFObASuLtqp1K5Jb3mLXeotvYAslJ8FFKzKcqytBsIzz0appbH7lClj2NKosUQ5F2FPotVzN04YEG2DN+gR/JpT5N3pXRYSAlbK33gRL+mnSztcCk2+gscxcDl2vjmgUil8uskBMPI0+5d0haYi4u7UYWkt5yX5AFpKg/BcEXnHHJZS1WyI+mcw0aCKEeVOyvqRWV4lbgaHBv/WJT62tM/iPL3xq+KRfQsfppAd6Pp5cRoTgEjR9Aw/qgF9O1NNucGFSF5iO40GtQj8psGr3XS5q5+Lw0Qo2xjO7+nCRB4raKRO7VjyPuNCkhJhVnPcg==~-1~-1~1720953316", "_cs_id": "4dffab88-9eaa-ae95-ed72-c334bacc6de1.1720678869.4.1720953753.1720953753.1709063960.1754842869031.1", "_ga_1234567890": "GS1.1.1720953754.4.0.1720953754.0.0.1388017742", "_ga_16419196": "GS1.1.1720953754.4.0.1720953754.0.0.0", "_ga_16418520": "GS1.1.1720953754.4.0.1720953754.0.0.0"}
            # burp0_headers = {"Dpr": "1", "Sec-Ch-Dpr": "1", "Viewport-Width": "1600", "Sec-Ch-Viewport-Width": "1600", "Sec-Ch-Ua": "\"Chromium\";v=\"127\", \"Not)A;Brand\";v=\"99\"", "Sec-Ch-Ua-Mobile": "?0", "Sec-Ch-Ua-Platform": "\"Windows\"", "Accept-Language": "zh-TW", "Upgrade-Insecure-Requests": "1", "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.6533.100 Safari/537.36", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7", "Sec-Fetch-Site": "none", "Sec-Fetch-Mode": "navigate", "Sec-Fetch-User": "?1", "Sec-Fetch-Dest": "document", "Accept-Encoding": "gzip, deflate, br", "Priority": "u=0, i", "Connection": "keep-alive"}

            response = requests.get(burp0_url)
            soup = BeautifulSoup(response.content, "html.parser")
            

            if 'spd' in burp0_url:
                product_soup = soup.select("li.mb-2")

                spect_dict = {}
                for i in product_soup:
                    # i = product_soup[0]
                    spect_dict[i.select_one("div").get_text(strip=True).lower()] = i.select_one(
                        "p"
                    ).get_text(strip=True)
                
            elif 'apd' in burp0_url:
                product_soup = soup.select(".spec__main_wrapper")
                spect_dict = {}
                for i in product_soup:
                    # i  = product_soup[0]
                    spect_dict[i.select_one('.spec__child__heading').get_text(strip=True).lower()] = ',\n'.join([i.get_text(strip=True) for i in i.select('.spec__item')])
            else:
                error_link.append(**product)
                
            if spect_dict == {}:
                ports_and_slots_element = soup.select_one('[data-title="Ports & Slots"]')
                if ports_and_slots_element:
                    spect_dict[ports_and_slots_element.get('data-title').lower()] = BeautifulSoup(ports_and_slots_element.get('data-description'), 'html.parser').get_text(separator=';', strip=True).replace('\xa0', ' ')
                error_link.append({**product,**spect_dict})
            else:
                if 'spd' in burp0_url:
                    content_text = "".join([i.text.lower() for i in soup.select("p")])
                    re.findall(r"4g(?!b|hz)", content_text)
                    if re.findall(r"4g(?!b|hz)", content_text):
                        spect_dict["wwan"] = "4G"
                    elif re.findall(r"5g(?!b|hz)", content_text):
                        spect_dict["wwan"] = "5G"
                    elif re.findall(r"5g(?!b|hz)", content_text) and re.findall(
                        r"4g(?!b|hz)", content_text
                    ):
                        spect_dict["wwan"] = "4G/5G"
                    if "nfc" in content_text:
                        spect_dict["nfc"] = "Yes"
                    else:
                        spect_dict["nfc"] = None

                    if "finger" in content_text:
                        spect_dict["FPR"] = "Yes"
                product_detail_list.append({**product, **spect_dict})
        except TooManyRedirects as e:
            # logging.error("Too many redirects: %s", e)
            error_link.append(product)
        except Exception as e:
            print(e)
            error_link.append(product)

    with open(f"./data/{company}/{keyword}_detail_list.json", "w") as f:
        json.dump(product_detail_list, f)

    with open(f"./data/{company}/{keyword}_more_list.json", "w") as f:
        json.dump(error_link, f)

    return product_detail_list


def detail_crawl_more(keyword, company):
    with open(f"./data/{company}/{keyword}_more_list.json", "r") as f:
        error_link_previous = json.load(f)

    with open(f"./data/{company}/{keyword}_detail_list.json", "r") as f:
        product_detail_list = json.load(f)

    error_link = []
    for error_product in tqdm(error_link_previous):
        # error_product = error_link_previous[59]
        try:
            link = error_product["Web Link"]

            # link = 'https://www.dell.com/en-us/shop/desktop-computers/xps-desktop/spd/xps-8960-desktop/usexpsthcto8960rpl27'
            # https://www.dell.com/en-us/shop/pdr/latitude-15-5550-laptop/gctol5550usvp?selectionState=&cartItemId=
            # https://www.dell.com/en-us/shop/dell-computer-laptops/latitude-5550-laptop/spd/latitude-15-5550-laptop/gctol5550usvp?redirectTo=SOC

            new_link = (
                "https://www.dell.com/en-us/shop/pdr"
                + link.split("/spd", 1)[1]
                + "?selectionState=&cartItemId="
            )


            response = requests.get(
                new_link
            )
            soup = BeautifulSoup(response.content, "html.parser")

            # 找到表格
            rows_soup = soup.select("th.hidden-print")

            spect_dict = {}
            for row in rows_soup:
                # row = rows_soup[0]
                key = row.find("h5").get_text(strip=True).replace(":", "").lower()
                value = row.find("div", class_="mobile-title").get_text(strip=True)

                spect_dict[key] = value
                
            
            # 尺寸
            burp0_url = f"https://www.dell.com:443/csbapi/contentwebparts/us/en/bsd/04/{link.split('/')[-2]}"
            
            burp0_cookies = {
                "search-visitorId": "fa91cb13-eefa-4498-af12-3da6919d5160",
                "akGD": "%7B%22country%22%3A%22TW%22%2C%22region%22%3A%22%22%7D",
                "akaas_dell_com_product_search_us": "1723270848~rv=46~id=4661a4adb5bb115d4df78c599b5929bd",
                "s_ecid": "MCMID%7C05594863603858791913966452533384812014",
                "txUid": "CraxQWaPecG1L7VKRsh4Ag==",
                "AMCV_4DD80861515CAB990A490D45%40AdobeOrg": "179643557%7CMCIDTS%7C19916%7CMCMID%7C05594863603858791913966452533384812014%7CMCAID%7CNONE%7CMCOPTOUT-1720686051s%7CNONE%7CvVersion%7C5.5.0",
                "lwp": "c=us&l=en&s=bsd&cs=04",
                "__privaci_cookie_consent_uuid": "f07ce1a7-c924-44fc-90dc-b2b5ebed872b:46",
                "__privaci_cookie_consent_generated": "f07ce1a7-c924-44fc-90dc-b2b5ebed872b:46",
                "_gcl_au": "1.1.1678367427.1720678865",
                "d_vi": "848a45cbb45a0300d0798f662600000023010000",
                "dell_consent_map": "139%7C140",
                "_cls_v": "9dc90fc3-cbe6-42d5-9542-c7a2df6a2cf6",
                "_ga": "GA1.1.1795885693.1720678865",
                "ajs_anonymous_id": "023e8c65-3bbf-4224-bdaa-323eed962092",
                "_cs_c": "0",
                "_fbp": "fb.1.1720678865737.353943247",
                "FPID": "FPID2.2.b1WEQc6AyZu2v%2FWqvf%2BaIOi88m1Jllk49mo8i5jMQ8c%3D.1720678865",
                "FPAU": "1.1.1678367427.1720678865",
                "_scid": "f94d06f3-93c1-4bb2-bbb9-8b5ed088a785",
                "_an_uid": "4436268287014373078",
                "_gd_visitor": "1a3db6f0-2c82-4a4b-8857-38041b965e6e",
                "_ScCbts": "%5B%5D",
                "_sctr": "1%7C1720627200000",
                "p13np": "dhs",
                "_lr_geo_location": "TW",
                "_evga_b184": "{%22uuid%22:%220bf99460a2cca1a8%22}",
                "_sfid_c405": "{%22anonymousId%22:%220bf99460a2cca1a8%22%2C%22consents%22:[]}",
                "_fbp": "fb.1.1720678865737.353943247",
                "_tt_enable_cookie": "1",
                "_ttp": "rwG7PC8y1a_ZaSYIm0cIeWWELW8",
                "_pin_unauth": "dWlkPU5HUXhPR05rWW1FdFlqZzRZeTAwTUdOaExXRmhNemt0TVRjMU1XVTRaVFZqTWpCbA",
                "__qca": "P0-557024765-1720685693346",
                "_cs_id": "4dffab88-9eaa-ae95-ed72-c334bacc6de1.1720678869.2.1720685722.1720685669.1709063960.1754842869031.1",
                "ipe_184_fov": "%7B%22numberOfVisits%22%3A1%2C%22sessionId%22%3A%2207a89636-0851-a14e-9c3d-52e685e57213%22%2C%22expiry%22%3A%222024-08-10T08%3A15%3A24.058Z%22%2C%22lastVisit%22%3A%222024-07-11T08%3A15%3A24.058Z%22%7D",
                "akaas_dell_com_configure_unifiedpd_splits": "1723277810~rv=61~id=247955fa32c7af62f940e66f868b0129",
                "_ga_16419196": "GS1.1.1720685674.2.0.1720685811.0.0.0",
                "_ga_16418520": "GS1.1.1720685674.2.0.1720685811.0.0.0",
                "um_g_uc": "false",
                "AKA_A2": "A",
                "check": "true",
                "mboxEdgeCluster": "32",
                "_abck": "115AC061C9005533F55227986749F8A0~0~YAAQzeNH0vbSqqKQAQAAPa/KpAwMQkEZ1caGyuqSQ8/FnDDrLfPwsAYpEjy1q6W1nXTe4hFH7TBXTjHPXVoHUh4NTD8ZzG2iwa0Kmehd7npsN+5sfE+ahfhaz8Te1KdzB+y9Gyv7wEm8O//nG6vhBdg/sczNQMTUcBk2flLKpnq1VulKc+BunfzReADr3D6KL545Agw2KsZgFhJLmzm5qhPu0GRNNmiN87TgaQ3ND3xHUy1kDw8EbWpJbSV5hUz9tcz+tVHylU76c0TX/ew2QmA7RJGAfhvS4fDHIVC/VAid1DSqtCh1pEGSI5iBvJr3N9xdRKlwYqmctExtXDMp7cx5SZnyKytvfd1FVnFMj6wpvOzfR2E0dIlba3gRFrMS+aYUs409LPFtVBklmtSzJkHxuEkm1A==~-1~-1~1720755264",
                "bm_mi": "C90AD4744512879DF4F62BBD1A7A1F3C~YAAQzeNH0gvTqqKQAQAA0bDKpBi42iKNG77FlEkzahCvJobzStn+uAkl9HgzAS9I2WKs3k356NOC7dgzGDeFbXhi8EP/R7+U3DU8R1R6k4RhmCwLE+p1hoFgl88H7dQsdEuWl6TLsgpfnbBTibSfKiQw+PNrcqKtcU/prhSja8hUz7xnGDuX6NtV6KVNyG7mjPvtre4wrg0FRJ0DzOuGYTE9rmXp6SYMaDv/VQ08APeEZ7CFvr97CCIfCn6k1dywAHjayi1odk+TwcNkAvnO+7uB7jUpw/kmZYDeddgzlAGrbu/KH7XRpq4KCizE2HgRgw761lvDuONXLvJGCKFaR+j/PjiBxNUcVXe1m7On2BM=~1",
                "dc-ctxt": "c=US&l=en&sdn=work",
                "DellCEMSession": "2C31427A0D55AFC5FAA3F6393A284EFA",
                "ooc-country-code": "us",
                "ak_bmsc": "5E617CFC8F2AAF2A14214BB0622EF1A2~000000000000000000000000000000~YAAQzeNH0oXUqqKQAQAAAcHKpBgYrw2fSTw4rGpLL2NhD4U7I470jdgKQqHqLx7Aspxlrb8cWYK0OQnoR7OlCJDEFO8iu3cirYJSfKFrdZztXMTwq1CitwO4229ancojRZams7yMArSNIsQS8zkzGvADBhg4y9HLDdAJRjYxc6AQugJ+ptjCpQQJQBLyHrvytgZKsRCoGQVxRAA7qGUiHmAp0fi6FG6h2hEwezkQFwVpcd6lvTjf07j83xYqlAFi/N8ZCnAOUld7ZqLOqdzeq2DuJbnNriIrrrIRQa4T+xdo6Lc80QkxmCK1bRi8xsCE4ggIKK6ZMu+cffq9gKHjfztdYC25XXKxpaqnxVFOGxfRzsydRnEtkwYnfM2mF/3XdtYa99dGA9cQL/k+cGI0vHM+Lmb2l7jZSeqQkVNlcX0zdzaMznAc6zyI9sBLW81qa4ObHE3cdq1Hr+g2Hb0dAByhHQT7G27Wo/4/kCeoZ4VOQpYjWUaSilIYLMyJoBtoeqWAqA==",
                "rumCki": "false",
                "s_c49": "c%3Dus%26l%3Den%26s%3Dbsd%26cs%3D04",
                "gpv_pn": "us%7Cen%7Cbsd%7C04%7Cstp%7Cshop%7Ceuc%7Cproductdetails%7Cxps-8960-desktop",
                "s_tp": "9794",
                "cidlid": "%3A%3A",
                "s_depth": "1",
                "s_vnc365": "1752287676089%26vn%3D3",
                "s_ivc": "true",
                "s_cc": "true",
                "__privaci_cookie_no_action": '{"status":"no-action-consent"}',
                "_cs_mk": "0.7598701529613674_1720751678767",
                "dell_cmp_consent": '{"s":1,"m":1,"e":1}',
                "_cls_s": "1ce64b7a-036e-4c3c-ab35-ab3a7e2ba710:1",
                "_cs_cvars": "%7B%7D",
                "FPGSID": "1.1720751679.1720751679.G-5932KMEGPX.09Vi3pek8bvML6GzBllyDw",
                "akavpau_vp2": "1720751979~id=1951b7c6a503537f11228d24d2c64dad",
                "bm_sz": "D7F88EBC7E445EC38038FAC2D232CC1C~YAAQzeNH0lbXqqKQAQAAXunKpBhrXUJ712tcmK4vh95qlx4+NSvbi9DyHCqkz5505LKGLPNK7uISmx7at4QafAO8JUSzrIuUvMkra2Khd2+lr0+NFCA5LOEc2VzR3fnMtt3AtyBloiyppA0dg28pPjjlXJWZ5vKVHWcxw8kesoLDCwNW4dJ42e1fiMO0oYT9cD5Tlf5UKJb7Rr8L8fCKsCoPniNeHmGlvc+xjF6tz+7I/ZRYxdCxlA4TpUk2DCwAsDY9ZKZBPVY+WbjrseaeWu7WxWF8NvDfVnJeVGYsL/K0u1vE+78muncJthFvp3ZsewvHAAK2ypqGujHsd6tnwcXS3uU3e+oUt7fH4m4loHQkdTko+XV/RumlhdOaCNefT4yjyfwAUjMdVEHfO75BIMxT~4339509~4338232",
                "_gd_session": "145e88ba-0341-49cd-8a8e-d7d96c95d858",
                "d_dnb": "true",
                "mbox": "PC#81a2e7edaca34af1838859a74a05ec00.32_0#1783996481|session#3108bd02081b4c0aaa3bc521b0eadea5#1720753541",
                "adcloud": "{%22_les_v%22:%22y%2Cdell.com%2C1720753480%22}",
                "s_ips": "4405.199951171875",
                "_rdt_uuid": "1720685694616.e8c35a74-6347-4f53-80a5-b5c301820c60",
                "_uetsid": "a72e76603f5d11ef937513c7b412d44f",
                "_uetvid": "a72e9a603f5d11ef9e9f83c81ad3cedd",
                "akavpau_maintenance_vp": "1720751981~id=e756741220230f8c46fd2a6d838f8edd",
                "bm_sv": "6CD54AE707ABB560E8059D0457BD946E~YAAQzeNH0qjXqqKQAQAAHe7KpBh8H3HiptRjFWAxnZniuL+jk5SQ4u5r9It+0v7iNjb7ReP3lE6bycOCt0zsXmFVUNuhcOk7s1sfFgdOl0I7vgtZ1Agr1CTiKGMV6Ue+uU1BEjp/ZNue5fmGsi4YkcwIljV2lvhiZfSuzLWajaqAZwGCx9ZKOkqGiaGmC5iegDcS8Lu8VWb/5LAW+PvluRrxCYrhzNYGlm1AjIzplfsCutPbZRd3UjVznj7mxIA=~1",
                "_scid_r": "f94d06f3-93c1-4bb2-bbb9-8b5ed088a785",
                "_ga_1234567890": "GS1.1.1720751679.3.0.1720751681.0.0.83345807",
                "FPLC": "eBY8MDF%2BGQEOscAE8kvjHyHavcKBO6HuvRYHbDB0bXLb%2Fez8SQHL4AMh5qnmC%2FCf4mQK3QZseGwTZp%2BrQ%2FycxUa9zwQynUvjAq0ebW6dIpfer%2BUqThUhpRMobASuWw%3D%3D",
                "s_sq": "dellglobalonlinemaster%3D%2526c.%2526a.%2526activitymap.%2526page%253Dus%25257Cen%25257Cbsd%25257C04%25257Cstp%25257Cshop%25257Ceuc%25257Cproductdetails%25257Cxps-8960-desktop%2526link%253DFeatures%2526region%253Dcf-body%2526pageIDType%253D1%2526.activitymap%2526.a%2526.c%2526pid%253Dus%25257Cen%25257Cbsd%25257C04%25257Cstp%25257Cshop%25257Ceuc%25257Cproductdetails%25257Cxps-8960-desktop%2526pidt%253D1%2526oid%253Dhttps%25253A%25252F%25252Fwww.dell.com%25252Fen-us%25252Fshop%25252Fdesktop-computers%25252Fxps-desktop%25252Fspd%25252Fxps-8960-desktop%25252Fusextpbts8960gscy%2526ot%253DA",
                "s_ppv": "us%257Cen%257Cbsd%257C04%257Cstp%257Cshop%257Ceuc%257Cproductdetails%257Cxps-8960-desktop%2C45%2C75%2C67%2C7330%2C13%2C9",
            }
            burp0_headers = {
                "Sec-Ch-Ua": '"Not/A)Brand";v="8", "Chromium";v="126"',
                "Accept-Language": "zh-TW",
                "Sec-Ch-Ua-Mobile": "?0",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.6478.127 Safari/537.36",
                "Content-Type": "application/json; charset=UTF-8",
                "Accept": "*/*",
                "X-Requested-With": "XMLHttpRequest",
                "Sec-Ch-Ua-Platform": '"Windows"',
                "Origin": "https://www.dell.com",
                "Sec-Fetch-Site": "same-origin",
                "Sec-Fetch-Mode": "cors",
                "Sec-Fetch-Dest": "empty",
                "Referer": f"{new_link}",
                "Accept-Encoding": "gzip, deflate, br",
                "Priority": "u=1, i",
            }
            burp0_json = {
                "includeCommonScriptsInResponse": True,
                "includeCommonStylesInResponse": False,
                "includeComponentStylesInResponse": True,
                "includeMediaMfeScriptsInResponse": False,
                "includeMediaMfeStylesInResponse": False,
                "isLazyLoaded": True,
            }
            response_more =  requests.post(
                burp0_url, headers=burp0_headers, cookies=burp0_cookies, json=burp0_json
            )
            soup_more = BeautifulSoup(response_more.content, "html.parser")
            

            
            rows_soup_more = soup_more.select("div.pd-feature-wrap")
            
            rows_soup_more += soup_more.select("div.pd-feature-wrap.ThreeUp")
            
            row_soup_more_2 = soup_more.select('.rwp-webpart.rwp-webpart-ContentLayout')
        
            if rows_soup_more:
                for row in rows_soup_more:
                    # row = rows_soup_more[27]
                    key_soup = row.select_one ('h2')
                    if key_soup:
                        key = key_soup.get_text(strip=True).replace(":", "").lower()
                    else: 
                        continue
                    value_soup = row.select("div.pd-item-desc")
                    if value_soup:
                        value = ''.join([i.get_text(strip=True) for i in value_soup])
                    else:
                        continue
                    
                    spect_dict[key] = value
            
            elif row_soup_more_2:
                for row in row_soup_more_2:
                    # row = row_soup_more_2[5]
                    key_soup = row.select_one ('h2')
                    if key_soup:
                        key = key_soup.get_text(strip=True).replace(":", "").lower()
                    else: 
                        continue
                    value_soup = row.select(".rwp-contentlayout-item__content-container")
                    if value_soup:
                        value = ''.join([i.get_text(strip=True) for i in value_soup])
                    else:
                        continue
                    
                    spect_dict[key] = value
            
            
                
            if spect_dict == {}:
                error_link.append({**error_product})
                
                
            else:
                content_text = soup_more.get_text().lower()
                
                # matches_with_context = []
                # for match in re.finditer(r"5g(?!b|hz)", content_text):
                #     start_index = max(0, match.start() - 10)  # 确保不会超出字符串的开始
                #     end_index = min(len(content_text), match.end() + 10)  # 确保不会超出字符串的结束
                #     context = content_text[start_index:end_index]
                #     matches_with_context.append(context)

                # for context in matches_with_context:
                #     print(context)
                if re.findall(r"4g(?!b|hz)", content_text):
                    spect_dict["wwan"] = "4G"
                elif re.findall(r"5g(?!b|hz)", content_text):
                    spect_dict["wwan"] = "5G"
                elif re.findall(r"5g(?!b|hz)", content_text) and re.findall(
                    r"4g(?!b|hz)", content_text
                ):
                    spect_dict["wwan"] = "4G/5G"

                if "nfc" in content_text:
                    spect_dict["nfc"] = "Yes"
                else:
                    spect_dict["nfc"] = None

                if "finger" in content_text:
                    spect_dict["FPR"] = "Yes"
                    
                product_detail_list.append({**error_product, **spect_dict})
                
        except TooManyRedirects as e:
            # logging.error("Too many redirects: %s", e)
            error_link.append(error_product)
        except Exception as e:
            print(e)
            error_link.append(error_product)

    with open(f"./data/{company}/{keyword}_detail_list.json", "w") as f:
        json.dump(product_detail_list, f)

    with open(f"./data/{company}/{keyword}_error_list.json", "w") as f:
        json.dump(error_link, f)

    return product_detail_list


def detail_laptop(keyword, company):
    with open(f"./data/{company}/{keyword}_detail_list.json", "r") as f:
        product_detail_list = json.load(f)

    df_laptop = pd.DataFrame(product_detail_list)

    df_laptop.to_csv(f"./data/{company}/{keyword}_detail_list.csv",encoding='utf-8-sig')
    ports_columns_list =     [
        "ports & slots",
        "ports",
        "slots",
        "top expansion port",
        "ports and slots",
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
    df_laptop["Camera"] = df_laptop["camera"]

    df_laptop["Display"] = df_laptop["display"]

    df_laptop["Primary Battery"] = df_laptop[
        [
            "primary battery",
            "battery life",
        ]
    ].apply(lambda x: ", ".join(x.dropna().astype(str)), axis=1)

    df_laptop["Processor"] = df_laptop["processor"]

    df_laptop["Graphics Card"] = df_laptop["graphics card"]

    df_laptop["Hard Drive"] = df_laptop["storage"]

    df_laptop["Memory"] = df_laptop[["memory*", "memoryi"]].apply(
        lambda x: ", ".join(x.dropna().astype(str)), axis=1
    )

    df_laptop["Operating System"] = df_laptop["operating system"]

    df_laptop["Audio and Speakers"] = df_laptop["audio and speakers"]


    def extract_dimension(text,dimension_type):
        
        if dimension_type=='Depth':
            dimension_type_alt = "Length"
            catch_order = 3
        elif dimension_type=='Width':
            dimension_type_alt = dimension_type
            catch_order = 2
        elif dimension_type=='Height':
            dimension_type_alt = dimension_type
            catch_order = 0
            
            
            
        text = str(text)
        # print(text)
        if text == "nan":
            return None
        pattern = rf"{dimension_type}.*?(\d+\.?\d*)\s*mm(?:\s*-\s*(\d+\.?\d*)\s*mm)?"
        match = re.search(pattern, text, re.IGNORECASE)

        pattern_cm = rf"{dimension_type}.*?(\d+\.?\d*)\s*cm(?:\s*-\s*(\d+\.?\d*)\s*cm)?"
        match_cm = re.search(pattern_cm, text, re.IGNORECASE)

        pattern_len = rf"{dimension_type_alt}.*?(\d+\.?\d*)\s*mm(?:\s*-\s*(\d+\.?\d*)\s*mm)?"
        match_len = re.search(pattern_len, text, re.IGNORECASE)
        
        pattern_in = rf"{dimension_type_alt}.*?(\d+\.?\d*)\s*in(?:\s*-\s*(\d+\.?\d*)\s*in)?"
        match_in = re.search(pattern_in, text, re.IGNORECASE)
        

        if match:
            return float(match.group(1))
        elif match_cm:
            return float(match_cm.group(1)) * 100
        elif match_len:
            return float(match_len.group(1))
        elif match_in:
            return float(match_in.group(1)) * 25.4
        else:
            if "H/W/D" in text:
                pattern = r"(\d+\.?\d*)\s*mm"
                matches = re.findall(pattern, text, re.IGNORECASE)

                return float(matches[catch_order])
        return None

    def extract_weight(text):

        text = str(text).lower()
        # print(text)
        if text == "nan":
            return None
        pattern = r"Weight.*?(\d+\.?\d*)\s*kg(?:\s*-\s*(\d+\.?\d*)\s*kg)?"
        match = re.search(pattern, text, re.IGNORECASE)
        
        pattern_oz = r"Weight.*?(\d+\.?\d*)\s*oz(?:\s*-\s*(\d+\.?\d*)\s*oz)?"
        match_oz = re.search(pattern_oz, text, re.IGNORECASE)

        if match:
            if match.group(2):
                return min(float(match.group(1)), float(match.group(2)))
            return float(match.group(1))
        elif match_oz:
            if match_oz.group(2):
                return min(float(match_oz.group(1)) * 0.0283495, float(match_oz.group(2)) * 0.0283495)
            return float(match_oz.group(1)) * 0.0283495
        else:
            if "H/W/D" in text:
                pattern = r"(\d+\.?\d*)\s*kg"
                matches = re.findall(pattern, text, re.IGNORECASE)

                return float(matches[0])

        return None
    df_laptop['Dimensions & Weight'] = df_laptop[
        [
            "dimensions & weight",
            "dimensions and weight",
        ]
    ].apply(lambda x: ", ".join(x.dropna().astype(str)), axis=1)

    df_laptop["Height(mm)"] = df_laptop["Dimensions & Weight"].apply(lambda x: extract_dimension(x, "Height"))
    df_laptop["Width(mm)"] = df_laptop["Dimensions & Weight"].apply(lambda x: extract_dimension(x, "Width"))
    df_laptop["Depth(mm)"] = df_laptop["Dimensions & Weight"].apply(lambda x: extract_dimension(x, "Depth"))

    df_laptop["Weight(kg)"] = df_laptop["Dimensions & Weight"].apply(extract_weight)

    if "wwan" not in df_laptop.columns:
        df_laptop["WWAN"] = None
    else:
        df_laptop["WWAN"] = df_laptop["wwan"]

    df_laptop["NFC"] = df_laptop["nfc"]

    #TODO keyboard中也會出現
    def set_fpr(row):
        # 检查'fingerprint reader'字段是否为'yes'
        if "with finger" in str(row["palmrest"]).lower():
            return "Yes"
        elif "without finger" in str(row["palmrest"]).lower():
            return "No"
        elif row["FPR"] == "Yes":
            return "Yes"
        elif 'with finger' in str(row["keyboard"].lower()):
            return "Yes"

        else:
            return None


    df_laptop["FPR"] = df_laptop.apply(set_fpr, axis=1)
    df_laptop["FPR_model"] = None

    df_laptop["Power Supply"] = df_laptop["power"] 
    df_laptop["Brand"] = company

    df_laptop["Official Price"] = df_laptop["Official Price"].str.replace(
        "Dell Price", ""
    )
    
    def determine_type(row):
        model_name = row["Model Name"].lower()
        if "chrome" in model_name:
            row["Operating System"] = "Chrome OS"
            return "Chrome"
        elif "precision" in model_name or "workstation" in model_name:
            return "Workstation"
        elif "alienware" in model_name or "gaming" in model_name:
            return "Gaming"
        elif "latitude" in model_name or "vostro" in model_name:
            return "Commercial"
        elif "inspiron" in model_name or "xps" in model_name:
            return "Consumer"
        else:
            return "None Type_NB"

    # 应用函数
    df_laptop["Type"] = df_laptop.apply(determine_type, axis=1)
    

    # 指定要输出的字段列表
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
    df_laptop[columns_to_output].to_csv(
        f"./data/{company}/{keyword}.csv", encoding="utf-8-sig", index=False
    )

    df_laptop = df_laptop[columns_to_output]
    return df_laptop

def detail_desktop(keyword, company):
    with open(f"./data/{company}/{keyword}_detail_list.json", "r") as f:
        product_detail_list = json.load(f)

    df_desktop = pd.DataFrame(product_detail_list)

    # df_desktop.to_csv(f"./{company}/{keyword}_detail_list.csv",encoding='utf-8-sig')
    ports_columns_list = [
        "ports & slots",
        "ports",
        "slots",
        "top expansion port",
        "ports and slots",
        'connectivity options'
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
    # df_desktop["Camera"] = df_desktop["Camera"]

    df_desktop["Display"] = df_desktop[
        [
            "display",
            "monitor",
        ]
    ].apply(lambda x: ", ".join(x.dropna().astype(str)), axis=1)


    df_desktop["Processor"] = df_desktop["processor"]

    df_desktop["Graphics Card"] = df_desktop["graphics card"]

    df_desktop["Hard Drive"] = df_desktop["storage"]

    df_desktop["Memory"] = df_desktop[["memory*", "memoryi"]].apply(
        lambda x: ", ".join(x.dropna().astype(str)), axis=1
    )

    df_desktop["Operating System"] = df_desktop["operating system"]

    df_desktop["Audio and Speakers"] = df_desktop["speakers"]

    def extract_dimension(text,dimension_type):
        
        if dimension_type=='Depth':
            dimension_type_alt = "Length"
            catch_order = 3
        elif dimension_type=='Width':
            dimension_type_alt = dimension_type
            catch_order = 2
        elif dimension_type=='Height':
            dimension_type_alt = dimension_type
            catch_order = 0
            
            
            
        text = str(text)
        # print(text)
        if text == "nan":
            return None
        pattern = rf"{dimension_type}.*?(\d+\.?\d*)\s*mm(?:\s*-\s*(\d+\.?\d*)\s*mm)?"
        match = re.search(pattern, text, re.IGNORECASE)

        pattern_cm = rf"{dimension_type}.*?(\d+\.?\d*)\s*cm(?:\s*-\s*(\d+\.?\d*)\s*cm)?"
        match_cm = re.search(pattern_cm, text, re.IGNORECASE)

        pattern_len = rf"{dimension_type_alt}.*?(\d+\.?\d*)\s*mm(?:\s*-\s*(\d+\.?\d*)\s*mm)?"
        match_len = re.search(pattern_len, text, re.IGNORECASE)
        
        pattern_in = rf"{dimension_type_alt}.*?(\d+\.?\d*)\s*in(?:\s*-\s*(\d+\.?\d*)\s*in)?"
        match_in = re.search(pattern_in, text, re.IGNORECASE)
        

        if match:
            return float(match.group(1))
        elif match_cm:
            return float(match_cm.group(1)) * 100
        elif match_len:
            return float(match_len.group(1))
        elif match_in:
            return float(match_in.group(1)) * 25.4
        else:
            if "H/W/D" in text:
                pattern = r"(\d+\.?\d*)\s*mm"
                matches = re.findall(pattern, text, re.IGNORECASE)

                return float(matches[catch_order])
        return None

    def extract_weight(text):

        text = str(text).lower()
        # print(text)
        if text == "nan":
            return None
        pattern = r"Weight.*?(\d+\.?\d*)\s*kg(?:\s*-\s*(\d+\.?\d*)\s*kg)?"
        match = re.search(pattern, text, re.IGNORECASE)
        
        pattern_oz = r"Weight.*?(\d+\.?\d*)\s*oz(?:\s*-\s*(\d+\.?\d*)\s*oz)?"
        match_oz = re.search(pattern_oz, text, re.IGNORECASE)

        if match:
            if match.group(2):
                return min(float(match.group(1)), float(match.group(2)))
            return float(match.group(1))
        elif match_oz:
            if match_oz.group(2):
                return min(float(match_oz.group(1)) * 0.0283495, float(match_oz.group(2)) * 0.0283495)
            return float(match_oz.group(1)) * 0.0283495
        else:
            if "H/W/D" in text:
                pattern = r"(\d+\.?\d*)\s*kg"
                matches = re.findall(pattern, text, re.IGNORECASE)

                return float(matches[0])

        return None
    
    df_desktop['Dimensions & Weight'] = df_desktop[
        [
            "dimensions & weight",
            "dimensions and weight",
        ]
    ].apply(lambda x: ", ".join(x.dropna().astype(str)), axis=1)


    df_desktop["Height(mm)"] = df_desktop["Dimensions & Weight"].apply(lambda x: extract_dimension(x, "Height"))
    df_desktop["Width(mm)"] = df_desktop["Dimensions & Weight"].apply(lambda x: extract_dimension(x, "Width"))
    df_desktop["Depth(mm)"] = df_desktop["Dimensions & Weight"].apply(lambda x: extract_dimension(x, "Depth"))

    df_desktop["Weight(kg)"] = df_desktop["Dimensions & Weight"].apply(extract_weight)



    df_desktop["Power Supply"] = df_desktop[
        [
            "power",
            "power supply",
        ]
    ].apply(lambda x: ", ".join(x.dropna().astype(str)), axis=1)

    df_desktop["Brand"] = company

    df_desktop["Official Price"] = df_desktop["Official Price"].str.replace(
        "Dell Price", ""
    )
    
    
    def determine_type_desktop(row):
        model_name = row["Model Name"].lower()
        if "precision" in model_name or "workstation" in model_name:
            return "Workstation"
        elif "alienware" in model_name:
            return "Gaming"
        elif "optiplex" in model_name or "vostro" in model_name:
            return "Commercial"
        elif "inspiron" in model_name or "xps" in model_name:
            return "Consumer"
        else:
            return "None Type_DT"

    # 应用函数
    df_desktop["Type"] = df_desktop.apply(determine_type_desktop, axis=1)

    # 指定要输出的字段列表
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
    df_desktop[columns_to_output].to_csv(
        f"./data/{company}/{keyword}.csv", encoding="utf-8-sig", index=False
    )

    df_desktop = df_desktop[columns_to_output]
    return df_desktop

def detail_docking(keyword, company):
    with open(f"./data/{company}/{keyword}_detail_list.json", "r") as f:
        product_detail_list = json.load(f)

    df_docking = pd.DataFrame(product_detail_list)

    df_docking.to_csv(f"./data/{company}/{keyword}_detail_list.csv",encoding='utf-8-sig')
    ports_columns_list = [
        "expansion / connectivity",
        "interfaces/ports",
        "slots",
        "top expansion port",
        "ports and slots",
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
    def extract_weight(text):

        text = str(text).lower()
        # print(text)
        if text == "nan":
            return None
        pattern = r"Weight.*?(\d+\.?\d*)\s*kg(?:\s*-\s*(\d+\.?\d*)\s*kg)?"
        match = re.search(pattern, text, re.IGNORECASE)
        
        pattern_oz = r"Weight.*?(\d+\.?\d*)\s*oz(?:\s*-\s*(\d+\.?\d*)\s*oz)?"
        match_oz = re.search(pattern_oz, text, re.IGNORECASE)
        
        pattern_lbs = r"Weight.*?(\d+\.?\d*)\s*lb(?:\s*-\s*(\d+\.?\d*)\s*lb)?"
        match_lbs = re.search(pattern_lbs, text, re.IGNORECASE)

        if match:
            if match.group(2):
                return min(float(match.group(1)), float(match.group(2)))
            return float(match.group(1))
        elif match_oz:
            if match_oz.group(2):
                return min(float(match_oz.group(1)) * 0.0283495, float(match_oz.group(2)) * 0.0283495)
            return float(match_oz.group(1)) * 0.0283495
        elif match_lbs:
            if match_lbs.group(2):
                return min(float(match_lbs.group(1)) * 0.453592, float(match_lbs.group(2)) * 0.453592)
            return float(match_lbs.group(1)) * 0.453592
        
        else:
            if "H/W/D" in text:
                pattern = r"(\d+\.?\d*)\s*kg"
                matches = re.findall(pattern, text, re.IGNORECASE)

                return float(matches[0])

        return None
    df_docking['Dimensions & Weight'] = df_docking[
        [
            "dimensions & weight",
            "dimensions and weight",
            "general",
            "physical characteristics"
        ]
    ].apply(lambda x: ", ".join(x.dropna().astype(str)), axis=1)
    
    df_docking["Weight(kg)"] = df_docking["Dimensions & Weight"].apply(extract_weight)
    
    df_docking["Power Supply"] = df_docking[
        [
            "power",
            "power description",
        ]
    ].apply(lambda x: ", ".join(x.dropna().astype(str)), axis=1)

    df_docking["Brand"] = company

    df_docking["Official Price"] = df_docking["Official Price"].str.replace(
        "Dell Price", ""
    )
    df_docking['Type'] = ""
    
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
    df_docking[columns_to_output].to_csv(
        f"./data/{company}/{keyword}.csv", encoding="utf-8-sig", index=False
    )

    df_docking = df_docking[columns_to_output]
    return df_docking


keyword_list = ["laptop", "desktop", "docking"]
company = "Dell"

for keyword in keyword_list:
    # keyword = keyword_list[2]
    search_crawl(keyword, company)
    
    if keyword == "laptop":
        detail_crawl(keyword, company)
        detail_crawl_more(keyword, company)
        detail_laptop(keyword, company)
    if keyword == "desktop":
        detail_crawl(keyword, company)
        detail_crawl_more(keyword, company)
        detail_desktop(keyword, company)
    if keyword == "docking":
        detail_crawl(keyword, company)
        detail_docking(keyword, company)
        

    # elif keyword == "desktop":
    #     detail_desktop(keyword, company)
    # elif keyword == "docking":
    #     detail_docking(keyword, company)
