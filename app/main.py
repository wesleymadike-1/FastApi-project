from fastapi import FastAPI
from app.routers import users, auth, post, like
from fastapi.middleware.cors import CORSMiddleware

# This function prints your name in ASCII when the script is loaded
def print_banner():
    banner = r"""
 _    _             _              ___  ___           _ _ _         
| |  | |           | |             |  \/  |          | (_) |        
| |  | | ___  ___  | | ___ _   _   | .  . | __ _  __| |_| | _____  
| |/\| |/ _ \/ __| | |/ _ \ | | |  | |\/| |/ _` |/ _` | | |/ / _ \ 
\  /\  /  __/\__ \ | |  __/ |_| |  | |  | | (_| | (_| | |   <  __/ 
 \/  \/ \___||___/ |_|\___|\__, |  \_|  |_/\__,_|\__,_|_|_|\_\___| 
                            __/ |                                  
                           |___/                                   
    """
    print(banner)
    print("🚀 WESLEY MADIKE API is starting up...")

print_banner()

description = """
### WESLEY MADIKE API 🚀
Professional API implementation using FastAPI, PostgreSQL, and SQLAlchemy.

#### Features:
* **Authentication**: Secure JWT-based login and token management.
* **User Management**: Complete CRUD operations for user profiles.
* **Social Engine**: Full support for creating posts and liking content.

---
"""

app = FastAPI(
    title="WESLEY MADIKE API",
    description=description,
    version="1.0.0",
    contact={
        "name": "Wesley Madike",
        "url": "https://github.com/wesleymadike-1/FastApi-project",
    },
)

# CORS Configuration
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routes
app.include_router(users.router)
app.include_router(auth.router)
app.include_router(post.router)
app.include_router(like.router)

@app.get("/", tags=["Root"])
async def root():
    return {"message": "Welcome to Wesley Madike's API. Visit /docs for documentation."}