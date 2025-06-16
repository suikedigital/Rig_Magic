from fastapi import FastAPI, HTTPException, Request, Depends
from src.models import BaseUser, TradeUser, CustomerUser
import src.services as services
from src.database import initialize_db
from jose import jwt, JWTError
import os

app = FastAPI()

initialize_db()

# Use your real Auth.js secret or public key in production
AUTH_JS_SECRET = os.environ.get("AUTH_JS_SECRET", "your_authjs_secret")

# Dependency to extract user_id from JWT
def get_user_id_from_jwt(request: Request):
    auth = request.headers.get("Authorization")
    if not auth or not auth.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing or invalid token")
    token = auth.split(" ")[1]
    try:
        payload = jwt.decode(token, AUTH_JS_SECRET, algorithms=["HS256"])
        user_id = payload.get("sub")
        if not user_id:
            raise HTTPException(status_code=401, detail="User ID not found in token")
        return user_id
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

@app.get("/users/me", response_model=BaseUser)
def get_my_profile(user_id: str = Depends(get_user_id_from_jwt)):
    user = services.get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.get("/users/{user_id}", response_model=BaseUser)
def get_user(user_id: str):
    user = services.get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.post("/users/", response_model=BaseUser)
def create_user(user: BaseUser):
    services.save_user(user)
    return user

@app.put("/users/{user_id}", response_model=BaseUser)
def update_user(user_id: str, user: BaseUser):
    existing = services.get_user(user_id)
    if not existing:
        raise HTTPException(status_code=404, detail="User not found")
    services.save_user(user)
    return user

@app.delete("/users/{user_id}")
def delete_user(user_id: str):
    success = services.delete_user(user_id)
    if not success:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted"}

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/users/", response_model=list[BaseUser])
def list_users():
    return services.list_users()