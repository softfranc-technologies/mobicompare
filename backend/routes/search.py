"""
routes/search.py
"""
from fastapi import APIRouter, Query
from database import db
import re

router = APIRouter()

@router.get("/")
async def search_phones(q: str = Query(..., min_length=1), page: int = 1, per_page: int = 20):
    pattern = re.compile(re.escape(q), re.IGNORECASE)
    query = {"$or": [{"name": {"$regex": pattern}}, {"brand": {"$regex": pattern}}, {"specs.processor": {"$regex": pattern}}]}
    skip  = (page - 1) * per_page
    total = await db.mobiles.count_documents(query)
    phones = await db.mobiles.find(query).skip(skip).limit(per_page).to_list(per_page)
    for p in phones:
        mid = str(p["_id"]); p["id"] = mid; p.pop("_id", None)
        best = await db.prices.find_one({"mobile_id": mid}, sort=[("price", 1)])
        p["min_price"] = best["price"] if best else p.get("base_price", 0)
        p["image"] = (p.get("images") or [""])[0]
    return {"phones": phones, "total": total, "query": q, "page": page}

@router.get("/suggestions")
async def suggestions(q: str = Query(..., min_length=1)):
    pattern = re.compile(re.escape(q), re.IGNORECASE)
    phones  = await db.mobiles.find(
        {"$or": [{"name": {"$regex": pattern}}, {"brand": {"$regex": pattern}}]},
        {"name": 1, "brand": 1, "images": 1, "base_price": 1}
    ).limit(8).to_list(8)
    return [{"id": str(p["_id"]), "name": p["name"], "brand": p["brand"],
             "image": (p.get("images") or [""])[0], "base_price": p.get("base_price", 0)} for p in phones]
