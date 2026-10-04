"""Markets the site stays out of: ecommerce, retail, and wine or other alcohol.

PRODUCT.md records the decision. build_landing.py fails the build when a
landing page uses this language; build_news.py leaves matching stories off
the news page. Jekyll skips _-prefixed folders, so this file is not published.
"""
import re

EXCLUDED = re.compile(
    r"\b(wines?|winer(y|ies)|vineyards?|vintners?|alcohol|liquor|spirits|beverages?|brewer(y|ies)"
    r"|e-?commerce|storefronts?|shopify|online (shop|store)s?|retail(ers?)?|skus?|reorder"
    r"|dtc|direct.to.consumer|stock levels?|stockouts?|where.?s my order|where is my order)\b",
    re.I,
)
