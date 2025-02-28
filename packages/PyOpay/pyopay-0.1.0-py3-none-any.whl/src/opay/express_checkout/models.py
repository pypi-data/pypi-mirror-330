from enum import Enum
from pydantic import BaseModel, EmailStr
from typing import List, Optional
import json
class Amount(BaseModel):
    total: int
    currency: str


class ProductList(BaseModel):
    productId: str
    name: str
    description: str
    price: int
    quantity: int
    imageUrl: Optional[str] = None

class UserModel(BaseModel):
    userId: Optional[str] = None
    userName: Optional[str] = None
    userMobile: Optional[str] = None
    userEmail: Optional[EmailStr] = None

class Product(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None

class Params(BaseModel):
    reference: str
    country: str
    amount: Amount
    callbackUrl: Optional[str] = None
    returnUrl: str
    productList: List[ProductList]
    cancelUrl: Optional[str] = None
    userClientIP: Optional[str] = None
    expireAt: Optional[int] = None
    userInfo: UserModel
    product: Optional[Product] = None
    payMethod: Optional[str] = None



class Status(Enum):
    INITIAL = "INITIAL"
    PENDING = "PENDING"
    SUCCESS = "SUCCESS"
    FAIL = "FAIL"
    CLOSE = "CLOSE"

class Error(BaseModel):
    code: str
    message: str

class ResponseData(BaseModel):
    reference: str
    orderNo: str
    cashierUrl: str
    status: Status
    amount: Amount
    vat: Amount
class Response(BaseModel):
    code: str
    message: str
    data: ResponseData

class Callbackpayload(BaseModel):
    country: str
    fee: str
    displayedFailure: str
    reference: str
    updated_at: str
    currency: str
    feeCurrency: str
    refunded: bool
    timestamp: str
    amount: str
    transactionId: str
    instrumentType: str
    status: str

class Callback(BaseModel):
    payload: Callbackpayload
    sha512: str
    type: str

# {
#    "payload":{
#       "amount":"49160",
#       "channel":"Web",
#       "country":"NG",
#       "currency":"NGN",
#       "displayedFailure":"",
#       "fee":"737",
#       "feeCurrency":"NGN",
#       "instrumentType":"BankCard",
#       "reference":"10023",
#       "refunded":false,
#       "status":"SUCCESS",
#       "timestamp":"2022-05-07T06:20:46Z",
#       "token":"220507145660712931829",
#       "transactionId":"220507145660712931829",
#       "updated_at":"2022-05-07T07:20:46Z"
#    },
#    "sha512":"9f605d69f04e94172875dc156537071cead060bbcaeaca94a7b8805af9f89611e2fdf6836713c9c90b028ca7e4470b1356e996975f2abc862315aaa9b7f2ae2d",
#    "type":"transaction-status"
# }
