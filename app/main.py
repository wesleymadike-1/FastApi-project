from fastapi import FastAPI
from app.routers import users
from fastapi.middleware.cors import CORSMiddleware

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

origins = [
    # "http://localhost:3000",
    # "http://127.0.0.1:8000",
    "*"
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users.router)