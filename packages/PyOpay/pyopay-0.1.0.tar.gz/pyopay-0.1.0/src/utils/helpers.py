import hashlib
import hmac
import json

from opay.express_checkout.auth import private_key, public_key

import os
import hmac
import hashlib
from dotenv import load_dotenv

def private_key_signature(payload, secret_key=None, path=None):
    """Generate a signature using the private key."""
    if secret_key is None:
        auth_details = private_key(path=path)  # Pass path to private_key function
        secret_key = auth_details.get("private_key", "key not found")
        merchant_id = auth_details.get("merchant_id", "merchant_id not found")

    signature = hmac.new(secret_key.encode(), payload.encode(), hashlib.sha512).hexdigest()
    headers = {
        'Authorization': f'Bearer {signature}',
        'MerchantId': merchant_id,
        'Content-Type': 'application/json'
    }
    return headers

def public_key_signature(pub_key=None, path=None):
    """Generate headers using the public key."""
    if pub_key is None:
        auth_details = public_key(path=path)  # Pass path to public_key function
        pub_key = auth_details.get("pub_key", "key not found")
        merchant_id = auth_details.get("merchant_id", "merchant_id not found")

    headers = {
        'Authorization': f'Bearer {pub_key}',
        'MerchantId': merchant_id,
    }
    return headers

# secret_key = 'your_secret_key'
# merchant_id = '256612345678901'

# # Payload (data you want to send in the request)
# payload = '{"orderId": "12345", "amount": "1000"}'

# # Generate the signature using HMAC-SHA512
# signature = hmac.new(secret_key.encode(), payload.encode(), hashlib.sha512).hexdigest()

# # Set headers
# headers = {
#     'Authorization': f'Bearer {signature}',
#     'MerchantId': merchant_id,
#     'Content-Type': 'application/json'
# }

# # Send the request
# response = requests.post('https://api.opay.com/cashier/payment-status', headers=headers, data=payload)

# # Print response
# print(response.json())
