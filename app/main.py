from fastapi import FastAPI
from app.routers import users
description = """
Wesley's API helps you do awesome stuff. 🚀

## Items 
You can **read items**.
## Users
You will be able to:
* **Create users**.
* **Read users**.
"""

app = FastAPI(
    title="WESLEY MADIKE API",
    description=description,
)
app.include_router(users.router)