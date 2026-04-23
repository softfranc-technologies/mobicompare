"""
routes/admin.py
"""
from fastapi import APIRouter, Depends
from database import db
from auth_utils import require_admin
from datetime import datetime

router = APIRouter()

@router.get("/stats", dependencies=[Depends(require_admin)])
async def dashboard_stats():
    return {
        "total_phones":  await db.mobiles.count_documents({}),
        "total_prices":  await db.prices.count_documents({}),
        "total_users":   await db.users.count_documents({}),
        "total_alerts":  await db.price_alerts.count_documents({}),
        "active_alerts": await db.price_alerts.count_documents({"triggered": False}),
        "total_reviews": await db.reviews.count_documents({}),
    }

@router.post("/trigger-alerts", dependencies=[Depends(require_admin)])
async def trigger_alerts():
    alerts = await db.price_alerts.find({"triggered": False}).to_list(1000)
    triggered = 0
    for alert in alerts:
        best = await db.prices.find_one({"mobile_id": alert["mobile_id"]}, sort=[("price", 1)])
        if best and best["price"] <= alert["target_price"]:
            print(f"📧 Alert triggered: {alert['user_email']} — price hit ₹{best['price']}")
            await db.price_alerts.update_one(
                {"_id": alert["_id"]},
                {"$set": {"triggered": True, "triggered_at": datetime.utcnow()}}
            )
            triggered += 1
    return {"triggered": triggered}
