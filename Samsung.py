import requests

url = "https://www.samsung.com/us/api/es_search_global/global/result_v2.json?searchTerm=Book&size=20&from=40"

payload = {}
headers = {
  'Cookie': 'country_codes=jp; country_region=CA-ON; device_type=pc; s_fpid=040bc53a-8eb9-4e9e-ab8e-a233a5b840b0'
}

response = requests.request("GET", url, headers=headers, data=payload)

data = response.json()