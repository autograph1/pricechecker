import requests
def parse_ozon(url):
    response = requests.get(url)
    print(response.status_code)