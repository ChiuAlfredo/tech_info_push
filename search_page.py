#%% 
# dell
import requests

url = "https://www.dell.com/en-us/search/desktop?p=2&t=Product&r=36679"#TODO 替換關鍵字 頁數

payload = {}
headers = {
  'Content-Type': 'text/javascript',
  'Cookie': 'DellCEMSession=394BF46C26CFE737585C8E39655C084E; _abck=DB03C213CA96D7A9C05F183785A7E742~-1~YAAQw4pFy25Z062LAQAAZH/grgoGTtbFCY4TxKxpgK0se8JJT8YR2kENE8nhe1YaMKt0kCBqe8VISoZvbaKLygZ9woDC9AYZULKsGimEaBHoZLSPv+lqvT+cqcc+Bvm5BWyR3DophXFO3wtKD/Sgt8yt7o+bBMY2FDPSCZHECQdwT7xiQk/NMzPcDUkqwNFBoanVKr1Nt3WGHCOkTTXf96C21t2welT9aHtlDZKJ8oO/vZ6oby0mN/qktl4Ot9SNJuvXjorHi82EkOcLtH90Esj1Qk/o66KlGkkHTIXbfOzGgwOayzyqeC42mw7cam71iTjp0bhKKx7eiUsuKrbxzWx0627JjtmJbmUnlMtsNmU/inxTPNu3WkJ/BUlF1Y9ElZVClWiDuQucoV2qsYEER+runeKbLP0=~-1~-1~1697444404; akGD=%7B%22country%22%3A%22TW%22%2C%22region%22%3A%22%22%7D; bm_sz=2A0E19E702030D05B579D07C4981A251~YAAQw4pFy29Z062LAQAAZH/grhVE5nzXEQbCs06nzfBEJgW7GLxZviysfPgQlexEa1sqeJXgh6e7lXOIRqxcSgY+qpZX+XZJonqRc2OYEtvJXnHeM7Wl+27zhew5J6iLcGv9SCzCtqqr6szXI+duV8jIHt1Wk0Yn4uphWZbwe3WUAIUg1FIq1SQNf7nmyAPaw04J+2tPTDB5Jwi1c0TWrO9saKjJtaIewhEi7fv17G1mOQUzT+mJiQCV+GkUllk+plJCDR4ET1A0T7nlu5H3B8qGG1uOK8HIl/FNyCu36EaI~3749186~4601648; dais-c=9dphbC5OzAb9/BqDJj8tcOBOEDnK6fF0rq3DeSmw8ZEsusM3A8AFkMqzykR6LY/yrcucsgrQSIobp0hz5Iqqww==; dc-ctxt=c=US&l=en; lwp=c=us&l=en&s=bsd&cs=04; lwprofile=c=us&l=en&s=bsd&cs=04; search-visitorId=9b689250-bef0-4d9e-a28d-ffa60f9ac044; um_g_uc=false; akaas_dell_com_configure_unifiedpd_splits=1699770013~rv=73~id=ea9ecc81f9c2fbb5093e562f572bbedf; akaas_dell_com_product_search_us=1702038044~rv=14~id=61c1135ab4bc2c1a9340437e1e119ea0; akavpau_maintenance_vp=1699446344~id=c34560549240dd6136f5d696b86d879d'
}

response = requests.request("GET", url, headers=headers, data=payload)

print(response.text)

#%%
#hp 
import requests
import json

url = "https://essearchapi-na.hawksearch.com/api/v2/search"

payload = json.dumps({
  "query": "type:product",
  "ClientData": {
    "VisitId": "394bbe69-22cc-4975-82df-0a1fad7e3114",
    "VisitorId": "91e30d9a-9dfb-4dfc-8ce2-1198c18496c3",
    "UserAgent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    "Custom": {}
  },
  "Keyword": "desktop",#TODO需要更改
  "PageNo": 1,#根據數量換頁
  "ClientGuid": "bdeebee3d2b74c8ea58522bb1db61f8e"
})
headers = {
  'Content-Type': 'application/json',
  'Accept': 'application/json, text/plain, */*'
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)

#%% lenovo

import requests

url = "https://openapi.lenovo.com/us/en/ofp/search/dlp/product/query/get/_tsc?pageFilterId=a7b024c8-a164-4c56-b65e-0c20fe323ada&subSeriesCode=thinkpad&params=%257B%2522classificationGroupIds%2522%253A%2522400001%2522%252C%2522pageFilterId%2522%253A%2522a7b024c8-a164-4c56-b65e-0c20fe323ada%2522%252C%2522facets%2522%253A%255B%257B%2522facetId%2522%253A%2522698%2522%252C%2522selectedValues%2522%253A%2522ThinkBook%2522%257D%255D%252C%2522page%2522%253A%25221%2522%252C%2522pageSize%2522%253A20%252C%2522init%2522%253Atrue%252C%2522sorts%2522%253A%255B%2522bestSelling%2522%255D%252C%2522version%2522%253A%2522v2%2522%252C%2522subseriesCode%2522%253A%2522%2522%257D"

payload = {}
headers = {

  'Cookie': '_abck=59A87B51A6012FB04230CDD8549B5C12~-1~YAAQgIpFy6bH/amLAQAAeA/irgq3FEU6IqK2Uvm2epd/5+0AvyU06SgL/TTve3jrv46HNDHBhOd2Sz309WGVVQ6gk58gyBwsGCW6aSB5SxNLg4L1lNQkkiUlmMtSI2kKArwb8ZyJgPd5/Ce3Dcg7c8arJFCPYyily57HUTpK9LLeRBmeKz8kMDavCKkTJH7hT5NZl6AH8tDZzF6YHVIcvF4Kcq1YRwoN165Eay5W4qimWckRZ7JJFKwO1o5R4k2P4jfID3LviyrYShmWun0AqWnZUVTJF6kppjAfMjrbBxquQgcp4JglgkBmaCqafc9vxYGuAfNQwmFxgVc77XT0DCGGbE/WPBFIjMH5+LEtNwwmuMxWp5CDZgAERt4ROyct+BBNxVCC0g==~-1~-1~1696560139; ak_bmsc=08DEE7BC6E956A4F69A3FAC724096385~000000000000000000000000000000~YAAQgIpFyzDN/amLAQAAKWvirhWECerPtsAJBR/LcQ64p/ZQwyR4vbzogcUEK6fbr3k2vm4+2kybJUtb9mJS0S4Zd24IkWDbN+evwwuK0yZdiVeMTIYGntBAZM277EmSWcdu6YZ8QBWUt8D561jlE0YQsUBFEufZ+yn8iZBbHqqv5Khar/nzfAfo1yoc5se28i+fY4BonJnWmKE+NWuia1loV6cZg73AOPPlI6vMTzVS8J+9RWQkl2tjQWdtQZfy8UB7XfpiE80givVXRuYsrRAxqC2j2CCcEDdlEEgt7GPogLR0oH3Ufn54mDhf1XYhTpCaf2xglx6KITOVpj+A/UYQ55jzXU1NedVlzsMTR1kdUBPmTznghCah7A==; bm_sv=4C95BD42649B612C360FA28651EC6FAE~YAAQgIpFy0zi/amLAQAAr0jjrhW4Djqmuay3hL2GPA+khtBcKqoiEZ2rJXdtLuxvvji04efZ6WU/vhYI2Ys1qdl8B2Rc37GN4J09tPfdsS/v33T+jBpNf4Yj/n9klS8bLGOEBBaQ6IWSM+ZEKZpSEb08NzrpfP2iFNPBb4cwHSepjGIFowGgugA0uQuwBadHQ+MgfmQnHFPUztyStXbL/BVIyJGJWHTnsT6LgbEkRuWwHqZI0z4le7COiBYVSRnz~1; bm_sz=DF0A5189AFE4470B3F8182C5584CAF3D~YAAQgIpFy6fH/amLAQAAeA/irhUzvGzarDsWaM9lKvjzS4olZ1TD44M8N4ZCAeGAGttGLbecgqFy8fdHJvqGALiG3Ab2ZkaLo1h91OKw54ZN2BpMcbeJusUcByrThkg0kjazlvOZXTPNAJZkLBcHLG93EnQRnU3acXPsYiB/EUQqqG3sDjV5r61F0lHDB6QKQPZ2Q3mcYTYdr62C6PAMF7Ihdw20p9rXOydFk44RZwWk1+J3jacrtHWybRBg01tqnw1VbQtMoRBn/J81vjARKWSqgDAUasBZpMjaVLnoIS1cbb4=~4534582~4342341; leid=2.R9uqqRVdUnu',
  'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',

}

response = requests.request("GET", url, headers=headers, data=payload)

print(response.text)
