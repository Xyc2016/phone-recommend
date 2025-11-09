"""手机搜索工具 - 让 AI Agent 能够从 MongoDB 搜索手机"""

import logging
from typing import Any, Dict, List, Optional

from langchain.tools import tool
from pydantic import BaseModel, Field

from app.models.phone import Phone, PhoneSearchParams
from app.services.phone_service import phone_service

logger = logging.getLogger("app.tools.phone_search")


@tool
async def search_phones(
    keyword: Optional[str] = None,
    brand: Optional[str] = None,
    tags: Optional[List[str]] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    ram: Optional[str] = None,
    storage: Optional[str] = None,
    min_display_size: Optional[float] = None,
    max_display_size: Optional[float] = None,
    min_battery: Optional[int] = None,
    max_battery: Optional[int] = None,
    limit: int = 5,
) -> list[Phone]:
    """
    从数据库搜索手机信息。

    这个工具可以根据多种条件搜索手机，包括：
    - 关键词：品牌、型号、描述、特色等
    - 品牌：精确匹配品牌名称
    - 标签：如旗舰机、游戏手机、拍照手机等
    - 价格区间：最低价格到最高价格
    - 硬件配置：运行内存、存储容量
    - 屏幕尺寸：最小与最大屏幕尺寸（英寸）
    - 电池容量：最小与最大电池容量（mAh）

    Args:
        keyword: 关键词搜索
        brand: 品牌名称
        tags: 标签列表
        min_price: 最低价格
        max_price: 最高价格
        ram: 运行内存
        storage: 存储容量
        limit: 返回结果数量（1-20，默认5）

    Returns:
        list[Phone]: 手机列表
    """
    print("calling", locals())
    try:
        # 构建搜索参数
        params = PhoneSearchParams(
            keyword=keyword,
            brand=brand,
            tags=tags or [],
            min_price=min_price,
            max_price=max_price,
            ram=ram,
            storage=storage,
            min_display_size=min_display_size,
            max_display_size=max_display_size,
            min_battery=min_battery,
            max_battery=max_battery,
            limit=limit,
        )

        logger.info(
            "Searching phones with params: keyword=%s, brand=%s, tags=%s, "
            "min_price=%s, max_price=%s, ram=%s, storage=%s, "
            "min_display_size=%s, max_display_size=%s, min_battery=%s, max_battery=%s, limit=%s",
            keyword,
            brand,
            tags,
            min_price,
            max_price,
            ram,
            storage,
            min_display_size,
            max_display_size,
            min_battery,
            max_battery,
            limit,
        )

        # 执行搜索
        phones = await phone_service.search_phones(params)

        return phones

    except Exception as e:
        logger.error("Error searching phones: %s", e, exc_info=True)
        return []
