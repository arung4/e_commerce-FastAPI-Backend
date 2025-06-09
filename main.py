from fastapi import FastAPI
from typing import Optional
from pydantic import BaseModel
from config.database import engine, Base
from auth.routes import router as auth_router 
from products.routes import router as product_router
# import uvicorn

app = FastAPI()

# Create all tables 
Base.metadata.create_all(bind = engine)

# Include all API routers 
app.include_router(auth_router)
app.include_router(product_router)

@app.get("/") # path operation decorator 
def app_start(): 
    return {'data': "Welcome to My E-Commerce App"}



# if __name__ == "__main__": 
#     uvicorn.run(app,host="127.0.0.1",port=9000)

