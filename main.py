from ray import serve
from fastapi import FastAPI
from pydantic import BaseModel

class PnLItem(BaseModel):
    pnl: float

# Define a FastAPI app & wrap it in a deployment with a route handler.
app = FastAPI(
    title="Test API",
    description="API Test",
    version="0.1.0"
)

@serve.deployment
@serve.ingress(app)
class TestAPI:
    @app.get("/")
    async def root(self):
        return "Welcome to the API"

    @app.post("/double")
    async def double(self, request: PnLItem):
        pnl_value = request.pnl
        return {"pnl_double": pnl_value*2}
       
app = TestAPI.bind()

