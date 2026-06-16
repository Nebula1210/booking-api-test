import requests
import allure
from config.settings import BASE_URL, TIMEOUT


class APIClient:
    def __init__(self, base_url=BASE_URL, timeout=TIMEOUT):
        self.base_url = base_url
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({"Content-Type":"application/json"})

    @allure.step("发送GET请求:{endpoint}")
    def get(self, endpoint,query=None,**kwargs):
        url = f"{self.base_url}{endpoint}"
        response = self.session.get(url, params=query, timeout=TIMEOUT,**kwargs)
        return response
    
    @allure.step("发送POST请求:{endpoint}")
    def post(self, endpoint,data=None,json = None,**kwargs):
        url = f"{self.base_url}{endpoint}"
        response = self.session.post(url,data=data,json = json,timeout = TIMEOUT,**kwargs)
        return response
    
    @allure.step("发送PUT请求:{endpoint}")
    def put(self, endpoint,data=None,json = None,**kwargs):
        url = f"{self.base_url}{endpoint}"
        response = self.session.put(url,data=data,json = json,timeout = TIMEOUT,**kwargs)
        return response
    
    @allure.step("发送DELETE请求:{endpoint}")
    def delete(self, endpoint,**kwargs):
        url = f"{self.base_url}{endpoint}"
        response = self.session.delete(url,timeout = TIMEOUT,**kwargs)
        return response


