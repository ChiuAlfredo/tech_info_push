import requests
import json
import os 
import glob
from bs4 import BeautifulSoup
import re


import time
from functools import wraps

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

    url = f"https://www.lenovo.com/us/en/search?fq=?&text={keyword}&rows=60&sort=relevance&display_tab=Products&page={page_number}&more=1"

    # url ='https://www.lenovo.com/us/en/search?fq={!ex=prodCat}lengs_Product_facet_ProdCategories:PCs%20Tablets&text=Laptops&rows=60&sort=relevance&display_tab=Products&more=1&page=11'
    payload = {}
    
    headers ={
        'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
        # 'Cookie':'zipcode=60654; leid=2.Y+i9b/nJUlF; searchabran=2; AMCV_F6171253512D2B8C0A490D45%40AdobeOrg=MCMID|22796032703182726071512371125726346184; navposkey=pc_nav; fsid=19; BVBRANDID=da21a037-de34-4ab3-987a-52d6b0be7a7d; ftv_for_usen=%252Fpc%252F; aamtest1=auto%3D549200; Adform%20Cookie%20ID=4059607695632243559; fl_guid=5701551EFF6D83; _ga=GA1.1.1746570426.1696555783; _mibhv=anon-1696555783300-6860938145_4876; _gcl_au=1.1.1993526881.1696555784; _tt_enable_cookie=1; _ttp=TDYcYSlEw5lhQzyTmx1l-lsM8WM; _fbp=fb.1.1696555788053.1759168665; _mkto_trk=id:183-WCT-620&token:_mch-lenovo.com-1696555788090-60972; ki_r=; _rdt_uuid=1696555790511.3082e1b5-8344-465f-8dae-02c1afc93e2e; QuantumMetricUserID=309abf2bad683b1de82791752efec793; algorithmId_adobe=%7B%22algorithmId%22%3Anull%7D; ki_s=199507%3A0.0.0.0.0; bluecoreNV=false; aam_sc=aamsc%3D3901189%7C3872579%7C10138496%7C10137485%7C9562573%7C11003488; _scid=e996b99e-96bd-4d70-a8eb-ca87cc0a0ac4; _scid_r=e996b99e-96bd-4d70-a8eb-ca87cc0a0ac4; _sctr=1%7C1696953600000; apay-session-set=hzQOmnSszVvZwfIIZuAHKg8vrSREuk4Eo7ZDs%2FLOqVjpEhfkYJ5YVAYZyVc29BU%3D; has_consent_cookie=; kndctr_F6171253512D2B8C0A490D45_AdobeOrg_consent=general%3Din; fsid=19; _uetvid=d358ad0063e711ee9310ad79f9d8b198; _evidon_consent_cookie={"consent_date":"2023-10-06T01:45:02.780Z","categories":{"1":{"essential":true,"analytics":true,"advertising":false,"social media":false}},"vendors":{"1":{"11":true,"14":false,"17":false,"31":true,"51":false,"63":true,"66":false,"80":false,"81":false,"82":false,"84":false,"99":false,"103":true,"108":true,"111":true,"128":true,"131":false,"149":false,"167":true,"174":false,"242":true,"249":false,"253":true,"257":false,"259":false,"290":true,"307":true,"321":true,"348":false,"384":false,"395":true,"414":true,"426":false,"442":false,"467":true,"480":true,"523":true,"560":false,"611":true,"662":true,"674":false,"688":true,"828":true,"831":false,"905":false,"933":true,"937":true,"1028":false,"1267":false,"1272":true,"1306":false,"1412":false,"1647":true,"1727":true,"2230":true,"2516":false,"2594":true,"3042":true,"3058":true,"3355":true,"3490":false,"3778":true,"3878":true,"4160":false,"4526":false,"4748":true,"4948":false,"5130":true,"5296":false,"6171":true,"6357":true,"6359":true,"6609":true,"6638":false}},"cookies":{"1":{}},"gpc":1,"consent_type":2}; kndctr_F6171253512D2B8C0A490D45_AdobeOrg_identity=CiYyMjc5NjAzMjcwMzE4MjcyNjA3MTUxMjM3MTEyNTcyNjM0NjE4NFIRCKSl6pSwMRgBKgRTR1AzMAGgAeDRsPq6MagB7%2Dr2vuuQuqZJsAEG8AHq6uPSuzE%3D; LOSAD=1; p3094257258_done=1; p3094257258_done=1; _page_type_=Single%20Model%20PDP; kndctr_F6171253512D2B8C0A490D45_AdobeOrg_cluster=sgp3; s_inv=4580; s_vnc365=1731219983511%26vn%3D18; s_ivc=true; QuantumMetricSessionID=96fc47dbc94f9305c1775d35b71d9d4e; bm_mi=EB868BF2C19A71704F05AFDD4F45A7B0~YAAQz+NH0gqJqKaLAQAAYiEQvRXR9NUAWZ6Q1RxUFtzKMfb81S4y8hkfqekIXJXr02Ge/zPEQl8hrRCZxzEWyxK6FYMH64hllEr6gF5G40GPox5Ajs0G/gX+gk26YGsyVzCYJRPbXGgCi04WeuW6tvpLXV4zsQcKRYZn5cyjVbfzMGV4BCPp5RuDGA/V0IXErP6OMRMLgXlklMSH27CW/bvCehz2cyL+u0saG/sfALiGiJ/Xoku22OHH3oqYifjLMKtrcLArb+2l4Fp7N9c2PVFnkU3wL2aonfS3GGoIhILj2L/jot0kgyLkKOBZtu7DcyHuR7NESJG/yKyMjnmNLPDPeILw8ow1Md+ZDM88RR9OC5bpyCKk092B0wDrSoQOerxrAfOi5tIdMOaP0F6H7gH5hu2PeIllskQ0aUENqJf+WTX6HBWuKGBSfLIB1t0b~1; ak_bmsc=DC14E4D15661434ED05E97878E609BE5~000000000000000000000000000000~YAAQz+NH0tuJqKaLAQAAgicQvRWWDRyYiMu/Fisxozj5i7nR9QbgjE0Pec1cCeaXwBGgUjQmy+gyVCwzQHRZxqLzk+cISswvCYRBL8dISdJ0aUyRsCUHMP+ipe7s81LPczlvvn4lMenHqchuv36bsLd9XQHRG4tiROX521QK2TPquSjoHlRlEPVkkFfhQDO8W+pLel8N+abIPgEKodeyyIW8Sqr1SaMhI4Nq53PAVVAzdqfLPfbxLQLobNKO5lbHJ11luFqa+oVRqRyfa3YVSKFkj2tFcRTVNyD+dcQAx+HmipnqMRjp2eQTlg15g/34zraFqxjPEK3p4AX6XB6NgmKjRch+jDBzZc3uwAAG2IWcr7lTmSt+T+48rtw2QUvvJeON1Heu5hDjQwIgRkvPnZF565hx0MeN1BBD0q62UJFy734j3m8l9+d/jGhLRIkimV6yUktr1N00tzDny6x7Hkl9zFlOaa1+bGLeQY7fTo5hsZSjxMdMGUNukyUt8BGNcgKLmAxRzMLypEQEVKVEMgu4dVhc9OnTpzafkr0aOUjEsFr1bl4r5zOH0YVoQCJV/ZvxuM9Q2+NyKtpY/dXtffjAfjWFniYL3zRsxhreIcevfOCfuzaKHXd7gbD20cy527JwZ8N3mvRS5x++xePKwE7RLQ==; recentlypns=90UX0004US%2C90V7003HUS%2CF0GH00PBUS%2CF0EU00MAUS%2C90VJ000EUS%2C90SM00C5US; fusionEXPID=flash_na_app_qpl_MLR_Flash_NER; s_eVar57=s.products_evar; s_eng_rfd=12.12; AKA_A2=A; _abck=540660EA9576B22ADDEF089463DBB37F~0~YAAQzONH0mzX/K6LAQAAKLxLvQqLxhxYmAUJXu6SytpfaJyyNthvOs7eJl7s51eAflV5WrG67dzAPGxwlsEH0XgheiRXcDoCEsRzbt+0GLS1K+PyzEnueJVL80svaF/DN04MfBBQkqYzhTMqRjTfOCjwHlRv7US5F2MAli9iJAxTDG5rhXSONekSnhgVLUoaa7I+FdIJSNHV0VVA6KOuPVI5lf08BCSRlpsewJ9f+6/1/aSK50HDDwntWAGBJPMYNUmPC4BgI1BiQfOrYJiAhs03XiA2FXmyDO1Cf9W7GO+EzsHmTS/ZXupydWR1sDVTTWJC553t7MXn3VnnTMuPGoqKDsnlXXc1l8Gw4vEVcupmlcX92ehxvWCE0Hn50NLxcQwrYBV7pSZ/xNhr9/7suuET3CqPqGP+~-1~-1~1699691479; s_dur=1699687939130; bc_invalidateUrlCache_targeting=1699687940976; fusionQueryId=bt8y1Pbzwt; bm_sz=91322B11B187BB341CFD60D14829BD09~YAAQzONH0sR6/a6LAQAAEXVSvRXXXcKS8u2cRofODfxYyZ0eyVwHSDinVsSHM67qcCOrrTq0i6wGL7NGVXCmpqw8EA09sw+psYT1P+tFp29KlgLg1XtcuPFm+SVYH/uJjMzk1SjYgWGQyaj3IUIiCofZeahyH+8XbPYSLtNOlps0feoBmbu6VzSDApRcRA87E0QOxR0S+4JnKNhiVLvwC994LzpN2HFnptfxB71xB7I2mmoGQemCRSnrUEug9HOfWPxfUelo+R90/0Crw4Xy82xLI6uf6yXa9XGU3c5I/otFqNu9ubVdMd/rEfB/V5LK7cU7UcFYRHf95+8=~3487793~3294008; s_tslv=1699688394620; s_tot_rfd=0.91; _ga_LXNLK45HZF=GS1.1.1699683982.19.1.1699688395.0.0.0; _ga_1RPSEV71KD=GS1.1.1699683982.15.1.1699688395.60.0.0; ki_t=1696555788502%3B1699683986706%3B1699688395656%3B8%3B155; mp_lenovo_us_mixpanel=%7B%22distinct_id%22%3A%20%2218b029ad5ce1b8-0872ace045a4a8-18525634-13c680-18b029ad5d535%22%2C%22bc_persist_updated%22%3A%201696555783639%7D; _ga_X0H82YEL7G=GS1.1.1699683982.15.1.1699688395.60.0.0; inside-us3=218290524-1731bf7cf3f5fc6879fd48c675d59188f8407b850772e0f9b48518d68faa898b-0-0; exitsurveynotdisplayed=Page%20count%20not%20met; RT="z=1&dm=lenovo.com&si=a29aea7b-13e3-4d20-ae35-c5c617791161&ss=lotqb8z0&sl=5&tt=cqn&bcn=%2F%2F684d0d47.akstat.io%2F&ld=9ucc&ul=9y77&hd=9yc3"; akavpau_WaitingRoomController=1699688708~id=6b8e1423783b8921e58e3c7f473e425b; bm_sv=BB9422D2F2F866366D19CF4F4932BA8B~YAAQzONH0iWG/a6LAQAAI+ZSvRVD6CFZ4m6Uo/FbmAeEs5xc75gFf974VaQs4DOx86aW7yyI/L7N7Sunr9qDTOLrPed5TaL0GNz0XPgdLWnDbz4Xm698xgFS35KhS135WbYHswaNLTGo5POTPM38ejHeQ4h1beYY6FEYzqNIVDF/ztkGTv+4RP/wwsVsRQBCMHzuiXj3GpVpGMIB915Z8BvEFxPpN1aN6nlZRk7A29WSkideZPvyeW2A4sKWT7jm9ngifDnUhbP+~1',
        'Upgrade-Insecure-Requests': '1'
    }

    response = requests.request("GET", url,headers=headers, data=payload)

    print(page_number)


    soup = BeautifulSoup(response.text, 'html.parser')
    # print(soup)
    
    # len(soup.select('.part_number'))
    
    web_url_soup = soup.select('.product_item>.product_name>a')
    product_name_soup = soup.select('.product_item>.product_name')
    product_code_soup = soup.select('.product_item>.product_name>a')
    
    web_url_list = [i.get('href') for i in web_url_soup]
    product_name_list = [i.text for i in product_name_soup]
    product_code_list = [i.get('data-productcode') for i in product_code_soup]
    
    product_number = len(web_url_list)
    print(len(product_name_list))
    
    return web_url_list,product_name_list,product_code_list,product_number

# 獲取thinksta
def get_page_json_thinksta(page_number,keyword,**kwargs):

    url = f'https://www.lenovo.com/us/en/search?fq=%7B!ex=prodCat%7Dlengs_Product_facet_ProdCategories:PCs%20Tablets&text={keyword}&rows=60&sort=relevance&display_tab=Products&page={page_number}&more=1'
    print(url)
    # url ='https://www.lenovo.com/us/en/search?fq={!ex=prodCat}lengs_Product_facet_ProdCategories:PCs%20Tablets&text=Laptops&rows=60&sort=relevance&display_tab=Products&more=1&page=11'
    payload = {}
    
    headers ={
        'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
        # 'Cookie':'zipcode=60654; leid=2.Y+i9b/nJUlF; searchabran=2; AMCV_F6171253512D2B8C0A490D45%40AdobeOrg=MCMID|22796032703182726071512371125726346184; navposkey=pc_nav; fsid=19; BVBRANDID=da21a037-de34-4ab3-987a-52d6b0be7a7d; ftv_for_usen=%252Fpc%252F; aamtest1=auto%3D549200; Adform%20Cookie%20ID=4059607695632243559; fl_guid=5701551EFF6D83; _ga=GA1.1.1746570426.1696555783; _mibhv=anon-1696555783300-6860938145_4876; _gcl_au=1.1.1993526881.1696555784; _tt_enable_cookie=1; _ttp=TDYcYSlEw5lhQzyTmx1l-lsM8WM; _fbp=fb.1.1696555788053.1759168665; _mkto_trk=id:183-WCT-620&token:_mch-lenovo.com-1696555788090-60972; ki_r=; _rdt_uuid=1696555790511.3082e1b5-8344-465f-8dae-02c1afc93e2e; QuantumMetricUserID=309abf2bad683b1de82791752efec793; algorithmId_adobe=%7B%22algorithmId%22%3Anull%7D; ki_s=199507%3A0.0.0.0.0; bluecoreNV=false; aam_sc=aamsc%3D3901189%7C3872579%7C10138496%7C10137485%7C9562573%7C11003488; _scid=e996b99e-96bd-4d70-a8eb-ca87cc0a0ac4; _scid_r=e996b99e-96bd-4d70-a8eb-ca87cc0a0ac4; _sctr=1%7C1696953600000; apay-session-set=hzQOmnSszVvZwfIIZuAHKg8vrSREuk4Eo7ZDs%2FLOqVjpEhfkYJ5YVAYZyVc29BU%3D; has_consent_cookie=; kndctr_F6171253512D2B8C0A490D45_AdobeOrg_consent=general%3Din; fsid=19; _uetvid=d358ad0063e711ee9310ad79f9d8b198; _evidon_consent_cookie={"consent_date":"2023-10-06T01:45:02.780Z","categories":{"1":{"essential":true,"analytics":true,"advertising":false,"social media":false}},"vendors":{"1":{"11":true,"14":false,"17":false,"31":true,"51":false,"63":true,"66":false,"80":false,"81":false,"82":false,"84":false,"99":false,"103":true,"108":true,"111":true,"128":true,"131":false,"149":false,"167":true,"174":false,"242":true,"249":false,"253":true,"257":false,"259":false,"290":true,"307":true,"321":true,"348":false,"384":false,"395":true,"414":true,"426":false,"442":false,"467":true,"480":true,"523":true,"560":false,"611":true,"662":true,"674":false,"688":true,"828":true,"831":false,"905":false,"933":true,"937":true,"1028":false,"1267":false,"1272":true,"1306":false,"1412":false,"1647":true,"1727":true,"2230":true,"2516":false,"2594":true,"3042":true,"3058":true,"3355":true,"3490":false,"3778":true,"3878":true,"4160":false,"4526":false,"4748":true,"4948":false,"5130":true,"5296":false,"6171":true,"6357":true,"6359":true,"6609":true,"6638":false}},"cookies":{"1":{}},"gpc":1,"consent_type":2}; kndctr_F6171253512D2B8C0A490D45_AdobeOrg_identity=CiYyMjc5NjAzMjcwMzE4MjcyNjA3MTUxMjM3MTEyNTcyNjM0NjE4NFIRCKSl6pSwMRgBKgRTR1AzMAGgAeDRsPq6MagB7%2Dr2vuuQuqZJsAEG8AHq6uPSuzE%3D; LOSAD=1; p3094257258_done=1; p3094257258_done=1; _page_type_=Single%20Model%20PDP; kndctr_F6171253512D2B8C0A490D45_AdobeOrg_cluster=sgp3; s_inv=4580; s_vnc365=1731219983511%26vn%3D18; s_ivc=true; QuantumMetricSessionID=96fc47dbc94f9305c1775d35b71d9d4e; bm_mi=EB868BF2C19A71704F05AFDD4F45A7B0~YAAQz+NH0gqJqKaLAQAAYiEQvRXR9NUAWZ6Q1RxUFtzKMfb81S4y8hkfqekIXJXr02Ge/zPEQl8hrRCZxzEWyxK6FYMH64hllEr6gF5G40GPox5Ajs0G/gX+gk26YGsyVzCYJRPbXGgCi04WeuW6tvpLXV4zsQcKRYZn5cyjVbfzMGV4BCPp5RuDGA/V0IXErP6OMRMLgXlklMSH27CW/bvCehz2cyL+u0saG/sfALiGiJ/Xoku22OHH3oqYifjLMKtrcLArb+2l4Fp7N9c2PVFnkU3wL2aonfS3GGoIhILj2L/jot0kgyLkKOBZtu7DcyHuR7NESJG/yKyMjnmNLPDPeILw8ow1Md+ZDM88RR9OC5bpyCKk092B0wDrSoQOerxrAfOi5tIdMOaP0F6H7gH5hu2PeIllskQ0aUENqJf+WTX6HBWuKGBSfLIB1t0b~1; ak_bmsc=DC14E4D15661434ED05E97878E609BE5~000000000000000000000000000000~YAAQz+NH0tuJqKaLAQAAgicQvRWWDRyYiMu/Fisxozj5i7nR9QbgjE0Pec1cCeaXwBGgUjQmy+gyVCwzQHRZxqLzk+cISswvCYRBL8dISdJ0aUyRsCUHMP+ipe7s81LPczlvvn4lMenHqchuv36bsLd9XQHRG4tiROX521QK2TPquSjoHlRlEPVkkFfhQDO8W+pLel8N+abIPgEKodeyyIW8Sqr1SaMhI4Nq53PAVVAzdqfLPfbxLQLobNKO5lbHJ11luFqa+oVRqRyfa3YVSKFkj2tFcRTVNyD+dcQAx+HmipnqMRjp2eQTlg15g/34zraFqxjPEK3p4AX6XB6NgmKjRch+jDBzZc3uwAAG2IWcr7lTmSt+T+48rtw2QUvvJeON1Heu5hDjQwIgRkvPnZF565hx0MeN1BBD0q62UJFy734j3m8l9+d/jGhLRIkimV6yUktr1N00tzDny6x7Hkl9zFlOaa1+bGLeQY7fTo5hsZSjxMdMGUNukyUt8BGNcgKLmAxRzMLypEQEVKVEMgu4dVhc9OnTpzafkr0aOUjEsFr1bl4r5zOH0YVoQCJV/ZvxuM9Q2+NyKtpY/dXtffjAfjWFniYL3zRsxhreIcevfOCfuzaKHXd7gbD20cy527JwZ8N3mvRS5x++xePKwE7RLQ==; recentlypns=90UX0004US%2C90V7003HUS%2CF0GH00PBUS%2CF0EU00MAUS%2C90VJ000EUS%2C90SM00C5US; fusionEXPID=flash_na_app_qpl_MLR_Flash_NER; s_eVar57=s.products_evar; s_eng_rfd=12.12; AKA_A2=A; _abck=540660EA9576B22ADDEF089463DBB37F~0~YAAQzONH0mzX/K6LAQAAKLxLvQqLxhxYmAUJXu6SytpfaJyyNthvOs7eJl7s51eAflV5WrG67dzAPGxwlsEH0XgheiRXcDoCEsRzbt+0GLS1K+PyzEnueJVL80svaF/DN04MfBBQkqYzhTMqRjTfOCjwHlRv7US5F2MAli9iJAxTDG5rhXSONekSnhgVLUoaa7I+FdIJSNHV0VVA6KOuPVI5lf08BCSRlpsewJ9f+6/1/aSK50HDDwntWAGBJPMYNUmPC4BgI1BiQfOrYJiAhs03XiA2FXmyDO1Cf9W7GO+EzsHmTS/ZXupydWR1sDVTTWJC553t7MXn3VnnTMuPGoqKDsnlXXc1l8Gw4vEVcupmlcX92ehxvWCE0Hn50NLxcQwrYBV7pSZ/xNhr9/7suuET3CqPqGP+~-1~-1~1699691479; s_dur=1699687939130; bc_invalidateUrlCache_targeting=1699687940976; fusionQueryId=bt8y1Pbzwt; bm_sz=91322B11B187BB341CFD60D14829BD09~YAAQzONH0sR6/a6LAQAAEXVSvRXXXcKS8u2cRofODfxYyZ0eyVwHSDinVsSHM67qcCOrrTq0i6wGL7NGVXCmpqw8EA09sw+psYT1P+tFp29KlgLg1XtcuPFm+SVYH/uJjMzk1SjYgWGQyaj3IUIiCofZeahyH+8XbPYSLtNOlps0feoBmbu6VzSDApRcRA87E0QOxR0S+4JnKNhiVLvwC994LzpN2HFnptfxB71xB7I2mmoGQemCRSnrUEug9HOfWPxfUelo+R90/0Crw4Xy82xLI6uf6yXa9XGU3c5I/otFqNu9ubVdMd/rEfB/V5LK7cU7UcFYRHf95+8=~3487793~3294008; s_tslv=1699688394620; s_tot_rfd=0.91; _ga_LXNLK45HZF=GS1.1.1699683982.19.1.1699688395.0.0.0; _ga_1RPSEV71KD=GS1.1.1699683982.15.1.1699688395.60.0.0; ki_t=1696555788502%3B1699683986706%3B1699688395656%3B8%3B155; mp_lenovo_us_mixpanel=%7B%22distinct_id%22%3A%20%2218b029ad5ce1b8-0872ace045a4a8-18525634-13c680-18b029ad5d535%22%2C%22bc_persist_updated%22%3A%201696555783639%7D; _ga_X0H82YEL7G=GS1.1.1699683982.15.1.1699688395.60.0.0; inside-us3=218290524-1731bf7cf3f5fc6879fd48c675d59188f8407b850772e0f9b48518d68faa898b-0-0; exitsurveynotdisplayed=Page%20count%20not%20met; RT="z=1&dm=lenovo.com&si=a29aea7b-13e3-4d20-ae35-c5c617791161&ss=lotqb8z0&sl=5&tt=cqn&bcn=%2F%2F684d0d47.akstat.io%2F&ld=9ucc&ul=9y77&hd=9yc3"; akavpau_WaitingRoomController=1699688708~id=6b8e1423783b8921e58e3c7f473e425b; bm_sv=BB9422D2F2F866366D19CF4F4932BA8B~YAAQzONH0iWG/a6LAQAAI+ZSvRVD6CFZ4m6Uo/FbmAeEs5xc75gFf974VaQs4DOx86aW7yyI/L7N7Sunr9qDTOLrPed5TaL0GNz0XPgdLWnDbz4Xm698xgFS35KhS135WbYHswaNLTGo5POTPM38ejHeQ4h1beYY6FEYzqNIVDF/ztkGTv+4RP/wwsVsRQBCMHzuiXj3GpVpGMIB915Z8BvEFxPpN1aN6nlZRk7A29WSkideZPvyeW2A4sKWT7jm9ngifDnUhbP+~1',
        'Upgrade-Insecure-Requests': '1'
    }

    response = requests.request("GET", url,headers=headers, data=payload)

    print(page_number)


    soup = BeautifulSoup(response.text, 'html.parser')
    # print(soup)
    
    # len(soup.select('.part_number'))
    
    web_url_soup = soup.select('.product_item>.product_name>a')
    product_name_soup = soup.select('.product_item>.product_name')
    product_code_soup = soup.select('.product_item>.product_name>a')
    
    web_url_list = [i.get('href') for i in web_url_soup]
    product_name_list = [i.text for i in product_name_soup]
    product_code_list = [i.get('data-productcode') for i in product_code_soup]
    
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

# @timing_decorator
# def try_time():
        
lenovo_desktop = lenovo_crawl(keyword='Desktops')
lenovo_desktop.get_web_url()
lenovo_desktop.get_data_normal()
lenovo_desktop.clean()


lenovo_lap = lenovo_crawl(keyword='Laptops')
lenovo_lap.get_web_url()
lenovo_lap.get_data_normal()
lenovo_lap.clean()

lenovo_dock = lenovo_crawl(keyword='Docking')
lenovo_dock.get_web_url()
lenovo_dock.get_data_normal()
lenovo_dock.clean()


lenovo_thinksta = lenovo_crawl(keyword='thinkstation')
lenovo_thinksta.get_web_url_thinsta()
lenovo_thinksta.get_data_normal()
lenovo_thinksta.clean()

# try_time()



