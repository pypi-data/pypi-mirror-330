from utils.custom_error import Environment_Variable_Exception
import hashlib
import hmac
import os
from dotenv import load_dotenv, find_dotenv, set_key



class Auth:
    def __init__(self, public_key: str = None, merchant_id: str = None, private_key: str = None):
        """
        Initialize the Auth instance with optional public key, merchant ID, and private key.

        Args:
            public_key (str, optional): The public key for authentication. Defaults to None.
            merchant_id (str, optional): The merchant ID for authentication. Defaults to None.
            private_key (str, optional): The private key for generating signatures. Defaults to None.
        """

        self.pub_key = public_key
        self.merchant_id = merchant_id
        self.prv_key = private_key

    def get_env_value(self, var_name: str) -> str | None:
        """
        Retrieves the value of a specified environment variable from the .env file.

        Args:
            var_name (str): The name of the environment variable to retrieve.

        Returns:
            str | None: The value of the specified environment variable, or None if it does not exist.

        Raises:
            Environment_Variable_Exception: If the specified environment variable does not exist.
        """
        load_dotenv(find_dotenv())
        value = os.getenv(var_name)
        if value is None:
            raise Environment_Variable_Exception(
                f"Environment variable '{var_name}' not found. Please check your .env file."
            )
        return value

    def get_public_key(self) -> dict[str, str]:
        """
        Retrieves the public key and merchant ID from the .env file.

        Returns:
            dict[str, str]: A dictionary containing the public key and merchant ID.

        Raises:
            ValueError: If the public key or merchant ID is not found in the .env file.
        """
        if self.pub_key is None:
            self.pub_key = self.get_env_value("PUBLIC_KEY")
        if self.merchant_id is None:
            self.merchant_id = self.get_env_value("MERCHANT_ID")

        if self.pub_key and self.merchant_id:
            return {"pub_key": self.pub_key, "merchant_id": self.merchant_id}
        raise ValueError("Public key or merchant ID not found")

    def public_key_signature(self) -> dict[str, str]:
        """
        Generates a public key signature for authentication.

        If the public key is not already set, this method will retrieve the public key and merchant ID from the .env file.

        Returns:
            dict[str, str]: A dictionary containing the public key signature and merchant ID.
        """
        
        if self.pub_key is None:
            auth_details = self.get_public_key()
            self.pub_key = auth_details["pub_key"]
            self.merchant_id = auth_details["merchant_id"]

        return {
            'Authorization': f'Bearer {self.pub_key}',
            'MerchantId': self.merchant_id,
        }

    def get_private_key(self) -> dict[str, str]:
        """
        Retrieves the private key and merchant ID from the .env file.

        If the private key or merchant ID is not already set, this method will retrieve the private key and merchant ID from the .env file.

        Returns:
            dict[str, str]: A dictionary containing the private key and merchant ID.

        Raises:
            ValueError: If the private key or merchant ID is not found in the .env file.
        """
        if self.prv_key is None:
            self.prv_key = self.get_env_value("PRIVATE_KEY")
        if self.merchant_id is None:
            self.merchant_id = self.get_env_value("MERCHANT_ID")

        if self.prv_key and self.merchant_id:
            return {"prv_key": self.prv_key, "merchant_id": self.merchant_id}
        raise ValueError("Private key or merchant ID not found")

    def private_key_signature(self, payload: str) -> dict[str, str]:
        """
        Generates a signature using the private key.

        If the private key is not already set, this method will retrieve the private key and merchant ID from the .env file.

        Args:
            payload (str): The payload to sign.

        Returns:
            dict[str, str]: A dictionary containing the signature, merchant ID, and content type.

        Raises:
            ValueError: If the private key or merchant ID is not found in the .env file.
        """
        if self.prv_key is None:

            auth_details = self.get_private_key()
            self.prv_key = auth_details["prv_key"]
            self.merchant_id = auth_details["merchant_id"]

        signature = hmac.new(self.prv_key.encode(), payload.encode(), hashlib.sha512).hexdigest()
        return {
            'Authorization': f'Bearer {signature}',
            'MerchantId': self.merchant_id,
            'Content-Type': 'application/json'
        }




# Two auth methods involves passing the key straight into the Opay cashier class or with the auth method in the class 
