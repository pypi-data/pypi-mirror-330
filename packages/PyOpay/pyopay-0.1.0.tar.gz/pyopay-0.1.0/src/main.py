import json
#from opay.auth import public_key_signature
from opay.express_checkout.opay_cashier import Opay_Cashier
from opay.express_checkout.models import Params
from pathlib import Path
# # Get the path to the .env file located 3 directories up from the current file
# path = Path(__file__).resolve().parent.parent / '.env'

from dotenv import dotenv_values

# Load as a dictionary (doesn't affect os.environ)
config = dotenv_values()
public_key = config["PUBLIC_KEY"]
merchant_id = config["MERCHANT_ID"]

data = "utils/data.json"
with open(data, mode="r") as file:
    loaded_data = json.load(file)

app = Opay_Cashier()
app.authentication(
    public_key=public_key, 
    merchant_id=merchant_id
)
print(app.request(payload=loaded_data))

#d = Params(**loaded_data)
# da = d.model_dump()
# print(json.dumps(da, indent=4))
##print(app)
