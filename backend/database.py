"""
database.py — MongoDB async connection via Motor
"""
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import ASCENDING, DESCENDING, TEXT
from config import settings
import logging

logger = logging.getLogger(__name__)

class Database:
    client: AsyncIOMotorClient = None
    db = None

    async def connect(self):
        self.client = AsyncIOMotorClient(settings.MONGO_URI)
        self.db = self.client[settings.MONGO_DB]
        await self._create_indexes()
        logger.info(f"Connected to MongoDB: {settings.MONGO_DB}")

    async def disconnect(self):
        if self.client:
            self.client.close()

    async def ping(self) -> bool:
        try:
            await self.client.admin.command("ping")
            return True
        except Exception:
            return False

    async def _create_indexes(self):
        await self.db.mobiles.create_index([("name", TEXT), ("brand", TEXT)])
        await self.db.mobiles.create_index([("brand", ASCENDING)])
        await self.db.mobiles.create_index([("base_price", ASCENDING)])
        await self.db.mobiles.create_index([("rating", DESCENDING)])
        await self.db.mobiles.create_index([("specs.fiveG", ASCENDING)])
        await self.db.mobiles.create_index([("created_at", DESCENDING)])
        await self.db.prices.create_index([("mobile_id", ASCENDING)])
        await self.db.prices.create_index([("website", ASCENDING)])
        await self.db.prices.create_index([("price", ASCENDING)])
        await self.db.users.create_index([("email", ASCENDING)], unique=True)
        await self.db.price_alerts.create_index([("user_email", ASCENDING)])
        await self.db.price_alerts.create_index([("mobile_id", ASCENDING)])
        logger.info("MongoDB indexes created")

    @property
    def mobiles(self):      return self.db.mobiles
    @property
    def prices(self):       return self.db.prices
    @property
    def users(self):        return self.db.users
    @property
    def price_alerts(self): return self.db.price_alerts
    @property
    def reviews(self):      return self.db.reviews
    @property
    def wishlist(self):     return self.db.wishlist

db = Database()
