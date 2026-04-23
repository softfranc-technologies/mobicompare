"""
database/seed.py — Populate MongoDB with all phones + seller prices
Run: python seed.py
"""
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime
import sys, os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "backend"))

MONGO_URI = os.environ.get("MONGO_URI", "mongodb://localhost:27017")
MONGO_DB  = os.environ.get("MONGO_DB",  "mobicompare")

# ─── Phone data ───────────────────────────────────────────────────────────────
PHONES = [
  # ── SAMSUNG ──
  {"name":"Galaxy S25 Ultra","brand":"Samsung","badge":"hot",
   "images":["https://images.samsung.com/is/image/samsung/p6pim/in/2501/gallery/in-galaxy-s25-ultra-sm-s938-sm-s938bztqins-thumb-544369352"],
   "specs":{"display":'6.9" QHD+ LTPO AMOLED',"processor":"Snapdragon 8 Elite","ram":"12 GB","storage":"256 GB","battery":"5000 mAh","camera":"200 MP","os":"Android 15","fiveG":True},
   "rating":4.8,"reviews":2847,"base_price":133999,"old_price":149999,"year":2025,
   "insights":["Best Display","5G Ready","Top Camera"]},

  {"name":"Galaxy S25+","brand":"Samsung","badge":"hot",
   "images":["https://images.samsung.com/is/image/samsung/p6pim/in/2501/gallery/in-galaxy-s25-plus-sm-s936-sm-s936bzkgins-thumb-544369368"],
   "specs":{"display":'6.7" AMOLED 2X',"processor":"Snapdragon 8 Elite","ram":"12 GB","storage":"256 GB","battery":"4900 mAh","camera":"50 MP","os":"Android 15","fiveG":True},
   "rating":4.7,"reviews":1420,"base_price":99999,"old_price":119999,"year":2025,
   "insights":["5G Ready","Fast Charging","Premium Build"]},

  {"name":"Galaxy A56 5G","brand":"Samsung","badge":"new",
   "images":["https://images.samsung.com/is/image/samsung/p6pim/in/sm-a566elggins/gallery/in-galaxy-a56-sm-a566-sm-a566elggins-thumb"],
   "specs":{"display":'6.7" Super AMOLED',"processor":"Exynos 1580","ram":"8 GB","storage":"128 GB","battery":"5000 mAh","camera":"50 MP","os":"Android 15","fiveG":True},
   "rating":4.4,"reviews":890,"base_price":35999,"old_price":42999,"year":2025,
   "insights":["5G Ready","IP67 Rating","Great Display"]},

  {"name":"Galaxy F55 5G","brand":"Samsung","badge":"budget",
   "images":["https://images.samsung.com/is/image/samsung/p6pim/in/sm-f556elgeins/gallery/in-galaxy-f55-sm-f556-sm-f556elgeins-thumb"],
   "specs":{"display":'6.7" Super AMOLED',"processor":"Snapdragon 7 Gen 1","ram":"8 GB","storage":"128 GB","battery":"5000 mAh","camera":"50 MP","os":"Android 14","fiveG":True},
   "rating":4.2,"reviews":1200,"base_price":26999,"old_price":31999,"year":2024,
   "insights":["5G Ready","Best Battery","Value Pick"]},

  # ── APPLE ──
  {"name":"iPhone 16 Pro Max","brand":"Apple","badge":"hot",
   "images":["https://store.storeimages.cdn-apple.com/4982/as-images.apple.com/is/iphone-16-pro-max-finish-unselect-gallery-2-202409?wid=5120&hei=2880&fmt=p-jpg&qlt=80&.v=1724015237814"],
   "specs":{"display":'6.9" Super Retina XDR OLED',"processor":"A18 Pro","ram":"8 GB","storage":"256 GB","battery":"4685 mAh","camera":"48 MP","os":"iOS 18","fiveG":True},
   "rating":4.9,"reviews":6210,"base_price":144900,"old_price":159900,"year":2024,
   "insights":["Best Performance","Premium Build","5G Ready"]},

  {"name":"iPhone 16 Pro","brand":"Apple","badge":"hot",
   "images":["https://store.storeimages.cdn-apple.com/4982/as-images.apple.com/is/iphone-16-pro-model-unselect-gallery-2-202409?wid=5120&hei=2880&fmt=p-jpg&qlt=80&.v=1725779498513"],
   "specs":{"display":'6.3" Super Retina XDR OLED',"processor":"A18 Pro","ram":"8 GB","storage":"128 GB","battery":"3274 mAh","camera":"48 MP","os":"iOS 18","fiveG":True},
   "rating":4.9,"reviews":5120,"base_price":119900,"old_price":134900,"year":2024,
   "insights":["Best Performance","5G Ready","ProRAW Camera"]},

  {"name":"iPhone 15","brand":"Apple","badge":"budget",
   "images":["https://store.storeimages.cdn-apple.com/4982/as-images.apple.com/is/iphone-15-model-unselect-gallery-1-202309?wid=5120&hei=2880&fmt=p-jpg&qlt=80&.v=1693086369818"],
   "specs":{"display":'6.1" Super Retina XDR',"processor":"A16 Bionic","ram":"6 GB","storage":"128 GB","battery":"3877 mAh","camera":"48 MP","os":"iOS 18","fiveG":True},
   "rating":4.7,"reviews":7832,"base_price":69900,"old_price":79900,"year":2023,
   "insights":["5G Ready","USB-C","Dynamic Island"]},

  # ── ONEPLUS ──
  {"name":"OnePlus 13","brand":"OnePlus","badge":"hot",
   "images":["https://image01.oneplus.net/ebp/202501/03/1-m00-5d-60-rb8bl2bsfemay2fzaafnlbvgjwg291.png"],
   "specs":{"display":'6.82" LTPO AMOLED',"processor":"Snapdragon 8 Elite","ram":"16 GB","storage":"512 GB","battery":"6000 mAh","camera":"50 MP","os":"Android 15","fiveG":True},
   "rating":4.7,"reviews":1842,"base_price":69999,"old_price":79999,"year":2025,
   "insights":["Best Battery","5G Ready","Fast Charging"]},

  {"name":"OnePlus Nord 4","brand":"OnePlus","badge":"new",
   "images":["https://image01.oneplus.net/ebp/202407/16/1-m00-5d-60-rb8bkwbsfeiad4zlaadgfr1emm0684.png"],
   "specs":{"display":'6.74" AMOLED',"processor":"Snapdragon 7+ Gen 3","ram":"8 GB","storage":"256 GB","battery":"5500 mAh","camera":"50 MP","os":"Android 14","fiveG":True},
   "rating":4.4,"reviews":1050,"base_price":29999,"old_price":34999,"year":2024,
   "insights":["5G Ready","Metal Body","Fast Charge"]},

  # ── XIAOMI / REDMI / POCO ──
  {"name":"Xiaomi 15 Pro","brand":"Xiaomi","badge":"new",
   "images":["https://i02.appmifile.com/mi-com-product/fly-birds/xiaomi-15-pro/m/pc/intro-360.png"],
   "specs":{"display":'6.73" LTPO AMOLED',"processor":"Snapdragon 8 Elite","ram":"16 GB","storage":"512 GB","battery":"6100 mAh","camera":"50 MP","os":"Android 15","fiveG":True},
   "rating":4.6,"reviews":983,"base_price":59999,"old_price":64999,"year":2025,
   "insights":["5G Ready","Fast Charging","Best Value"]},

  {"name":"Redmi Note 14 Pro+","brand":"Xiaomi","badge":"budget",
   "images":["https://i02.appmifile.com/mi-com-product/fly-birds/redmi-note-14-pro-plus/m/pc/kv-section-1.png"],
   "specs":{"display":'6.67" AMOLED',"processor":"Dimensity 7300 Ultra","ram":"8 GB","storage":"256 GB","battery":"5500 mAh","camera":"200 MP","os":"Android 14","fiveG":True},
   "rating":4.3,"reviews":2103,"base_price":23999,"old_price":28999,"year":2024,
   "insights":["200MP Camera","5G Ready","Best Budget"]},

  {"name":"POCO X7 Pro 5G","brand":"Xiaomi","badge":"budget",
   "images":["https://in.xiaomi.com/public/upload/d6a4bfbb-8513-4734-b2e6-6bc28e16baff.png"],
   "specs":{"display":'6.67" AMOLED',"processor":"Dimensity 8400 Ultra","ram":"12 GB","storage":"256 GB","battery":"6550 mAh","camera":"50 MP","os":"Android 15","fiveG":True},
   "rating":4.4,"reviews":1576,"base_price":27999,"old_price":32999,"year":2025,
   "insights":["Massive Battery","5G Ready","Gaming Beast"]},

  # ── REALME ──
  {"name":"Realme GT 7 Pro","brand":"Realme","badge":"new",
   "images":["https://image.realme.com/cdn-cgi/image/format=auto,onerror=redirect,width=2048/content/dam/realme/in/product-images/realme-gt-7-pro/realme-gt7-pro.png"],
   "specs":{"display":'6.78" AMOLED',"processor":"Snapdragon 8 Elite","ram":"12 GB","storage":"256 GB","battery":"6500 mAh","camera":"50 MP","os":"Android 15","fiveG":True},
   "rating":4.5,"reviews":1204,"base_price":41999,"old_price":49999,"year":2024,
   "insights":["Best Battery","5G Ready","Great Value"]},

  {"name":"Realme Narzo 70 Pro","brand":"Realme","badge":"budget",
   "images":["https://image.realme.com/cdn-cgi/image/format=auto,onerror=redirect,width=2048/content/dam/realme/in/product-images/narzo-70-pro/narzo70pro.png"],
   "specs":{"display":'6.67" AMOLED',"processor":"Dimensity 7050","ram":"8 GB","storage":"128 GB","battery":"5000 mAh","camera":"50 MP","os":"Android 14","fiveG":True},
   "rating":4.1,"reviews":780,"base_price":17999,"old_price":22999,"year":2024,
   "insights":["Budget Pick","5G Ready","Good Camera"]},

  # ── VIVO ──
  {"name":"Vivo X200 Pro","brand":"Vivo","badge":"hot",
   "images":["https://cdnassets.vivo.com/uploads/image/file/a/ab7d1e90de5c4bc78fcd5e843c7aef0a.png"],
   "specs":{"display":'6.78" AMOLED',"processor":"Dimensity 9400","ram":"16 GB","storage":"512 GB","battery":"5800 mAh","camera":"200 MP","os":"Android 15","fiveG":True},
   "rating":4.6,"reviews":742,"base_price":74999,"old_price":84999,"year":2024,
   "insights":["Best Camera","5G Ready","Zeiss Optics"]},

  {"name":"Vivo V40 Pro","brand":"Vivo","badge":"new",
   "images":["https://cdnassets.vivo.com/uploads/image/file/2/2e7a4f5b9c3d4e6f8a1b0c4d5e6f7890.png"],
   "specs":{"display":'6.78" AMOLED',"processor":"Snapdragon 7 Gen 3","ram":"12 GB","storage":"256 GB","battery":"5500 mAh","camera":"50 MP","os":"Android 14","fiveG":True},
   "rating":4.3,"reviews":620,"base_price":39999,"old_price":44999,"year":2024,
   "insights":["Zeiss Cameras","5G Ready","Fast Charge"]},

  # ── GOOGLE PIXEL ──
  {"name":"Pixel 9 Pro XL","brand":"Google","badge":"hot",
   "images":["https://lh3.googleusercontent.com/pixel-9-pro-xl-obsidian"],
   "specs":{"display":'6.8" LTPO OLED',"processor":"Tensor G4","ram":"16 GB","storage":"256 GB","battery":"5100 mAh","camera":"50 MP","os":"Android 15","fiveG":True},
   "rating":4.7,"reviews":920,"base_price":109999,"old_price":124999,"year":2024,
   "insights":["Best AI Camera","Pure Android","5G Ready"]},

  {"name":"Pixel 9","brand":"Google","badge":"new",
   "images":["https://lh3.googleusercontent.com/pixel-9-obsidian"],
   "specs":{"display":'6.3" OLED',"processor":"Tensor G4","ram":"12 GB","storage":"128 GB","battery":"4700 mAh","camera":"50 MP","os":"Android 15","fiveG":True},
   "rating":4.6,"reviews":710,"base_price":79999,"old_price":89999,"year":2024,
   "insights":["AI-Powered","Pure Android","5G Ready"]},

  # ── MOTOROLA ──
  {"name":"Motorola Edge 50 Ultra","brand":"Motorola","badge":"new",
   "images":["https://motorola-global-portal.custhelp.com/ci/fattach/get/2128001/0/filename/EDGE_50_ULTRA.png"],
   "specs":{"display":'6.7" pOLED',"processor":"Snapdragon 8s Gen 3","ram":"12 GB","storage":"256 GB","battery":"4500 mAh","camera":"50 MP","os":"Android 14","fiveG":True},
   "rating":4.4,"reviews":652,"base_price":49999,"old_price":59999,"year":2024,
   "insights":["Stock Android","5G Ready","Thin Design"]},

  {"name":"Moto G85 5G","brand":"Motorola","badge":"budget",
   "images":["https://motorola-global-portal.custhelp.com/ci/fattach/get/2128005/0/filename/MOTO_G85.png"],
   "specs":{"display":'6.67" pOLED',"processor":"Snapdragon 6s Gen 3","ram":"8 GB","storage":"128 GB","battery":"5000 mAh","camera":"50 MP","os":"Android 14","fiveG":True},
   "rating":4.2,"reviews":1100,"base_price":17999,"old_price":21999,"year":2024,
   "insights":["Budget Pick","5G Ready","Stock Android"]},

  # ── NOTHING ──
  {"name":"Nothing Phone (3)","brand":"Nothing","badge":"hot",
   "images":["https://in.nothing.tech/cdn/shop/files/Phone_3_Transparent_1.png?v=1737634811"],
   "specs":{"display":'6.77" AMOLED',"processor":"Snapdragon 8s Gen 3","ram":"12 GB","storage":"256 GB","battery":"5150 mAh","camera":"50 MP","os":"Android 15","fiveG":True},
   "rating":4.5,"reviews":521,"base_price":39999,"old_price":44999,"year":2025,
   "insights":["Unique Design","5G Ready","Glyph Interface"]},

  {"name":"Nothing Phone (2a) Plus","brand":"Nothing","badge":"budget",
   "images":["https://in.nothing.tech/cdn/shop/files/phone-2a-plus-black.png?v=1724823101"],
   "specs":{"display":'6.7" AMOLED',"processor":"Dimensity 7350 Pro","ram":"12 GB","storage":"256 GB","battery":"5000 mAh","camera":"50 MP","os":"Android 14","fiveG":True},
   "rating":4.3,"reviews":870,"base_price":23999,"old_price":27999,"year":2024,
   "insights":["Glyph LED","5G Ready","Unique Design"]},

  # ── ASUS ──
  {"name":"ASUS ROG Phone 9 Pro","brand":"ASUS","badge":"hot",
   "images":["https://dlcdnwebimgs.asus.com/files/media/2024/rog-phone-9-pro/img/kv/phone-front.webp"],
   "specs":{"display":'6.78" AMOLED 185Hz',"processor":"Snapdragon 8 Elite","ram":"24 GB","storage":"1 TB","battery":"5800 mAh","camera":"50 MP","os":"Android 15","fiveG":True},
   "rating":4.7,"reviews":430,"base_price":124999,"old_price":139999,"year":2024,
   "insights":["Gaming Beast","185Hz Display","5G Ready"]},

  # ── OPPO ──
  {"name":"OPPO Find X8 Pro","brand":"OPPO","badge":"hot",
   "images":["https://image.oppo.com/content/dam/oppo/product-asset-library/find-x8-pro/find-x8-pro-v3/assets/img/body-phone.png"],
   "specs":{"display":'6.78" LTPO AMOLED',"processor":"Dimensity 9400","ram":"16 GB","storage":"512 GB","battery":"5910 mAh","camera":"50 MP","os":"Android 15","fiveG":True},
   "rating":4.6,"reviews":560,"base_price":89999,"old_price":99999,"year":2024,
   "insights":["Hasselblad Camera","5G Ready","Best Battery"]},

  {"name":"OPPO Reno 13 Pro","brand":"OPPO","badge":"new",
   "images":["https://image.oppo.com/content/dam/oppo/product-asset-library/reno13-pro/assets/img/kv-phone.png"],
   "specs":{"display":'6.83" AMOLED',"processor":"Dimensity 8350","ram":"12 GB","storage":"256 GB","battery":"5600 mAh","camera":"50 MP","os":"Android 15","fiveG":True},
   "rating":4.3,"reviews":410,"base_price":39999,"old_price":45999,"year":2025,
   "insights":["5G Ready","AI Camera","Good Battery"]},

  # ── iQOO ──
  {"name":"iQOO 13","brand":"iQOO","badge":"hot",
   "images":["https://www.iqoo.com/content/dam/iqoo-website/in/iqoo-13/overview/kv-phone.png"],
   "specs":{"display":'6.82" LTPO AMOLED',"processor":"Snapdragon 8 Elite","ram":"16 GB","storage":"512 GB","battery":"6000 mAh","camera":"50 MP","os":"Android 15","fiveG":True},
   "rating":4.7,"reviews":880,"base_price":54999,"old_price":64999,"year":2025,
   "insights":["Gaming Beast","144Hz Display","5G Ready"]},

  {"name":"iQOO Z9s Pro","brand":"iQOO","badge":"budget",
   "images":["https://www.iqoo.com/content/dam/iqoo-website/in/iqoo-z9s-pro/overview/kv-phone.png"],
   "specs":{"display":'6.77" AMOLED',"processor":"Dimensity 9200+","ram":"8 GB","storage":"128 GB","battery":"5500 mAh","camera":"50 MP","os":"Android 14","fiveG":True},
   "rating":4.3,"reviews":720,"base_price":22999,"old_price":26999,"year":2024,
   "insights":["Flagship Chip","5G Ready","Gaming"]},

  # ── TECNO ──
  {"name":"Tecno Phantom V Fold 2","brand":"Tecno","badge":"new",
   "images":["https://tecno-in.com/wp-content/uploads/2024/09/phantom-v-fold2-main.png"],
   "specs":{"display":'7.85" LTPO AMOLED Fold',"processor":"Dimensity 9300+","ram":"16 GB","storage":"512 GB","battery":"5750 mAh","camera":"50 MP","os":"Android 14","fiveG":True},
   "rating":4.2,"reviews":280,"base_price":94999,"old_price":109999,"year":2024,
   "insights":["Foldable","5G Ready","Unique Design"]},

  {"name":"Tecno Spark 30 Pro","brand":"Tecno","badge":"budget",
   "images":["https://tecno-in.com/wp-content/uploads/2024/08/spark-30-pro-main.png"],
   "specs":{"display":'6.78" AMOLED',"processor":"Helio G100","ram":"8 GB","storage":"256 GB","battery":"5000 mAh","camera":"108 MP","os":"Android 14","fiveG":False},
   "rating":4.0,"reviews":450,"base_price":13999,"old_price":16999,"year":2024,
   "insights":["Budget Pick","108MP Camera","Good Battery"]},

  # ── INFINIX ──
  {"name":"Infinix Zero 40 5G","brand":"Infinix","badge":"budget",
   "images":["https://in.infinixmobility.com/public/cache/b7b9e45b1de05bfca80a2eb6c4d84680/file/zqwpkm.png"],
   "specs":{"display":'6.78" AMOLED',"processor":"Dimensity 8020","ram":"12 GB","storage":"256 GB","battery":"5000 mAh","camera":"108 MP","os":"Android 14","fiveG":True},
   "rating":4.1,"reviews":340,"base_price":19999,"old_price":23999,"year":2024,
   "insights":["Budget 5G","108MP Camera","AMOLED"]},

  # ── NOKIA ──
  {"name":"Nokia G42 5G","brand":"Nokia","badge":"budget",
   "images":["https://www.nokia.com/sites/default/files/styles/scale_720_no_upscale/public/2023-08/nokia-g42-5g-so-pink.png"],
   "specs":{"display":'6.56" HD+',"processor":"Snapdragon 480+","ram":"6 GB","storage":"128 GB","battery":"5000 mAh","camera":"50 MP","os":"Android 13","fiveG":True},
   "rating":4.0,"reviews":520,"base_price":14999,"old_price":18999,"year":2023,
   "insights":["Budget 5G","3-Year Updates","Durable"]},
]

# ─── Seller price data per phone ──────────────────────────────────────────────
SELLERS_MAP = {
  "Samsung": [
    {"website":"Samsung Official","delivery":"Free, 2-3 days","return_policy":"7-day return","link":"https://www.samsung.com/in/"},
    {"website":"Croma",           "delivery":"Free, 1-2 days","return_policy":"10-day return","link":"https://www.croma.com/"},
    {"website":"Vijay Sales",     "delivery":"Free, 2-4 days","return_policy":"7-day return","link":"https://www.vijaysales.com/"},
    {"website":"Reliance Digital","delivery":"Free, 3-5 days","return_policy":"7-day return","link":"https://www.reliancedigital.in/"},
    {"website":"Tata Cliq",       "delivery":"Free, 2-3 days","return_policy":"7-day return","link":"https://www.tatacliq.com/"},
  ],
  "Apple": [
    {"website":"Apple Official","delivery":"Free, 1-2 days","return_policy":"14-day return","link":"https://www.apple.com/in/"},
    {"website":"Croma",         "delivery":"Free, 1-2 days","return_policy":"10-day return","link":"https://www.croma.com/"},
    {"website":"JioMart",       "delivery":"Free, 2-3 days","return_policy":"7-day return", "link":"https://www.jiomart.com/"},
    {"website":"Vijay Sales",   "delivery":"Free, 2-4 days","return_policy":"7-day return", "link":"https://www.vijaysales.com/"},
    {"website":"Tata Cliq",     "delivery":"Free, 2-3 days","return_policy":"7-day return", "link":"https://www.tatacliq.com/"},
  ],
  "OnePlus": [
    {"website":"OnePlus Official","delivery":"Free, 2-3 days","return_policy":"15-day return","link":"https://www.oneplus.in/"},
    {"website":"Croma",           "delivery":"Free, 1-2 days","return_policy":"10-day return","link":"https://www.croma.com/"},
    {"website":"Vijay Sales",     "delivery":"Free, 2-4 days","return_policy":"7-day return", "link":"https://www.vijaysales.com/"},
    {"website":"Reliance Digital","delivery":"Free, 3-5 days","return_policy":"7-day return", "link":"https://www.reliancedigital.in/"},
    {"website":"Snapdeal",        "delivery":"Paid, 4-6 days","return_policy":"5-day return", "link":"https://www.snapdeal.com/"},
  ],
  "Xiaomi": [
    {"website":"Xiaomi Official","delivery":"Free, 2-3 days","return_policy":"10-day return","link":"https://www.mi.com/in/"},
    {"website":"Croma",          "delivery":"Free, 1-2 days","return_policy":"10-day return","link":"https://www.croma.com/"},
    {"website":"Vijay Sales",    "delivery":"Free, 2-4 days","return_policy":"7-day return", "link":"https://www.vijaysales.com/"},
    {"website":"Snapdeal",       "delivery":"Paid, 4-6 days","return_policy":"5-day return", "link":"https://www.snapdeal.com/"},
    {"website":"JioMart",        "delivery":"Free, 2-3 days","return_policy":"7-day return", "link":"https://www.jiomart.com/"},
  ],
  "Realme": [
    {"website":"Realme Official","delivery":"Free, 2-3 days","return_policy":"10-day return","link":"https://www.realme.com/in/"},
    {"website":"Croma",          "delivery":"Free, 1-2 days","return_policy":"10-day return","link":"https://www.croma.com/"},
    {"website":"Vijay Sales",    "delivery":"Free, 2-4 days","return_policy":"7-day return", "link":"https://www.vijaysales.com/"},
    {"website":"Snapdeal",       "delivery":"Paid, 4-6 days","return_policy":"5-day return", "link":"https://www.snapdeal.com/"},
    {"website":"JioMart",        "delivery":"Free, 2-3 days","return_policy":"7-day return", "link":"https://www.jiomart.com/"},
  ],
  "Vivo": [
    {"website":"Vivo Official",  "delivery":"Free, 2-3 days","return_policy":"10-day return","link":"https://www.vivo.com/in/"},
    {"website":"Croma",          "delivery":"Free, 1-2 days","return_policy":"10-day return","link":"https://www.croma.com/"},
    {"website":"Reliance Digital","delivery":"Free, 3-5 days","return_policy":"7-day return","link":"https://www.reliancedigital.in/"},
    {"website":"Tata Cliq",      "delivery":"Free, 2-3 days","return_policy":"7-day return", "link":"https://www.tatacliq.com/"},
    {"website":"Vijay Sales",    "delivery":"Free, 2-4 days","return_policy":"7-day return", "link":"https://www.vijaysales.com/"},
  ],
  "Google": [
    {"website":"Google Store",   "delivery":"Free, 2-3 days","return_policy":"15-day return","link":"https://store.google.com/in/"},
    {"website":"Croma",          "delivery":"Free, 1-2 days","return_policy":"10-day return","link":"https://www.croma.com/"},
    {"website":"Vijay Sales",    "delivery":"Free, 2-4 days","return_policy":"7-day return", "link":"https://www.vijaysales.com/"},
    {"website":"Tata Cliq",      "delivery":"Free, 2-3 days","return_policy":"7-day return", "link":"https://www.tatacliq.com/"},
    {"website":"JioMart",        "delivery":"Free, 2-3 days","return_policy":"7-day return", "link":"https://www.jiomart.com/"},
  ],
  "Motorola": [
    {"website":"Motorola Official","delivery":"Free, 2-3 days","return_policy":"10-day return","link":"https://www.motorola.in/"},
    {"website":"Croma",            "delivery":"Free, 1-2 days","return_policy":"10-day return","link":"https://www.croma.com/"},
    {"website":"Vijay Sales",      "delivery":"Free, 2-4 days","return_policy":"7-day return", "link":"https://www.vijaysales.com/"},
    {"website":"JioMart",          "delivery":"Free, 2-3 days","return_policy":"7-day return", "link":"https://www.jiomart.com/"},
    {"website":"Snapdeal",         "delivery":"Paid, 4-6 days","return_policy":"5-day return", "link":"https://www.snapdeal.com/"},
  ],
  "Nothing": [
    {"website":"Nothing Official","delivery":"Free, 3-5 days","return_policy":"7-day return","link":"https://in.nothing.tech/"},
    {"website":"Croma",           "delivery":"Free, 1-2 days","return_policy":"10-day return","link":"https://www.croma.com/"},
    {"website":"Tata Cliq",       "delivery":"Free, 2-3 days","return_policy":"7-day return","link":"https://www.tatacliq.com/"},
    {"website":"Vijay Sales",     "delivery":"Free, 2-4 days","return_policy":"7-day return","link":"https://www.vijaysales.com/"},
    {"website":"Cashify",         "delivery":"Paid, 3-5 days","return_policy":"No return",   "link":"https://www.cashify.in/"},
  ],
  "ASUS": [
    {"website":"ASUS Official",  "delivery":"Free, 3-5 days","return_policy":"7-day return","link":"https://www.asus.com/in/"},
    {"website":"Croma",          "delivery":"Free, 1-2 days","return_policy":"10-day return","link":"https://www.croma.com/"},
    {"website":"Vijay Sales",    "delivery":"Free, 2-4 days","return_policy":"7-day return","link":"https://www.vijaysales.com/"},
    {"website":"Tata Cliq",      "delivery":"Free, 2-3 days","return_policy":"7-day return","link":"https://www.tatacliq.com/"},
    {"website":"Reliance Digital","delivery":"Free, 3-5 days","return_policy":"7-day return","link":"https://www.reliancedigital.in/"},
  ],
  "OPPO": [
    {"website":"OPPO Official",  "delivery":"Free, 2-3 days","return_policy":"10-day return","link":"https://www.oppo.com/in/"},
    {"website":"Croma",          "delivery":"Free, 1-2 days","return_policy":"10-day return","link":"https://www.croma.com/"},
    {"website":"Vijay Sales",    "delivery":"Free, 2-4 days","return_policy":"7-day return", "link":"https://www.vijaysales.com/"},
    {"website":"Reliance Digital","delivery":"Free, 3-5 days","return_policy":"7-day return","link":"https://www.reliancedigital.in/"},
    {"website":"JioMart",        "delivery":"Free, 2-3 days","return_policy":"7-day return", "link":"https://www.jiomart.com/"},
  ],
  "iQOO": [
    {"website":"iQOO Official",  "delivery":"Free, 2-3 days","return_policy":"10-day return","link":"https://www.iqoo.com/in/"},
    {"website":"Croma",          "delivery":"Free, 1-2 days","return_policy":"10-day return","link":"https://www.croma.com/"},
    {"website":"Vijay Sales",    "delivery":"Free, 2-4 days","return_policy":"7-day return", "link":"https://www.vijaysales.com/"},
    {"website":"Reliance Digital","delivery":"Free, 3-5 days","return_policy":"7-day return","link":"https://www.reliancedigital.in/"},
    {"website":"Snapdeal",       "delivery":"Paid, 4-6 days","return_policy":"5-day return", "link":"https://www.snapdeal.com/"},
  ],
  "Tecno": [
    {"website":"Tecno Official","delivery":"Free, 3-5 days","return_policy":"7-day return","link":"https://www.tecno-mobile.com/in/"},
    {"website":"Croma",         "delivery":"Free, 1-2 days","return_policy":"10-day return","link":"https://www.croma.com/"},
    {"website":"JioMart",       "delivery":"Free, 2-3 days","return_policy":"7-day return", "link":"https://www.jiomart.com/"},
    {"website":"Vijay Sales",   "delivery":"Free, 2-4 days","return_policy":"7-day return", "link":"https://www.vijaysales.com/"},
    {"website":"Snapdeal",      "delivery":"Paid, 4-6 days","return_policy":"5-day return", "link":"https://www.snapdeal.com/"},
  ],
  "Infinix": [
    {"website":"Infinix Official","delivery":"Free, 3-5 days","return_policy":"7-day return","link":"https://in.infinixmobility.com/"},
    {"website":"Croma",           "delivery":"Free, 1-2 days","return_policy":"10-day return","link":"https://www.croma.com/"},
    {"website":"JioMart",         "delivery":"Free, 2-3 days","return_policy":"7-day return", "link":"https://www.jiomart.com/"},
    {"website":"Vijay Sales",     "delivery":"Free, 2-4 days","return_policy":"7-day return", "link":"https://www.vijaysales.com/"},
    {"website":"Snapdeal",        "delivery":"Paid, 4-6 days","return_policy":"5-day return", "link":"https://www.snapdeal.com/"},
  ],
  "Nokia": [
    {"website":"Nokia Official","delivery":"Free, 3-5 days","return_policy":"7-day return","link":"https://www.nokia.com/phones/en_in/"},
    {"website":"Croma",         "delivery":"Free, 1-2 days","return_policy":"10-day return","link":"https://www.croma.com/"},
    {"website":"JioMart",       "delivery":"Free, 2-3 days","return_policy":"7-day return", "link":"https://www.jiomart.com/"},
    {"website":"Vijay Sales",   "delivery":"Free, 2-4 days","return_policy":"7-day return", "link":"https://www.vijaysales.com/"},
    {"website":"Snapdeal",      "delivery":"Paid, 4-6 days","return_policy":"5-day return", "link":"https://www.snapdeal.com/"},
  ],
}

# Price multipliers per seller (vs base_price)
PRICE_OFFSETS = {
  "Samsung Official": 0.00, "Apple Official": 0.00, "OnePlus Official": 0.00,
  "Xiaomi Official": 0.00,  "Realme Official": 0.00, "Vivo Official": 0.00,
  "Google Store": 0.00,     "Motorola Official": 0.00, "Nothing Official": 0.00,
  "ASUS Official": 0.00,    "OPPO Official": 0.00, "iQOO Official": 0.00,
  "Tecno Official": 0.00,   "Infinix Official": 0.00, "Nokia Official": 0.00,
  "Croma":  0.015,   "Vijay Sales": 0.004,  "Reliance Digital": 0.025,
  "JioMart":-0.015,  "Tata Cliq":  -0.010,  "Snapdeal": -0.020,
  "Cashify":-0.030,
}

import random

async def seed():
    client = AsyncIOMotorClient(MONGO_URI)
    db = client[MONGO_DB]

    # Clear existing data
    await db.mobiles.drop()
    await db.prices.drop()
    print("🗑️  Cleared existing mobiles & prices collections")

    total_phones  = 0
    total_sellers = 0

    for phone_data in PHONES:
        phone_doc = {**phone_data, "created_at": datetime.utcnow()}
        result = await db.mobiles.insert_one(phone_doc)
        mobile_id = str(result.inserted_id)
        total_phones += 1

        brand    = phone_data["brand"]
        base     = phone_data["base_price"]
        sellers  = SELLERS_MAP.get(brand, SELLERS_MAP["Xiaomi"])

        for s in sellers:
            offset   = PRICE_OFFSETS.get(s["website"], 0)
            # Add a small random jitter so prices feel real
            jitter   = random.uniform(-0.005, 0.005)
            price    = max(1000, round(base * (1 + offset + jitter) / 100) * 100)
            price_doc = {
                "mobile_id":     mobile_id,
                "website":       s["website"],
                "price":         price,
                "link":          s["link"],
                "delivery":      s["delivery"],
                "return_policy": s["return_policy"],
                "in_stock":      True,
                "updated_at":    datetime.utcnow(),
            }
            await db.prices.insert_one(price_doc)
            total_sellers += 1

        print(f"  ✅ {phone_data['brand']} {phone_data['name']} — ₹{base:,} — {len(sellers)} sellers")

    # ── Create admin user ──────────────────────────────────────────────────────
    from passlib.context import CryptContext
    pwd = CryptContext(schemes=["bcrypt"], deprecated="auto")

    await db.users.drop()
    await db.users.insert_one({
        "name":       "Admin",
        "email":      "admin@mobicompare.in",
        "password":   pwd.hash("admin1234"),
        "is_admin":   True,
        "created_at": datetime.utcnow(),
    })
    print("\n👤 Admin user created: admin@mobicompare.in / admin1234")

    # ── Indexes ────────────────────────────────────────────────────────────────
    from pymongo import ASCENDING, DESCENDING, TEXT
    await db.mobiles.create_index([("name", TEXT), ("brand", TEXT)])
    await db.mobiles.create_index([("brand", ASCENDING)])
    await db.mobiles.create_index([("base_price", ASCENDING)])
    await db.mobiles.create_index([("rating", DESCENDING)])
    await db.prices.create_index( [("mobile_id", ASCENDING)])
    await db.prices.create_index( [("price", ASCENDING)])
    await db.users.create_index(  [("email", ASCENDING)], unique=True)
    print("📊 Indexes created")

    client.close()
    print(f"\n🎉 Seed complete! {total_phones} phones, {total_sellers} price entries inserted.\n")

if __name__ == "__main__":
    asyncio.run(seed())
