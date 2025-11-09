"""为数据库添加示例手机数据"""

import asyncio
import logging
from datetime import UTC, datetime

from motor.motor_asyncio import AsyncIOMotorClient

from app.config import settings
from app.models import Phone, PhoneSku

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def _utc_now() -> datetime:
    return datetime.now(UTC)


# 示例手机数据
SAMPLE_PHONES = [
    Phone(
        brand="小米",
        model="小米14 Pro",
        description="徕卡光学全焦段三摄，骁龙8 Gen3旗舰芯片，120W澎湃秒充",
        os="HyperOS",
        chipset="骁龙8 Gen3",
        display_size=6.73,
        display_freq=120,
        battery=4880,
        camera="徕卡Summilux镜头，5000万像素主摄(Light Fusion 800)+5000万像素超广角+5000万像素浮动长焦",
        tags=["旗舰机", "拍照手机", "游戏手机"],
        features=["徕卡影像", "骁龙8 Gen3", "120W快充", "120Hz高刷", "IP68防水"],
        specs={
            "weight": "223g",
            "thickness": "8.49mm",
            "5G": True,
            "NFC": True,
            "IR": True,
        },
        skus=[
            PhoneSku(
                sku_id="mi14pro_12_256_black",
                name="12GB+256GB 黑色",
                ram="12GB",
                storage="256GB",
                color="黑色",
                price=4999,
                currency="CNY",
                availability="有货",
            ),
            PhoneSku(
                sku_id="mi14pro_16_512_white",
                name="16GB+512GB 白色",
                ram="16GB",
                storage="512GB",
                color="白色",
                price=5799,
                currency="CNY",
                availability="有货",
            ),
            PhoneSku(
                sku_id="mi14pro_16_1t_titan",
                name="16GB+1TB 钛金属",
                ram="16GB",
                storage="1TB",
                color="钛金属",
                price=6499,
                currency="CNY",
                availability="有货",
            ),
        ],
        created_at=_utc_now(),
        updated_at=_utc_now(),
    ),
    Phone(
        brand="华为",
        model="Mate 60 Pro",
        description="先锋之作，灵犀通信，XMAGE影像，鸿蒙4.0",
        os="HarmonyOS 4.0",
        chipset="麒麟9000s",
        display_size=6.82,
        display_freq=120,
        battery=5000,
        camera="超光变摄像头，5000万像素主摄+1200万像素超广角+4800万像素长焦",
        tags=["旗舰机", "拍照手机", "商务手机"],
        features=["卫星通信", "鸿蒙4.0", "XMAGE影像", "昆仑玻璃", "IP68防水"],
        specs={
            "weight": "225g",
            "thickness": "8.1mm",
            "5G": True,
            "NFC": True,
            "IR": True,
        },
        skus=[
            PhoneSku(
                sku_id="mate60pro_12_256_black",
                name="12GB+256GB 雅黑",
                ram="12GB",
                storage="256GB",
                color="雅黑",
                price=6999,
                currency="CNY",
                availability="有货",
            ),
            PhoneSku(
                sku_id="mate60pro_12_512_white",
                name="12GB+512GB 白色",
                ram="12GB",
                storage="512GB",
                color="白色",
                price=7999,
                currency="CNY",
                availability="有货",
            ),
        ],
        created_at=_utc_now(),
        updated_at=_utc_now(),
    ),
    Phone(
        brand="OPPO",
        model="Find X7 Ultra",
        description="四主摄，超光影影像系统，天玑9300旗舰芯片",
        os="ColorOS 14",
        chipset="天玑9300",
        display_size=6.82,
        display_freq=120,
        battery=5000,
        camera="四主摄：5000万像素索尼LYT-900主摄+5000万像素超广角+5000万像素潜望长焦+5000万像素长焦",
        tags=["旗舰机", "拍照手机"],
        features=["哈苏影像", "四主摄", "天玑9300", "100W快充", "IP68防水"],
        specs={
            "weight": "221g",
            "thickness": "9.5mm",
            "5G": True,
            "NFC": True,
            "IR": False,
        },
        skus=[
            PhoneSku(
                sku_id="findx7ultra_12_256_black",
                name="12GB+256GB 星辰黑",
                ram="12GB",
                storage="256GB",
                color="星辰黑",
                price=5999,
                currency="CNY",
                availability="有货",
            ),
            PhoneSku(
                sku_id="findx7ultra_16_512_brown",
                name="16GB+512GB 大漠银月",
                ram="16GB",
                storage="512GB",
                color="大漠银月",
                price=6999,
                currency="CNY",
                availability="有货",
            ),
        ],
        created_at=_utc_now(),
        updated_at=_utc_now(),
    ),
    Phone(
        brand="vivo",
        model="X100 Pro",
        description="蔡司APO超级长焦，天玑9300旗舰芯片，蓝晶×天玑9300芯片",
        os="OriginOS 4",
        chipset="天玑9300",
        display_size=6.78,
        display_freq=120,
        battery=5400,
        camera="蔡司影像：5000万像素主摄+5000万像素超广角+5000万像素APO长焦",
        tags=["旗舰机", "拍照手机"],
        features=["蔡司影像", "天玑9300", "蓝晶芯片", "5400mAh大电池", "IP68防水"],
        specs={
            "weight": "225g",
            "thickness": "8.91mm",
            "5G": True,
            "NFC": True,
            "IR": True,
        },
        skus=[
            PhoneSku(
                sku_id="x100pro_12_256_black",
                name="12GB+256GB 星迹蓝",
                ram="12GB",
                storage="256GB",
                color="星迹蓝",
                price=4999,
                currency="CNY",
                availability="有货",
            ),
            PhoneSku(
                sku_id="x100pro_16_512_white",
                name="16GB+512GB 落日橙",
                ram="16GB",
                storage="512GB",
                color="落日橙",
                price=5999,
                currency="CNY",
                availability="有货",
            ),
        ],
        created_at=_utc_now(),
        updated_at=_utc_now(),
    ),
    Phone(
        brand="一加",
        model="一加12",
        description="第四代骁龙8旗舰移动平台，2K东方屏，哈苏影像",
        os="ColorOS 14",
        chipset="骁龙8 Gen3",
        display_size=6.82,
        display_freq=120,
        battery=5400,
        camera="哈苏影像：5000万像素主摄+4800万像素超广角+6400万像素潜望长焦",
        tags=["旗舰机", "游戏手机", "性价比"],
        features=["骁龙8 Gen3", "2K东方屏", "5400mAh大电池", "100W快充", "哈苏影像"],
        specs={
            "weight": "220g",
            "thickness": "9.15mm",
            "5G": True,
            "NFC": True,
            "IR": True,
        },
        skus=[
            PhoneSku(
                sku_id="oneplus12_12_256_black",
                name="12GB+256GB 黑色",
                ram="12GB",
                storage="256GB",
                color="黑色",
                price=4299,
                currency="CNY",
                availability="有货",
            ),
            PhoneSku(
                sku_id="oneplus12_16_512_white",
                name="16GB+512GB 白色",
                ram="16GB",
                storage="512GB",
                color="白色",
                price=4799,
                currency="CNY",
                availability="有货",
            ),
            PhoneSku(
                sku_id="oneplus12_24_1t_green",
                name="24GB+1TB 苍绿",
                ram="24GB",
                storage="1TB",
                color="苍绿",
                price=5799,
                currency="CNY",
                availability="有货",
            ),
        ],
        created_at=_utc_now(),
        updated_at=_utc_now(),
    ),
    Phone(
        brand="Redmi",
        model="Redmi K70 Pro",
        description="2K高光屏，骁龙8 Gen3，极致性能释放",
        os="HyperOS",
        chipset="骁龙8 Gen3",
        display_size=6.67,
        display_freq=120,
        battery=5000,
        camera="5000万像素Light Fusion 800主摄+1200万像素超广角+5000万像素长焦",
        tags=["旗舰机", "性价比", "游戏手机"],
        features=["骁龙8 Gen3", "2K高光屏", "5000mAh电池", "120W快充", "性价比"],
        specs={
            "weight": "209g",
            "thickness": "8.21mm",
            "5G": True,
            "NFC": True,
            "IR": True,
        },
        skus=[
            PhoneSku(
                sku_id="k70pro_12_256_black",
                name="12GB+256GB 黑色",
                ram="12GB",
                storage="256GB",
                color="黑色",
                price=3299,
                currency="CNY",
                availability="有货",
            ),
            PhoneSku(
                sku_id="k70pro_16_512_white",
                name="16GB+512GB 白色",
                ram="16GB",
                storage="512GB",
                color="白色",
                price=3699,
                currency="CNY",
                availability="有货",
            ),
            PhoneSku(
                sku_id="k70pro_16_1t_green",
                name="16GB+1TB 墨羽",
                ram="16GB",
                storage="1TB",
                color="墨羽",
                price=4199,
                currency="CNY",
                availability="有货",
            ),
        ],
        created_at=_utc_now(),
        updated_at=_utc_now(),
    ),
    Phone(
        brand="荣耀",
        model="荣耀Magic6 Pro",
        description="荣耀鹰眼相机，骁龙8 Gen3，荣耀巨犀玻璃",
        os="MagicOS 8.0",
        chipset="骁龙8 Gen3",
        display_size=6.8,
        display_freq=120,
        battery=5600,
        camera="荣耀鹰眼相机：5000万像素主摄+5000万像素超广角+1.8亿像素潜望长焦",
        tags=["旗舰机", "拍照手机", "长续航"],
        features=[
            "1.8亿像素",
            "5600mAh超大电池",
            "荣耀鹰眼相机",
            "骁龙8 Gen3",
            "IP68防水",
        ],
        specs={
            "weight": "229g",
            "thickness": "8.9mm",
            "5G": True,
            "NFC": True,
            "IR": True,
        },
        skus=[
            PhoneSku(
                sku_id="magic6pro_12_256_black",
                name="12GB+256GB 曜石黑",
                ram="12GB",
                storage="256GB",
                color="曜石黑",
                price=5699,
                currency="CNY",
                availability="有货",
            ),
            PhoneSku(
                sku_id="magic6pro_16_512_green",
                name="16GB+512GB 海湖绿",
                ram="16GB",
                storage="512GB",
                color="海湖绿",
                price=6199,
                currency="CNY",
                availability="有货",
            ),
        ],
        created_at=_utc_now(),
        updated_at=_utc_now(),
    ),
    Phone(
        brand="真我",
        model="真我GT5 Pro",
        description="骁龙8 Gen3，真我首款旗舰影像手机",
        os="realme UI 5.0",
        chipset="骁龙8 Gen3",
        display_size=6.78,
        display_freq=144,
        battery=5400,
        camera="索尼IMX890主摄5000万像素+超广角5000万像素+长焦5000万像素",
        tags=["旗舰机", "性价比", "游戏手机"],
        features=["骁龙8 Gen3", "144Hz高刷", "5400mAh大电池", "100W快充", "性价比"],
        specs={
            "weight": "218g",
            "thickness": "8.6mm",
            "5G": True,
            "NFC": True,
            "IR": False,
        },
        skus=[
            PhoneSku(
                sku_id="gt5pro_12_256_green",
                name="12GB+256GB 极光",
                ram="12GB",
                storage="256GB",
                color="极光",
                price=3298,
                currency="CNY",
                availability="有货",
            ),
            PhoneSku(
                sku_id="gt5pro_16_512_white",
                name="16GB+512GB 皓月",
                ram="16GB",
                storage="512GB",
                color="皓月",
                price=3798,
                currency="CNY",
                availability="有货",
            ),
        ],
        created_at=_utc_now(),
        updated_at=_utc_now(),
    ),
]


async def seed_phones():
    """向数据库添加示例手机数据"""
    client = AsyncIOMotorClient(settings.mongodb_url)
    db = client[settings.mongodb_db_name]
    collection = db.get_collection("phones")

    # 清空现有数据（可选）
    logger.info("Clearing existing phone data...")
    await collection.delete_many({})

    # 插入示例数据
    logger.info("Inserting %d sample phones...", len(SAMPLE_PHONES))
    documents = [phone.py() for phone in SAMPLE_PHONES]
    result = await collection.insert_many(documents)
    logger.info("Inserted %d phones successfully", len(result.inserted_ids))

    # 创建索引以提高搜索性能
    logger.info("Creating indexes...")
    await collection.create_index("brand")
    await collection.create_index("model")
    await collection.create_index("tags")
    await collection.create_index("updated_at")
    logger.info("Indexes created successfully")

    client.close()
    logger.info("Seeding completed!")


if __name__ == "__main__":
    asyncio.run(seed_phones())
