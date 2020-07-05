import time
import requests
from fake_useragent import UserAgent

ua = UserAgent(verify_ssl=False)
headers = {
    'User-Agent': ua.random,
    'Referer'   : 'https://shimo.im/login?from=home',
    'Origin'    : 'https://shimo.im',
    'Host'      : 'shimo.im',
    'TE'        : 'Trailers',
    'Upgrade-Insecure-Requests' : '1',
}

with requests.Session() as s:
    login_page_url = 'https://shimo.im/login?from=home'
    response = s.get(login_page_url, headers = headers)
    print(response.status_code)
    print(s.cookies)

    login_url = 'https://shimo.im/lizard-api/auth/password/login'
    form_data = {
        'mobile': '+8613434343434',
        'password': '341234',
    }
    response2 = s.post(login_url, data = form_data, headers = headers, cookies = s.cookies)
    print(response2.status_code)
    print(response2.text)