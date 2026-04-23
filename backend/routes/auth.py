"""
routes/auth.py
"""
from fastapi import APIRouter, HTTPException, Depends
from database import db
from models import UserRegister, UserLogin, Token, UserOut
from auth_utils import hash_password, verify_password, create_access_token, get_current_user
from datetime import datetime
from bson import ObjectId

router = APIRouter()

@router.post("/register", response_model=Token, status_code=201)
async def register(data: UserRegister):
    if await db.users.find_one({"email": data.email}):
        raise HTTPException(400, "Email already registered")
    doc = {"name": data.name, "email": data.email, "password": hash_password(data.password),
           "is_admin": False, "created_at": datetime.utcnow()}
    result = await db.users.insert_one(doc)
    user_id = str(result.inserted_id)
    token = create_access_token({"sub": user_id, "email": data.email})
    return Token(access_token=token, user=UserOut(id=user_id, name=data.name, email=data.email))

@router.post("/login", response_model=Token)
async def login(data: UserLogin):
    user = await db.users.find_one({"email": data.email})
    if not user or not verify_password(data.password, user["password"]):
        raise HTTPException(401, "Invalid email or password")
    user_id = str(user["_id"])
    token = create_access_token({"sub": user_id, "email": data.email})
    return Token(access_token=token, user=UserOut(id=user_id, name=user["name"], email=user["email"]))

@router.get("/me", response_model=UserOut)
async def me(current_user: dict = Depends(get_current_user)):
    return UserOut(id=str(current_user["_id"]), name=current_user["name"], email=current_user["email"])

@router.post("/wishlist/{mobile_id}")
async def toggle_wishlist(mobile_id: str, current_user: dict = Depends(get_current_user)):
    user_id = str(current_user["_id"])
    existing = await db.wishlist.find_one({"user_id": user_id, "mobile_id": mobile_id})
    if existing:
        await db.wishlist.delete_one({"_id": existing["_id"]})
        return {"action": "removed"}
    await db.wishlist.insert_one({"user_id": user_id, "mobile_id": mobile_id, "added_at": datetime.utcnow()})
    return {"action": "added"}

@router.get("/wishlist")
async def get_wishlist(current_user: dict = Depends(get_current_user)):
    user_id = str(current_user["_id"])
    items = await db.wishlist.find({"user_id": user_id}).to_list(200)
    mobile_ids = [i["mobile_id"] for i in items]
    phones = await db.mobiles.find({"_id": {"$in": [ObjectId(i) for i in mobile_ids]}}).to_list(200)
    for p in phones:
        mid = str(p["_id"]); p["id"] = mid; p.pop("_id", None)
        best = await db.prices.find_one({"mobile_id": mid}, sort=[("price", 1)])
        p["min_price"] = best["price"] if best else p.get("base_price", 0)
        p["image"] = (p.get("images") or [""])[0]
    return phones
