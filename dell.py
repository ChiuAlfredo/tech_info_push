import requests
import json 


def search_page(keyword, page):
    url = "https://www.dell.com/en-us/search/desktop?p=2&t=Product"

    payload = {}
    headers = {
    'Content-Type': 'text/javascript',
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    print(response.text)
    
    json_data = json.loads(response.text)
    
    create_directory(f'data/hp/{file_name}_content/')
