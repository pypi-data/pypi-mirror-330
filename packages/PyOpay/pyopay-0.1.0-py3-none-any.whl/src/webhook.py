import fastapi
from opay.express_checkout.models import Callback

app = fastapi.FastAPI()

@app.post("/callback/")
def webhook_func(data:Callback):
    print ({"message":"sucess", "data": f"{data.model_dump()}"}
)
@app.post("/cancelurl")
def cancel(data:Callback):
    return {"message":"sucess", "data": f"{data}"}

@app.post("/returnurl")
def returnUrl(data:Callback):
    return {"message":"sucess", "data": f"{data}"}


