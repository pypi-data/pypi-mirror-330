CASHIER_ENDPOINTS = {
    'sandbox': "https://testapi.opaycheckout.com/api/v1/international/cashier/create",

    'production': "https://api.opaycheckout.com/api/v1/international/cashier/create"
}

PAYMENT_STATUS = {
    'sandbox': "https://sandboxapi.opaycheckout.com/api/v1/international/cashier/status",
    'production': "https://api.opaycheckout.com/api/v1/international/cashier/status"
}

ORDER_EXISTS = "Order already exists"
AUTHENTICATION_FAILED = "authentication failed"
INVALID_PARAMAS = "request parameters not valid"
PAY_METHOD_ERROR = "payMethod not supported"
ALREADY_EXISTS = "the payment reference(merchant order number) already exists."
MERCHANT_NOTCONFIG = "merchant not configured with this function."
MERCHANT_NOT_AVAILABLE = "merchant not available"
SERVICE_NOT_AVAILABLE = "service not available, please try again."
