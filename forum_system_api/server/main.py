from fastapi import FastAPI
from routers.user import users_router


app = FastAPI()

app.include_router(users_router)
