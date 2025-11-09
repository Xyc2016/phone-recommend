from __future__ import annotations

import logging
from datetime import datetime
from typing import Any, Dict, List, Optional

from motor.motor_asyncio import AsyncIOMotorCollection

from app.database import get_phones_collection
from app.models import Phone, PhoneSearchParams, PhoneSku

logger = logging.getLogger("app.phone_service")


class PhoneService:
    """手机数据服务，仅提供查询功能供 LLM 工具使用。"""

    def __init__(self) -> None:
        self._collection: Optional[AsyncIOMotorCollection] = None

    @property
    def collection(self) -> AsyncIOMotorCollection:
        if self._collection is None:
            self._collection = get_phones_collection()
        return self._collection

    async def search_phones(self, params: PhoneSearchParams) -> List[Phone]:
        """按照参数搜索手机列表"""
        query = self._build_search_query(params)
        logger.debug("Phone search query: %s", query)

        cursor = self.collection.find(query).sort("updated_at", -1).limit(params.limit)

        results: List[Phone] = []
        async for doc in cursor:
            results.append(Phone.model_validate(doc))
        return results

    def _build_search_query(self, params: PhoneSearchParams) -> Dict[str, Any]:
        """构建 MongoDB 查询"""
        query: Dict[str, Any] = {}

        if params.brand:
            query["brand"] = {"$regex": params.brand.strip(), "$options": "i"}

        if params.keyword:
            keyword_regex = {"$regex": params.keyword.strip(), "$options": "i"}
            query.setdefault("$or", [])
            query["$or"].extend(
                [
                    {"brand": keyword_regex},
                    {"model": keyword_regex},
                    {"description": keyword_regex},
                    {"features": keyword_regex},
                    {"tags": keyword_regex},
                ]
            )

        if params.tags:
            tags = [tag.strip() for tag in params.tags if tag.strip()]
            if tags:
                query["tags"] = {"$all": tags}

        display_constraints: Dict[str, float] = {}
        if params.min_display_size is not None:
            display_constraints["$gte"] = params.min_display_size
        if params.max_display_size is not None:
            display_constraints["$lte"] = params.max_display_size
        if display_constraints:
            query["display_size"] = display_constraints

        battery_constraints: Dict[str, int] = {}
        if params.min_battery is not None:
            battery_constraints["$gte"] = params.min_battery
        if params.max_battery is not None:
            battery_constraints["$lte"] = params.max_battery
        if battery_constraints:
            query["battery"] = battery_constraints

        sku_match: Dict[str, Any] = {}
        price_constraints: Dict[str, float] = {}
        if params.min_price is not None:
            price_constraints["$gte"] = params.min_price
        if params.max_price is not None:
            price_constraints["$lte"] = params.max_price
        if price_constraints:
            sku_match["price"] = price_constraints

        if params.ram:
            sku_match["ram"] = {"$regex": params.ram.strip(), "$options": "i"}
        if params.storage:
            sku_match["storage"] = {"$regex": params.storage.strip(), "$options": "i"}

        if sku_match:
            query["skus"] = {"$elemMatch": sku_match}

        return query


phone_service = PhoneService()
