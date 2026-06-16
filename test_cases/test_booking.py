import allure
import pytest
from lib.api_client import APIClient


@allure.feature("预订接口")
class TestBooking:

    @allure.story("创建预定")
    @allure.title("创建新的预定")
    def test_create_booking(self, api_client: APIClient):
        """测试创建新的预定记录"""
        payload = {
            "firstname": "Meili",
            "lastname": "Dong",
            "totalprice": 888,
            "depositpaid": True,
            "bookingdates": {
                "checkin": "2026-01-01",
                "checkout": "2026-01-10"
            },
            "additionalneeds": "Breakfast"
        }
        response = api_client.post("/booking", json=payload)
        assert response.status_code == 200
        booking_data = response.json()
        assert "bookingid" in booking_data
        assert booking_data['booking']['firstname'] == "Meili"

    @allure.story("查询预定")
    @allure.title("根据ID查询预定")
    def test_get_booking_by_id(self, api_client: APIClient):
        """先创建一个预定记录，然后根据ID查询"""
        create_payload = {
            "firstname": "Test",
            "lastname": "User",
            "totalprice": 100,
            "depositpaid": False,
            "bookingdates": {
                "checkin": "2026-02-01",
                "checkout": "2026-02-05"
            },
        }
        create_response = api_client.post("/booking", json=create_payload)
        booking_id = create_response.json()["bookingid"]
        allure.attach(str(booking_id), "创建的预定ID", allure.attachment_type.TEXT)

        # 查询预定
        get_response= api_client.get(f"/booking/{booking_id}")
        assert get_response.status_code == 200
        fetched_booking = get_response.json()
        assert fetched_booking["firstname"] == create_payload["firstname"]
        assert fetched_booking["bookingdates"]["checkin"] == create_payload["bookingdates"]["checkin"]

    @allure.story("更新预定")
    @allure.title("使用PUT方法完全更新预定【需要认证】")
    def test_update_booking(self, api_client: APIClient, auth_token):
        """测试完全更新一个预定记录"""
        # 1,先创建预定,并获取id
        create_payload = {
            "firstname": "Yezi",
            "lastname": "Zhi",
            "totalprice": 405,
            "depositpaid": False,
            "bookingdates": {
                "checkin": "2026-03-01",
                "checkout": "2026-03-05"
            },
        }
        create_response = api_client.post("/booking", json=create_payload)
        booking_id = create_response.json()["bookingid"]
        allure.attach(str(booking_id), "Booking ID", allure.attachment_type.TEXT)
        # 2,准备更新数据
        update_payload = {
            "firstname": "chapai",
            "lastname": "Nong",
            "totalprice": 220,
            "depositpaid": True,
            "bookingdates": {
                "checkin": "2026-03-02",
                "checkout": "2026-03-06"
            },
            "additionalneeds": "Lunch"
        }

        # 3, 使用PUT方法更新预定，需要在请求头中带上Cookie token
        # 为了方便直接使用session对象设置cookie
        api_client.session.cookies.set("token", auth_token)
        update_response = api_client.put(f"/booking/{booking_id}", json=update_payload)
        assert update_response.status_code == 200
        update_data = update_response.json()
        assert update_data["firstname"] == update_payload["firstname"]
        assert update_data["totalprice"] == update_payload["totalprice"]

    @allure.story("删除预定")
    @allure.title("删除特定预定【需要认证】")
    def test_delete_booking(self, api_client: APIClient, auth_token):
        """测试删除一个预定"""
        # 1，还是先创建一个预定记录，并获取ID
        create_payload = {
            "firstname": "Shanchu",
            "lastname": "Del",
            "totalprice": 405,
            "depositpaid": False,
            "bookingdates": {
                "checkin": "2026-03-01",
                "checkout": "2026-03-05"
            },
        }
        create_response = api_client.post("/booking", json=create_payload)
        booking_id = create_response.json()["bookingid"]
        # 2，使用DELETE方法删除预定，断言删除成功，状态码201
        api_client.session.cookies.set("token", auth_token)
        del_response = api_client.delete(f"/booking/{booking_id}")
        assert del_response.status_code == 201

        # 3，删除后再次通过GET查询，断言状态码404
        get_response = api_client.get(f"/booking/{booking_id}")
        assert get_response.status_code == 404
