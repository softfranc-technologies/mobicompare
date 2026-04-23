"""
routes/mobiles.py — CRUD for phones + price attachment
"""
from fastapi import APIRouter, HTTPException, Query, Depends
from typing import Optional, List
from bson import ObjectId
from database import db
from models import MobileCreate, SortBy, BadgeType
from auth_utils import require_admin
import math

router = APIRouter()

SORT_MAP = {
    "popular":    [("reviews", -1)],
    "price-low":  [("base_price", 1)],
    "price-high": [("base_price", -1)],
    "rating":     [("rating", -1)],
    "newest":     [("year", -1), ("created_at", -1)],
}

def _oid(id_str: str):
    try:
        return ObjectId(id_str)
    except Exception:
        raise HTTPException(400, "Invalid phone ID")

async def _enrich(phone: dict) -> dict:
    mid = str(phone.get("_id", phone.get("id", "")))
    phone["id"] = mid
    phone.pop("_id", None)
    sellers = await db.prices.find({"mobile_id": mid}).sort([("price", 1)]).to_list(20)
    for s in sellers:
        s["id"] = str(s.pop("_id"))
    phone["sellers"]      = sellers
    phone["min_price"]    = sellers[0]["price"] if sellers else phone.get("base_price", 0)
    phone["seller_count"] = len(sellers)
    phone["image"]        = (phone.get("images") or [""])[0]
    return phone


# ── GET /api/mobiles ──────────────────────────────────────────────────────────
@router.get("/")
async def list_mobiles(
    page:       int            = Query(1, ge=1),
    per_page:   int            = Query(24, ge=1, le=100),
    sort:       SortBy         = Query(SortBy.popular),
    brand:      Optional[str]  = None,
    min_price:  Optional[int]  = None,
    max_price:  Optional[int]  = None,
    ram:        Optional[str]  = None,
    storage:    Optional[str]  = None,
    five_g:     Optional[bool] = None,
    min_rating: Optional[float]= None,
    badge:      Optional[BadgeType] = None,
):
    query: dict = {}
    if brand:      query["brand"]         = {"$in": brand.split(",")}
    if badge:      query["badge"]         = badge.value
    if min_price:  query["base_price"]    = {"$gte": min_price}
    if max_price:  query.setdefault("base_price", {})["$lte"] = max_price
    if ram:        query["specs.ram"]     = {"$in": ram.split(",")}
    if storage:    query["specs.storage"] = {"$in": storage.split(",")}
    if five_g is not None: query["specs.fiveG"] = five_g
    if min_rating: query["rating"]        = {"$gte": min_rating}

    sort_spec = SORT_MAP.get(sort.value, SORT_MAP["popular"])
    total = await db.mobiles.count_documents(query)
    skip  = (page - 1) * per_page

    cursor = db.mobiles.find(query).sort(sort_spec).skip(skip).limit(per_page)
    phones = await cursor.to_list(per_page)
    phones = [await _enrich(p) for p in phones]

    return {"phones": phones, "total": total, "page": page, "pages": math.ceil(total / per_page)}


# ── GET /api/mobiles/trending ─────────────────────────────────────────────────
@router.get("/trending")
async def trending(limit: int = Query(8, le=20), category: Optional[str] = None):
    query: dict = {}
    if category == "flagship": query["base_price"] = {"$gte": 60000}
    elif category == "mid":    query["base_price"] = {"$gte": 20000, "$lt": 60000}
    elif category == "budget": query["base_price"] = {"$lt": 20000}
    elif category == "5g":     query["specs.fiveG"] = True
    else:                      query["badge"] = "hot"

    phones = await db.mobiles.find(query).sort([("rating", -1)]).limit(limit).to_list(limit)
    return [await _enrich(p) for p in phones]


# ── GET /api/mobiles/latest ───────────────────────────────────────────────────
@router.get("/latest")
async def latest(limit: int = Query(6, le=20)):
    phones = await db.mobiles.find({"badge": {"$in": ["new", "hot"]}}).sort(
        [("year", -1), ("created_at", -1)]
    ).limit(limit).to_list(limit)
    return [await _enrich(p) for p in phones]


# ── GET /api/mobiles/budget ───────────────────────────────────────────────────
@router.get("/budget")
async def budget(limit: int = Query(6, le=20)):
    phones = await db.mobiles.find({"base_price": {"$lte": 20000}}).sort(
        [("base_price", 1)]
    ).limit(limit).to_list(limit)
    return [await _enrich(p) for p in phones]


# ── GET /api/mobiles/brands ───────────────────────────────────────────────────
@router.get("/brands")
async def brands():
    pipeline = [
        {"$group": {"_id": "$brand", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}}
    ]
    result = await db.mobiles.aggregate(pipeline).to_list(50)
    return [{"brand": r["_id"], "count": r["count"]} for r in result]


# ── GET /api/mobiles/ticker ───────────────────────────────────────────────────
@router.get("/ticker")
async def ticker(limit: int = Query(16, le=30)):
    """Data for the trending price marquee."""
    phones = await db.mobiles.find({}).limit(limit).to_list(limit)
    out = []
    for p in phones:
        mid = str(p["_id"])
        best = await db.prices.find_one({"mobile_id": mid}, sort=[("price", 1)])
        price = best["price"] if best else p.get("base_price", 0)
        out.append({
            "id":    mid,
            "name":  f"{p['brand']} {p['name']}",
            "price": price,
            "trend": "up" if p.get("badge") in ("hot", "new") else "down",
        })
    return out


# ── GET /api/mobiles/{id} ─────────────────────────────────────────────────────
@router.get("/{phone_id}")
async def get_mobile(phone_id: str):
    phone = await db.mobiles.find_one({"_id": _oid(phone_id)})
    if not phone:
        raise HTTPException(404, "Phone not found")
    phone = await _enrich(phone)
    phone["reviews_list"] = await db.reviews.find(
        {"mobile_id": phone_id}
    ).sort([("created_at", -1)]).limit(10).to_list(10)
    for r in phone["reviews_list"]:
        r["id"] = str(r.pop("_id"))
    return phone


# ── POST /api/mobiles (admin) ─────────────────────────────────────────────────
@router.post("/", status_code=201, dependencies=[Depends(require_admin)])
async def create_mobile(data: MobileCreate):
    from datetime import datetime
    doc = data.model_dump()
    doc["created_at"] = datetime.utcnow()
    result = await db.mobiles.insert_one(doc)
    return {"id": str(result.inserted_id), "message": "Phone created"}


# ── PUT /api/mobiles/{id} (admin) ─────────────────────────────────────────────
@router.put("/{phone_id}", dependencies=[Depends(require_admin)])
async def update_mobile(phone_id: str, data: MobileCreate):
    result = await db.mobiles.update_one({"_id": _oid(phone_id)}, {"$set": data.model_dump()})
    if result.matched_count == 0:
        raise HTTPException(404, "Phone not found")
    return {"message": "Updated"}


# ── DELETE /api/mobiles/{id} (admin) ─────────────────────────────────────────
@router.delete("/{phone_id}", dependencies=[Depends(require_admin)])
async def delete_mobile(phone_id: str):
    result = await db.mobiles.delete_one({"_id": _oid(phone_id)})
    if result.deleted_count == 0:
        raise HTTPException(404, "Phone not found")
    await db.prices.delete_many({"mobile_id": phone_id})
    return {"message": "Deleted"}
