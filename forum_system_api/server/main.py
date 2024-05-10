from fastapi import FastAPI
from routers.user import users_router
from routers.topic import topics_router
from routers.reply import replies_router
from routers.category import category_router
from routers.message import message_router
# import uvicorn


app = FastAPI()


app.include_router(users_router)
app.include_router(topics_router)
app.include_router(replies_router)
app.include_router(category_router)
app.include_router(message_router)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)