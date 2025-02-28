from .models import * 
from .auth import Auth
import utils.constants as constants
from utils.custom_error import Opay_ResponseHandler, Custom_Response
from typing import Optional, Any, Dict
import requests
from requests.exceptions import ConnectionError
import time



class Opay_Cashier:
    def __init__(self, environment: str = "sandbox", auth_keys: Optional[Dict[str, Any]] = None) -> None:
        """
        Initialize the Opay_Cashier instance with the specified environment and optional authentication keys.

        Args:
            environment (str): The operating environment for the Opay_Cashier instance, either "sandbox" or "production".
            auth_keys (Optional[Dict[str, Any]]): Optional dictionary containing authentication credentials.

        Raises:
            ValueError: If the environment is not "sandbox" or "production".
        """

        self.environment = environment
        self.auth_keys = auth_keys if auth_keys else {}
        self.auth = Auth(**self.auth_keys)

        
        # Accessing CASHIER_ENDPOINTS dictionary
        self.base_url = constants.CASHIER_ENDPOINTS.get(self.environment)
        
        if not self.base_url:
            raise ValueError("Invalid Environment: Environment should be 'sandbox' or 'production'")

    def authentication(self, public_key: Optional[str] = None, merchant_id: Optional[str] = None) -> dict:
        """
        Set or generate authentication keys for the Opay_Cashier instance.

        If the auth_keys attribute is empty, this method will validate and set the
        authentication keys using the provided arguments, or generate them
        using the public_key_signature function.

        Args:
            public_key (Optional[str]): The public key for authentication.
            merchant_id (Optional[str]): The merchant ID for authentication.

        Returns:
            dict: A dictionary containing the authentication keys.

        Raises:
            ValueError: If the required 'public_key' and 'merchant_id' are missing.
        """
        # Check if auth_keys are already set, otherwise validate the provided arguments
        if not self.auth_keys:
            # Ensure both 'public_key' and 'merchant_id' are provided
            if public_key and merchant_id:
                self.auth_keys = {
                    "Content-Type": "application/json",
                    "Authorization": f"Bearer {public_key}",
                    "MerchantId": merchant_id
                }
            else:
                # Generate keys using public_key_signature if no arguments are provided, to use this function, it must have been passed in the Opay_Cashier class initalization. 
                self.auth_keys = self.auth.public_key_signature()

                # Verify that the generated headers contain the required fields
                if 'Authorization' not in self.auth_keys or 'MerchantId' not in self.auth_keys:
                    raise ValueError("Authentication failed: Required 'public_key' and 'merchant_id' are missing.")
        print(self.auth_keys)
        return self.auth_keys
    

    # def __repr__(self) -> str:
    #     return (f"Opay_Cashier(environment: {self.environment}, auth_keys: {self.auth_keys}, "
    #             f"base_url: {self.base_url})")

    def request(self, payload: dict) -> dict:
        # Validate and prepare the payload
        self.payload: Params = Params(**payload)  
        self.data = self.payload.model_dump()
        
        # Authenticate and set headers
        self.auth_keys = self.authentication()  # This ensures headers are set or generated correctly

        #To-do: error handling for failed connection
        self.response = requests.post(
        url= self.base_url, json=self.data, headers=self.auth_keys)
        data = self.response.json()
        if data["code"] != "00000":
            error = Error(**data).model_dump()
            error_code = error["code"]
            opay_handler = Opay_ResponseHandler(error_code=error_code)
            # print (opay_handler.response)
            return opay_handler.get_response()

        else:
            #print(data)
            res = Response(**data).model_dump()
            success =Custom_Response()
            response = success.success_response(res)
            print(response)
            
       
