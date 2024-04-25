from fastapi import FastAPI
# Vladi
from routers.user import users_router
# Elena
from routers.topic import topics_router
from routers.reply import replies_router
# Valkata
from routers.category import category_router
from routers.message import message_router

app = FastAPI()

# Vladi
app.include_router(users_router)
# Elena
app.include_router(topics_router)
app.include_router(replies_router)
# Valkata
app.include_router(category_router)
app.include_router(message_router)