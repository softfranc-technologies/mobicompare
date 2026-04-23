"""
models.py — Pydantic schemas for request/response validation
"""
from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum


class BadgeType(str, Enum):
    hot    = "hot"
    new    = "new"
    budget = "budget"

class SortBy(str, Enum):
    popular    = "popular"
    price_low  = "price-low"
    price_high = "price-high"
    rating     = "rating"
    newest     = "newest"


class PhoneSpecs(BaseModel):
    display:   str
    processor: str
    ram:       str
    storage:   str
    battery:   str
    camera:    str
    os:        str
    fiveG:     bool = True


class SellerPrice(BaseModel):
    mobile_id:     str
    website:       str
    price:         int
    link:          str
    delivery:      str  = "Free delivery"
    return_policy: str  = "7-day return"
    in_stock:      bool = True
    updated_at:    datetime = Field(default_factory=datetime.utcnow)


class MobileBase(BaseModel):
    name:       str
    brand:      str
    badge:      BadgeType = BadgeType.new
    specs:      PhoneSpecs
    images:     List[str] = []
    rating:     float = Field(0.0, ge=0, le=5)
    reviews:    int   = 0
    base_price: int
    old_price:  int
    insights:   List[str] = []
    year:       int = 2025


class MobileCreate(MobileBase):
    pass


class UserRegister(BaseModel):
    name:     str
    email:    EmailStr
    password: str = Field(..., min_length=8)

class UserLogin(BaseModel):
    email:    EmailStr
    password: str

class UserOut(BaseModel):
    id:    str
    name:  str
    email: EmailStr

class Token(BaseModel):
    access_token: str
    token_type:   str = "bearer"
    user:         UserOut


class PriceAlertCreate(BaseModel):
    mobile_id:    str
    user_email:   EmailStr
    target_price: int

class ReviewCreate(BaseModel):
    mobile_id: str
    user_id:   str
    rating:    int = Field(..., ge=1, le=5)
    title:     str
    body:      str

class CompareRequest(BaseModel):
    phone_ids: List[str] = Field(..., min_length=2, max_length=3)
