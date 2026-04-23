"""
routes/compare.py
"""
from fastapi import APIRouter, HTTPException
from bson import ObjectId
from database import db
from models import CompareRequest
import re

router = APIRouter()

def _extract_num(val) -> float:
    nums = re.findall(r"[\d.]+", str(val))
    return float(nums[0]) if nums else 0

@router.post("/")
async def compare_phones(data: CompareRequest):
    phones = []
    for pid in data.phone_ids:
        try: oid = ObjectId(pid)
        except Exception: raise HTTPException(400, f"Invalid id: {pid}")
        phone = await db.mobiles.find_one({"_id": oid})
        if not phone: raise HTTPException(404, f"Phone {pid} not found")
        sellers = await db.prices.find({"mobile_id": pid}).sort([("price", 1)]).to_list(20)
        for s in sellers: s["id"] = str(s.pop("_id"))
        phone["sellers"]   = sellers
        phone["min_price"] = sellers[0]["price"] if sellers else phone.get("base_price", 0)
        phones.append(phone)

    winner = {
        "price":   str(min(phones, key=lambda p: p["min_price"])["_id"]),
        "rating":  str(max(phones, key=lambda p: p.get("rating", 0))["_id"]),
        "battery": str(max(phones, key=lambda p: _extract_num(p.get("specs", {}).get("battery", "")))["_id"]),
        "camera":  str(max(phones, key=lambda p: _extract_num(p.get("specs", {}).get("camera", "")))["_id"]),
        "ram":     str(max(phones, key=lambda p: _extract_num(p.get("specs", {}).get("ram", "")))["_id"]),
    }

    for p in phones:
        p["id"] = str(p.pop("_id"))
    return {"phones": phones, "winner": winner}
