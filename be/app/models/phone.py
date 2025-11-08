from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field

from app.models.base import MongoModel


class PhoneSku(BaseModel):
    """手机 SKU 信息"""

    sku_id: str = Field(..., description="SKU 唯一标识")
    name: Optional[str] = Field(None, max_length=100, description="SKU 名称或规格描述，例如“12GB+256GB”")
    ram: Optional[str] = Field(None, max_length=50, description="运行内存配置，例如 12GB")
    storage: Optional[str] = Field(None, max_length=50, description="存储容量，例如 256GB")
    color: Optional[str] = Field(None, max_length=50, description="颜色")
    price: Optional[float] = Field(
        None,
        ge=0,
        description="价格，单位由 currency 字段决定",
    )
    currency: str = Field(
        "CNY",
        min_length=3,
        max_length=3,
        description="价格币种，默认 CNY",
    )
    availability: Optional[str] = Field(
        None,
        max_length=50,
        description="库存或销售状态描述",
    )
    extra: Dict[str, Any] = Field(
        default_factory=dict,
        description="额外的规格信息，键值对形式",
    )


class Phone(MongoModel):
    """手机数据模型"""

    brand: str = Field(..., max_length=100, description="品牌名称")
    model: str = Field(..., max_length=100, description="型号名称")
    description: Optional[str] = Field(None, description="型号简介或卖点")
    os: Optional[str] = Field(None, max_length=100, description="操作系统或界面")
    chipset: Optional[str] = Field(None, max_length=150, description="SoC/芯片型号")
    display: Optional[str] = Field(None, max_length=200, description="屏幕相关信息")
    battery: Optional[str] = Field(None, max_length=200, description="电池及充电信息")
    camera: Optional[str] = Field(None, max_length=200, description="摄像头信息")
    tags: List[str] = Field(default_factory=list, description="标签列表，用于检索")
    features: List[str] = Field(default_factory=list, description="特色功能列表")
    specs: Dict[str, Any] = Field(default_factory=dict, description="详细规格字典")
    skus: List[PhoneSku] = Field(default_factory=list, description="可选 SKU 列表")
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class PhoneSearchParams(BaseModel):
    """手机搜索参数"""

    keyword: Optional[str] = Field(None, description="关键词，匹配品牌、型号、描述、特色等")
    brand: Optional[str] = Field(None, description="品牌精确匹配")
    tags: List[str] = Field(default_factory=list, description="标签列表，全部匹配")
    min_price: Optional[float] = Field(None, ge=0, description="最低价格")
    max_price: Optional[float] = Field(None, ge=0, description="最高价格")
    ram: Optional[str] = Field(None, description="期望的运行内存配置")
    storage: Optional[str] = Field(None, description="期望的存储配置")
    limit: int = Field(
        5,
        ge=1,
        le=20,
        description="返回结果数量上限，默认 5，最大 20",
    )
