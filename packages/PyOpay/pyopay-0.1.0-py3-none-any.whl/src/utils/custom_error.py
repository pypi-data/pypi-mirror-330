from typing import Optional
import utils.constants as constants

class Environment_Variable_Exception(Exception):
    def __init__ (self, variable_name):
        self.variable_name = variable_name
        super().__init__(f"Environment_Variable_Error: Variable missing {self.variable_name}")

class Environment_Exception(Exception):
    def __init__(self, environment) -> None:
        self.environment = environment
        super().__init__(f"Wrong Enviroment given: {self.environment}. Environment must either be production or development")


class Custom_Response:
    """Custom response class"""

    def success_response(self, data: dict, status_code: int = 200, code: str = "00000") -> dict:
        return {'status': 'success', 'data': data, "code": code, "status_code": status_code}

    def base_error_response(self, message: str, status_code: int, error_code: str) -> dict:
        return {'status': 'error', 'error': message, "status_code": status_code, "code": error_code}

    def failed_auth(self, message: str = constants.AUTHENTICATION_FAILED) -> dict:
        return self.base_error_response(message, status_code=401, error_code="02000")

    def invalid_params(self, message: str = constants.INVALID_PARAMAS) -> dict:
        return self.base_error_response(message, status_code=400, error_code="02001")

    def pay_method_error(self, message: str = constants.PAY_METHOD_ERROR) -> dict:
        return self.base_error_response(message, status_code=400, error_code="02003")

    def referance_exist(self, message: str = constants.ALREADY_EXISTS) -> dict:
        return self.base_error_response(message, status_code=409, error_code="02004")

    def merchant_not_config(self, message: str = constants.MERCHANT_NOTCONFIG) -> dict:
        return self.base_error_response(message, status_code=409, error_code="02002")

    def merchant_not_found(self, message: str = constants.MERCHANT_NOT_AVAILABLE) -> dict:
        return self.base_error_response(message, status_code=400, error_code="02007")

    def service_unavailable(self, message: str = constants.SERVICE_NOT_AVAILABLE) -> dict:
        return self.base_error_response(message, status_code=500, error_code="50003")
    def order_exists(self, message: str = constants.ORDER_EXISTS) -> dict:
        return self.base_error_response(message, status_code=409, error_code="00001")







class Opay_ResponseHandler(Custom_Response):
    def __init__(self, error_code: str):
        self.error_code = error_code
        self.response = self.get_response()

    def get_response(self) -> dict:
        error_map = {
            "02000": self.failed_auth,
            "02001": self.invalid_params,
            "02003": self.pay_method_error,
            "02004": self.referance_exist,
            "02002": self.merchant_not_config,
            "00001": self.order_exists,
            "02007": self.merchant_not_found,
            "50003": self.service_unavailable,
        }
        return error_map.get(self.error_code, lambda: {"status": "error", "message": "Unknown error"})()
