"""
routes/prices.py
"""
from fastapi import APIRouter, HTTPException, Depends
from bson import ObjectId
from database import db
from models import PriceAlertCreate
from auth_utils import require_admin
from datetime import datetime

router = APIRouter()

@router.get("/{mobile_id}")
async def get_prices(mobile_id: str):
    sellers = await db.prices.find({"mobile_id": mobile_id}).sort([("price", 1)]).to_list(20)
    if not sellers:
        raise HTTPException(404, "No price data found for this phone")
    for s in sellers:
        s["id"] = str(s.pop("_id"))
    return {"mobile_id": mobile_id, "sellers": sellers, "cheapest": sellers[0], "updated_at": sellers[0].get("updated_at")}

@router.post("/alert", status_code=201)
async def set_price_alert(data: PriceAlertCreate):
    doc = data.model_dump()
    doc["triggered"]  = False
    doc["created_at"] = datetime.utcnow()
    existing = await db.price_alerts.find_one({"mobile_id": data.mobile_id, "user_email": data.user_email})
    if existing:
        await db.price_alerts.update_one({"_id": existing["_id"]}, {"$set": {"target_price": data.target_price, "triggered": False}})
        return {"message": "Alert updated"}
    result = await db.price_alerts.insert_one(doc)
    return {"id": str(result.inserted_id), "message": "Alert created"}

@router.get("/alerts/{email}")
async def get_alerts(email: str):
    alerts = await db.price_alerts.find({"user_email": email}).to_list(100)
    for a in alerts: a["id"] = str(a.pop("_id"))
    return alerts
