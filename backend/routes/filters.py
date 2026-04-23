"""
routes/filters.py
"""
from fastapi import APIRouter
from database import db

router = APIRouter()

@router.get("/")
async def get_filter_options():
    brands   = await db.mobiles.distinct("brand")
    rams     = await db.mobiles.distinct("specs.ram")
    storages = await db.mobiles.distinct("specs.storage")
    procs    = await db.mobiles.distinct("specs.processor")
    pipeline = [{"$group": {"_id": None, "min": {"$min": "$base_price"}, "max": {"$max": "$base_price"}}}]
    price_result = await db.mobiles.aggregate(pipeline).to_list(1)
    price_min = price_result[0]["min"] if price_result else 5000
    price_max = price_result[0]["max"] if price_result else 200000
    return {
        "brands":    sorted(brands),
        "ram":       sorted(rams,     key=lambda x: int(x.split()[0]) if x.split()[0].isdigit() else 0),
        "storage":   sorted(storages, key=lambda x: int(x.split()[0]) if x.split()[0].isdigit() else 0),
        "processor": sorted(procs),
        "price_min": price_min,
        "price_max": price_max,
    }
