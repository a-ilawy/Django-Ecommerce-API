import requests
from django.conf import settings
import hashlib
import hmac

BASE_URL = "https://accept.paymob.com/api"

def get_auth_token():
    url = f"{BASE_URL}/auth/tokens"
    response = requests.post(url, json={"api_key": settings.PAYMOB_API_KEY})
    return response.json()["token"]


def create_paymob_order(auth_token, amount_cents):
    url = f"{BASE_URL}/ecommerce/orders"
    data = {
        "auth_token": auth_token,
        "delivery_needed": False,
        "amount_cents": amount_cents,
        "currency": "EGP",
        "items": []
    }
    response = requests.post(url, json=data)
    return response.json()["id"]


def generate_payment_key(auth_token, order_id, amount_cents, billing_data):
    url = f"{BASE_URL}/acceptance/payment_keys"
    data = {
        "auth_token": auth_token,
        "amount_cents": amount_cents,
        "expiration": 3600,
        "order_id": order_id,
        "billing_data": billing_data,
        "currency": "EGP",
        "integration_id": settings.PAYMOB_INTEGRATION_ID
    }
    response = requests.post(url, json=data)
    return response.json()["token"]



def verify_paymob_hmac(data):
    PAYMOB_HMAC = settings.PAYMOB_HMAC_SECRET

    KEYS = [
        "amount_cents",
        "created_at",
        "currency",
        "error_occured",
        "has_parent_transaction",
        "id",
        "integration_id",
        "is_3d_secure",
        "is_auth",
        "is_capture",
        "is_refunded",
        "is_standalone_payment",
        "is_voided",
        "order",
        "owner",
        "pending",
        "source_data.pan",
        "source_data.sub_type",
        "source_data.type",
        "success",
    ]

    concatenated = ""

    for key in KEYS:
        if "." in key:
            main, sub = key.split(".")
            value = data.get(main + "." + sub, "")
        else:
            value = data.get(key, "")
        concatenated += str(value)

    generated_hmac = hmac.new(
        PAYMOB_HMAC.encode(),
        concatenated.encode(),
        hashlib.sha512
    ).hexdigest()

    return generated_hmac == data.get("hmac")
